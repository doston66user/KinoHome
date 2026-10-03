from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from KinoHome.models import Comment, Gender, Profile


class LoginForm(AuthenticationForm):
    username = forms.CharField(label=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите Логин'
    }))
    password = forms.CharField(label=False, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите Пароль'
    }))


class RegisterForm(UserCreationForm):
    username = forms.CharField(label=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Придумайте Логин'
    }))

    first_name = forms.CharField(label=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите ваше Имя'
    }))

    last_name = forms.CharField(label=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите Фамилию'
    }))

    gender = forms.ModelChoiceField(queryset=Gender.objects.all(), label=False, widget=forms.Select(attrs={
        'class': 'form-control',
        'placeholder': 'Введите Пол'
    }))

    email = forms.EmailField(label=False, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите вашу Почту'
    }))

    password1 = forms.CharField(label=False, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Придумайте Пароль'
    }))

    password2 = forms.CharField(label=False, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Подтвердите Пароль'
    }))

    country_region = forms.CharField(label=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите страну проживания'
    }))

    phone_number = forms.CharField(label=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите ваш номер телефона (через +)'
    }))

    class Meta:
        model = User
        fields = (
        'first_name', 'last_name', 'phone_number', 'country_region', 'username', 'gender', 'email', 'password1',
        'password2')


class CommentForm(forms.ModelForm):
    text = forms.CharField(label=False, widget=forms.Textarea(attrs={
        'class': 'form-control bg-dark',
        'placeholder': 'Оставить комментарий'
    }))

    class Meta:
        model = Comment
        fields = ['text']


class EditAccountForm(forms.ModelForm):
    username = forms.CharField(label=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    first_name = forms.CharField(label=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    last_name = forms.CharField(label=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    gender = forms.ModelChoiceField(queryset=Gender.objects.all(), label=False,
                                    widget=forms.Select(attrs={
                                        'class': 'form-control',
                                    }))

    email = forms.EmailField(label=False, widget=forms.EmailInput(attrs={
        'class': 'form-control',
    }))

    old_password = forms.CharField(required=False, label=False, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Текущий Пароль'
    }))

    new_password = forms.CharField(required=False, min_length=8, label=False, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Новый Пароль'
    }))

    confirm_password = forms.CharField(required=False, min_length=8, label=False, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Подтвердите Пароль'
    }))
    class Meta:
        model = User
        fields = (
        'first_name', 'last_name', 'username', 'gender', 'email', 'old_password', 'new_password',
        'confirm_password')


class EditProfileForm(forms.ModelForm):
    phone = forms.CharField(label=False, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Номер телефона'
    }))
    country = forms.CharField(label=False, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Страна или регион'
    }))
    about = forms.CharField(label=False, required=False, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'О себе'
    }))

    avatar = forms.ImageField(label=False, required=False, widget=forms.FileInput(attrs={
        'class': 'form-control bg-dark text-light'
    }))

    class Meta:
        model = Profile
        fields = ('phone', 'country', 'about', 'avatar')
