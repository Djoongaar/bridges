from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView, PasswordResetView
from django.db.models import Q
from django.forms import inlineformset_factory, modelformset_factory
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from guardian.decorators import permission_required, permission_required_or_403
from guardian.shortcuts import assign_perm

from newsapp.models import News
from ordersapp.models import Order
from django.views.generic import View, CreateView
from .forms import *
from .models import *


@user_passes_test(lambda u: u.is_staff)
def get_inactive_users(request):
    inactive_users = Users.objects.filter(is_active=False)
    return inactive_users


@login_required
def restricted_area(request):
    user = get_object_or_404(Users, pk=request.user.pk)
    user_companies = CompanyUsers.objects.filter(user_id=user.pk, works=True)
    user_projects = ProjectManagers.objects.filter(manager_id=user.pk).order_by('-project__updated')
    user_orders = Order.objects.filter(user_id=user.pk)
    my_news = News.objects.filter(author_id=request.user.pk)
    if user.is_superuser:
        partners = Company.objects.all().order_by('name')
        users = Users.objects.all().order_by('last_name')
    elif user.is_staff:
        partners = Company.objects.all().order_by('name')
        users = Users.objects.all().order_by('last_name').exclude(
            Q(is_staff=True) |
            Q(username='AnonymousUser'))
    else:
        partners = user_companies
        users = Users.objects.filter(is_staff=True).exclude(is_superuser=True)
    context = {
        'section': 'restricted_area',
        'page_title': 'Личный кабинет',
        'bred_title': 'Личный кабинет',
        'user_companies': user_companies,
        'user_projects': user_projects,
        'user_orders': user_orders,
        'inactive_users': get_inactive_users(request),
        'partners': partners,
        'my_news': my_news,
        'users': users,
        'user': user
    }
    return render(request, 'authapp/restricted_area.html', context)


def register(request):
    if request.method == 'POST':
        user_form = RegisterUserForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.is_active = False
            new_user.save()
            return render(request, 'authapp/register_done.html', {
                'new_user': new_user,
                'page_title': 'Успешная регистрация',
                'bred_title': 'Регистрация'
            })
    else:
        user_form = RegisterUserForm()
    context = {
        'form': user_form,
        'page_title': 'Регистрация на сайте',
        'bred_title': 'Регистрация'
    }
    return render(request, 'authapp/register.html', context)


@cache_page(3600)
def user_profile(request, pk):
    user = get_object_or_404(Users, pk=pk)
    if request.user.pk == user.pk:
        return HttpResponseRedirect(user.get_self_absolute_url())
    else:
        user_companies = CompanyUsers.objects.filter(user_id=pk, works=True)
        user = get_object_or_404(Users, pk=pk)
        user_projects = ProjectManagers.objects.filter(manager_id=pk).order_by('-project__updated')
        context = {
            'user': user,
            'user_projects': user_projects,
            'user_companies': user_companies,
            'page_title': 'Профиль пользователя',
            'bred_title': 'Профиль пользователя'
        }
        return render(request, 'authapp/user_profile.html', context)


def company_self_user_update(request, pk):
    company_user = get_object_or_404(Users, pk=pk)
    company_user_form = UsersForCompanyUsersForm(instance=company_user)
    InlineFormset = inlineformset_factory(Users, CompanyUsers, form=CompanyUsersForm, extra=1)
    formset = InlineFormset(instance=company_user)
    if request.method == 'POST':
        company_user_form = UsersForCompanyUsersForm(request.POST, instance=company_user)
        formset = InlineFormset(request.POST)
        if company_user_form.is_valid():
            updated_company_user_form = company_user_form.save(commit=False)
            formset = InlineFormset(request.POST, instance=updated_company_user_form)
            if formset.is_valid():
                updated_company_user_form.save()
                formset.save()
                return HttpResponseRedirect(updated_company_user_form.get_self_absolute_url())
    context = {
        'form': company_user_form,
        'formset': formset,
        'user': company_user,
        'page_title': 'Редактор компаний пользователя',
        'bred_title': 'Редактор компаний пользователя'
    }
    return render(request, 'authapp/self_profile_update.html', context)


def profile_self_user_update(request, pk):
    user = get_object_or_404(Users, pk=pk)
    user_form = UsersSelfEditProfileForm(instance=user)
    if request.method == 'POST':
        user_form = UsersSelfEditProfileForm(request.POST, request.FILES, instance=user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(user.get_self_absolute_url())
    context = {
        'form': user_form,
        'page_title': 'Редактор профиля пользователя',
        'bred_title': 'Редактор профиля пользователя'
    }
    return render(request, 'authapp/self_profile_update.html', context)


def profile_user_update(request, pk):
    user = get_object_or_404(Users, pk=pk)
    if request.user.has_perm('change_users', user):
        user_form = UsersForEditProfileForm(instance=user)
        if request.method == 'POST':
            user_form = UsersForEditProfileForm(request.POST, instance=user)
            if user_form.is_valid():
                user_form.save()
                return HttpResponseRedirect(user.get_absolute_url())
        context = {
            'form': user_form,
            'form_user': user,
            'page_title': 'Редактор профиля пользователя',
            'bred_title': 'Редактор профиля пользователя'
        }
        return render(request, 'authapp/user_profile_update.html', context)
    else:
        raise Http404


@user_passes_test(lambda u: u.is_staff)
def profile_user_activate(request, pk):
    user = get_object_or_404(Users, pk=pk)
    user_form = UsersForEditProfileForm(instance=user)
    if request.method == 'POST':
        user_form = UsersForEditProfileForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(user.get_absolute_url())
    context = {
        'form': user_form,
        'form_user': user,
        'page_title': 'Редактор профиля пользователя',
        'bred_title': 'Редактор профиля пользователя'
    }
    return render(request, 'authapp/user_profile_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def project_user_update(request, pk):
    project_user = get_object_or_404(Users, pk=pk)
    project_user_form = UsersForProjectManagersForm(instance=project_user)
    InlineFormset = inlineformset_factory(Users, ProjectManagers, form=ProjectManagersForm, extra=1)
    formset = InlineFormset(instance=project_user)
    if request.method == 'POST':
        project_user_form = UsersForCompanyUsersForm(request.POST, instance=project_user)
        formset = InlineFormset(request.POST)
        if project_user_form.is_valid():
            updated_project_user_form = project_user_form.save(commit=False)
            formset = InlineFormset(request.POST, instance=updated_project_user_form)
            if formset.is_valid():
                updated_project_user_form.save()
                formset.save()
                return HttpResponseRedirect(updated_project_user_form.get_absolute_url())
    context = {
        'form': project_user_form,
        'formset': formset,
        'form_user': project_user,
        'page_title': 'Редактор проектов пользователя',
        'bred_title': 'Редактор проектов пользователя'
    }
    return render(request, 'authapp/user_profile_update.html', context)


def company_self_user_list(request, pk):
    user_companies_list = CompanyUsers.objects.filter(user_id=pk).order_by('-works')
    context = {
        'user_companies_list': user_companies_list,
        'page_title': 'Список компаний пользователя',
        'bred_title': 'Список компаний пользователя'
    }
    return render(request, 'authapp/self_list.html', context)


def company_user_list(request, pk):
    user = get_object_or_404(Users, pk=pk)
    user_companies_list = CompanyUsers.objects.filter(user_id=pk).order_by('-works')
    context = {
        'user_companies_list': user_companies_list,
        'user': user,
        'page_title': 'Список компаний пользователя',
        'bred_title': 'Список компаний пользователя'
    }
    return render(request, 'authapp/user_list.html', context)


def check_username(request):
    if request.method == 'GET':
        new_username = request.GET['username']
        user_names = Users.get_all_usernames()
        if not new_username:
            return HttpResponse("stay", content_type='text/html')
        elif new_username in user_names:
            return HttpResponse("no", content_type='text/html')
        else:
            return HttpResponse("ok", content_type='text/html')


def check_phone(request):
    if request.method == 'GET':
        new_phone = f"+{request.GET['phone']}".replace(' ', '')
        user_phones = Users.get_all_phones()
        if new_phone == '+7(___)___-__-__':
            return HttpResponse("stay", content_type='text/html')
        elif new_phone in user_phones:
            return HttpResponse("no", content_type='text/html')
        else:
            return HttpResponse("ok", content_type='text/html')


def check_email(request):
    if request.method == 'GET':
        try_email = request.GET['email']
        users_emails = Users.get_all_emails()
        if not try_email:
            return HttpResponse("stay", content_type='text/html')
        elif try_email in users_emails:
            return HttpResponse("ok", content_type='text/html')
        else:
            return HttpResponse("no", content_type='text/html')


class MyLoginView(LoginView):
    form_class = LoginForm


class MyPasswordResetView(PasswordResetView):
    form_class = MyPasswordResetForm
    extra_context = {
        'page_title': 'Сброс пароля',
        'bred_title': 'Сброс пароля'
    }
