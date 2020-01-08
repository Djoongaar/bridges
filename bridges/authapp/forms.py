from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField, PasswordResetForm

from projectsapp.models import ProjectManagers
from .models import *


class RegisterUserForm(forms.ModelForm):
    username = UsernameField(widget=forms.TextInput(attrs={
        'placeholder': "Логин *",
        'style': "width: 250px;",
        'tabindex': "1"
    }))
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': "Моб. телефон *",
        'style': "width: 250px;",
        'tabindex': "2"
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': "Пароль *",
        'style': "width: 503px;",
        'tabindex': "3"
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': "Повторите пароль *",
        'style': "width: 503px;",
        'tabindex': "4"
    }))

    class Meta:
        model = Users
        fields = ('username', 'phone', 'password', 'password2')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Введенные пароли не совпадают')
        return cd['password2']


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={
        'autofocus': True,
        'placeholder': "Логин *",
        'style': "width: 250px;",
        'tabindex': "1"
    }))
    password = forms.CharField(strip=False, widget=forms.PasswordInput(attrs={
        'placeholder': "Пароль *",
        'style': "width: 250px;",
        'tabindex': "2"
    }),
    )


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={
        'placeholder': "Email *",
        'style': "width: 500px;",
        'tabindex': "1"
    }))


class UsersForEditProfileForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = [
            'first_name',
            'patronymic',
            'last_name',
            'avatar',
            'description',
            'gender',
            'birthday',
            'phone',
            'email',
            'is_active',
        ]


class UsersSelfEditProfileForm(forms.ModelForm):
    # birthday
    class Meta:
        model = Users
        fields = [
            'description',
            'birthday',
            'email',
        ]


class UsersForCompanyUsersForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = []


class CompanyUsersForm(forms.ModelForm):
    class Meta:
        model = CompanyUsers
        exclude = ()


class UsersForProjectManagersForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = []


class ProjectManagersForm(forms.ModelForm):
    class Meta:
        model = ProjectManagers
        exclude = ('is_active',)
