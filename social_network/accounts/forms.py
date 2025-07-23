from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'profile_picture', 'bio')


from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError


class CustomAuthenticationForm(AuthenticationForm):
    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            UserModel = get_user_model()
            try:
                user = UserModel.objects.get(email=email)
                if not user.check_password(password):
                    raise ValidationError("Invalid password")
                if not user.is_active:
                    raise ValidationError("User is inactive")
            except UserModel.DoesNotExist:
                raise ValidationError("User with this email does not exist")

            self.user_cache = user
            return self.cleaned_data