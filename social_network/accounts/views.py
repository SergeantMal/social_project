from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Exists, OuterRef
from django.shortcuts import render, get_object_or_404

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import FormView, RedirectView

from messaging.models import Conversation
from notifications.models import Notification
from .forms import CustomUserCreationForm, CustomUserChangeForm, AutoEmailPasswordResetForm
from .models import CustomUser, Subscription
from django.contrib import messages
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST


@login_required
def profile_view(request, username=None):
    if username is None:
        # Если username не указан, показываем профиль текущего пользователя
        profile_user = request.user
    else:
        # Иначе показываем профиль указанного пользователя
        profile_user = get_object_or_404(CustomUser, username=username)

    # Подсчет непрочитанных сообщений (только для личных бесед)
    unread_count = 0
    if request.user.is_authenticated and request.user != profile_user:
        conversation = Conversation.objects.filter(
            participants=request.user
        ).filter(
            participants=profile_user
        ).first()

        if conversation:
            unread_count = conversation.messages.filter(
                is_read=False
            ).exclude(
                sender=request.user
            ).count()

    # Проверка подписки
    is_subscribed = False
    if request.user.is_authenticated and request.user != profile_user:
        is_subscribed = request.user.subscriptions.filter(target_user=profile_user).exists()

    return render(request, 'accounts/profile.html', {
        'profile_user': profile_user,
        'is_subscribed': is_subscribed,
        'unread_count': unread_count,
    })

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('feed:home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')  # Редирект на собственный профиль
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'accounts/profile_edit.html', {'form': form})

from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'accounts/login.html'

    def form_invalid(self, form):
        messages.error(self.request, "Login failed. Please check your credentials.")
        return super().form_invalid(form)

def logout_view(request):
    logout(request)
    return redirect('feed:home')


@require_POST
@login_required
def toggle_subscription(request, username):
    target_user = get_object_or_404(CustomUser, username=username)

    if request.user == target_user:
        return JsonResponse({'error': 'Cannot subscribe to yourself'}, status=400)

    is_subscribed = request.user.is_subscribed_to(target_user)

    if is_subscribed:
        request.user.unsubscribe(target_user)
    else:
        request.user.subscribe(target_user)
        Notification.objects.create(
            user=target_user,
            sender=request.user,
            notification_type='follow',  # Используем 'follow' вместо 'subscription'
            message=f"{request.user.username} подписался(ась) на вас"
        )

    return JsonResponse({
        'new_status': not is_subscribed,
        'subscribers_count': target_user.subscribers_count,
        'success': True
    })

@login_required
def subscriptions_list(request, username):
    user = get_object_or_404(CustomUser, username=username)
    subscriptions = user.subscriptions.all()
    return render(request, 'accounts/subscriptions_list.html', {
        'profile_user': user,
        'subscriptions': subscriptions
    })


@login_required
def subscribers_list(request, username):
    user = get_object_or_404(CustomUser, username=username)
    subscribers = user.subscribers.all()
    return render(request, 'accounts/subscribers_list.html', {
        'profile_user': user,
        'subscribers': subscribers
    })

User = get_user_model()


@login_required
def user_list(request):
    query = request.GET.get('q', '')
    users = CustomUser.objects.all().order_by('username')

    if query:
        users = users.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query)
        )

    return render(request, 'accounts/user_list.html', {
        'users': users,
        'search_query': query
    })


class InstantPasswordResetView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        # Создаем временную форму и отправляем письмо
        from django.contrib.auth.forms import PasswordResetForm
        form = PasswordResetForm(data={'email': self.request.user.email})
        if form.is_valid():
            form.save(
                request=self.request,
                email_template_name='accounts/registration/password_reset_email.html',
                subject_template_name='accounts/registration/password_reset_subject.txt'
            )
            messages.success(self.request, f"Ссылка для сброса пароля отправлена на {self.request.user.email}")
        else:
            messages.error(self.request, "Ошибка при отправке письма")

        return reverse_lazy('accounts:password_reset_done')