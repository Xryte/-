from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator


class CustomUserCreationForm(UserCreationForm):

    username = forms.CharField(
        label='Имя пользователя',
        min_length=3,
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'От 3 до 30 символов',
            'maxlength': '30',
        }),
        help_text='От 3 до 30 символов. Только буквы, цифры и @/./+/-/_',
        validators=[
            MinLengthValidator(3, message='Минимум 3 символа'),
            MaxLengthValidator(30, message='Максимум 30 символов'),
        ]
    )

    password1 = forms.CharField(
        label='Пароль',
        min_length=8,
        max_length=128,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control password-field',
            'placeholder': 'Минимум 8 символов',
            'maxlength': '128',
        }),
        help_text='Минимум 8 символов',
        validators=[
            MinLengthValidator(8, message='Минимум 8 символов'),
        ]
    )

    password2 = forms.CharField(
        label='Подтверждение пароля',
        min_length=8,
        max_length=128,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control password-field',
            'placeholder': 'Повторите пароль',
            'maxlength': '128',
        }),
        help_text='Повторите пароль для проверки',
        validators=[
            MinLengthValidator(8, message='Минимум 8 символов'),
        ]
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class CustomAuthenticationForm(AuthenticationForm):

    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите имя пользователя',
        })
    )

    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control password-field',
            'placeholder': 'Введите пароль',
        })
    )