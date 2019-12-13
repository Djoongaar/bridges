from django import forms
from projectsapp.models import ProjectManagers
from .models import *


class RegisterUserForm(forms.ModelForm):
    password = forms.CharField(label='Введите пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторно введите пароль', widget=forms.PasswordInput)

    class Meta:
        model = Users
        fields = ('username', 'phone', 'password', 'password2')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Введенные пароли не совпадают')
        return cd['password2']


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
