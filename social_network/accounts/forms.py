from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username')

class CustomUserChangeForm(UserChangeForm):
    email = forms.EmailField(label=_('Email'), widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label=_('Имя пользователя'), help_text=_(
        'Обязательное поле. Не более 150 символов. Только буквы, цифры и @/./+/-/_'),
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    profile_picture = forms.ImageField(label=_('Аватар'), required=False,
                                     widget=forms.FileInput(attrs={'class': 'form-control'}))
    bio = forms.CharField(label=_('О себе'), required=False,
                         widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'profile_picture', 'bio')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Удаляем поле пароля из формы
        self.fields.pop('password', None)

from django.contrib.auth.forms import PasswordResetForm


class AutoEmailPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, request=None, **kwargs):
        if self.user:
            self.cleaned_data = {'email': self.user.email}
        return super().save(request=request, **kwargs)

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваш email'
        })
    )


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