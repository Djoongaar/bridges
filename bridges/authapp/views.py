from django.forms import forms
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.detail import DetailView
from .forms import RegisterUserForm

from .models import Users


# Create your views here.

class RegisterUserView(CreateView):
    model = Users
    form_class = RegisterUserForm
    extra_context = {
        'page_title': 'Регистрация на сайте',
        'bred_title': 'Регистрация'
    }
    template_name = 'authapp/register.html'
    success_url = reverse_lazy('auth:login')


class UserLoginView(LoginView):
    extra_context = {
        'page_title': 'Авторизация на сайте',
        'bred_title': 'Авторизация'
    }
    template_name = 'authapp/login.html'


class UserProfileView(DetailView):
    model = Users
    extra_context = {
        'page_title': 'Профиль пользователя',
        'bred_title': 'Профиль пользователя'
    }
    template_name = 'authapp/profile.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context


class UserLogoutView(LogoutView):
    extra_context = {
        'page_title': 'Выход с сайта',
        'bred_title': 'Выход с сайта'
    }
    template_name = 'authapp/logout.html'
