from django.shortcuts import render

# Create your views here.


from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from django.contrib import messages
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})

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
            return redirect('accounts:profile')
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