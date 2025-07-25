from django.shortcuts import render, get_object_or_404

# Create your views here.


from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
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

    is_subscribed = False
    if request.user.is_authenticated and request.user != profile_user:
        is_subscribed = request.user.subscriptions.filter(target_user=profile_user).exists()

    return render(request, 'accounts/profile.html', {
        'profile_user': profile_user,
        'is_subscribed': is_subscribed
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

    # Возвращаем обновленные данные
    return JsonResponse({
        'new_status': not is_subscribed,
        'subscribers_count': target_user.subscribers_count
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