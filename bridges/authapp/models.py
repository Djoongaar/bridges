import datetime

from django.contrib import admin
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.urls import reverse
from guardian.shortcuts import assign_perm
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFill


def image_upload_to(instance, filename):
    return 'users/images/user_{0}/{1}'.format(instance.pk, filename)


class CategoryCompany(models.Model):
    """ модель содержит информацию о категории компании,
    например: проектный институт, подрядная организация, заказчик и др. """
    name = models.CharField(verbose_name='Категория компании*', max_length=50, unique=True)
    description = models.CharField(verbose_name='Описание категории', max_length=300, default='', null=True, blank=True)

    class Meta:
        verbose_name = "Категорию компании"
        verbose_name_plural = "Категории компаний"
        ordering = ["name"]

    def __str__(self):
        return self.name.title()


class FormCompany(models.Model):
    """ модель содержит организационно-правовые формы предприятия,
    например, ООО, ИП, ОАО, ЗАО и др. """
    name = models.CharField(verbose_name='Форма компании*', max_length=30, unique=True)
    description = models.CharField(verbose_name='Описание формы', max_length=300, default='', null=True, blank=True)

    class Meta:
        verbose_name = "Форму компании"
        verbose_name_plural = "Формы компаний"
        ordering = ["name"]

    def __str__(self):
        return self.name.upper()


class Company(models.Model):
    """модель содержит подробную информацию о компании"""

    name = models.CharField(verbose_name='Полное название*', max_length=70)
    short = models.CharField(verbose_name='Короткое название', max_length=30, blank=True, null=True)
    form = models.ForeignKey(FormCompany, on_delete=models.PROTECT, verbose_name='Форма', blank=True, null=True)
    category = models.ForeignKey(CategoryCompany, on_delete=models.PROTECT, verbose_name='Категория компании*')
    logo = models.ImageField(verbose_name='Логотип', upload_to='logo_company', default='logo_company/no_logo.jpg',
                             blank=True, null=True)
    inn = models.BigIntegerField(verbose_name='ИНН*', unique=True)
    city = models.CharField(verbose_name='Город', max_length=30, default='', null=True, blank=True)
    address = models.CharField(verbose_name='Адрес', max_length=300, default='', null=True, blank=True)
    phone = models.CharField(verbose_name='Телефон', max_length=30, default='', null=True, blank=True)
    email = models.CharField(verbose_name='Эл. почта', max_length=30, default='', null=True, blank=True)
    created = models.DateTimeField(verbose_name='создан', auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(verbose_name='обновлен', auto_now=True)

    class Meta:
        verbose_name = "Новую компанию"
        verbose_name_plural = "Компании"
        ordering = ["name"]

    def __str__(self):
        return self.name.title()

    def get_absolute_url(self):
        return reverse('partners:partner_detail', args=[str(self.id)])

    def get_employees(self):
        return self.employees.select_related()


class Users(AbstractUser):
    """ модель содержит информацию о всех пользователях, включая superuser, сотрудников компании
    и простых пользователей.
    У AbstractUser есть поля: password, last_login, first_name, last_name, email, is_superuser, is_staff,
    # is_active и date_joined.
    Создадим дополнительные поля. """
    GENDER_CHOICES = (
        (None, 'не указан'),
        ('male', 'муж'),
        ('female', 'жен'),
    )
    username = models.CharField(verbose_name='Логин*', max_length=50, unique=True)  # переопределили из-за verbose_name
    first_name = models.CharField(verbose_name='Имя', max_length=50)
    patronymic = models.CharField(verbose_name='Отчество', max_length=50, default='', null=True, blank=True)
    last_name = models.CharField(verbose_name='Фамилия', max_length=50)
    avatar = ProcessedImageField(verbose_name='Аватар', upload_to=image_upload_to, processors=[ResizeToFill(462, 462)],
                                 blank=True)
    # avatar = models.ImageField(verbose_name='Аватар', upload_to=image_upload_to, blank=True)
    description = models.TextField(verbose_name='Подробно о себе', max_length=5000, blank=True)
    gender = models.CharField(verbose_name='Пол', max_length=6, choices=GENDER_CHOICES, blank=True, null=True)
    birthday = models.DateField(verbose_name='День рождения', blank=True, null=True)
    phone = models.CharField(verbose_name='Телефон*', max_length=50, default='не указан')
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    social_media_image = models.ImageField(upload_to=image_upload_to, blank=True)

    class Meta(AbstractUser.Meta):
        verbose_name = "Пользователь"
        ordering = ['-date_joined']
        default_permissions = ('add', 'change', 'delete')

    def get_self_absolute_url(self):
        return reverse('restricted_area')

    def get_absolute_url(self):
        return reverse('user_profile', args=[str(self.id)])

    def get_company(self):
        return self.company.select_related()

    def get_projects(self):
        return self.projects.select_related()


    # def get_last_login(self):
    #     login_l = datetime.datetime.now() - self.last_login
    #     if login_l < 600:

    def __str__(self):
        if self.patronymic:
            return str(f"{self.last_name} {self.first_name} {self.patronymic}")
        else:
            return str(f"{self.last_name} {self.first_name}")

    @staticmethod
    def get_all_usernames():
        users = []
        for user in Users.objects.all():
            users.append(user.username)
        return users

    @staticmethod
    def get_all_phones():
        phones = []
        for user in Users.objects.all():
            phones.append(user.phone)
        return phones

    @staticmethod
    def get_all_emails():
        emails = []
        for user in Users.objects.all():
            emails.append(user.email)
        return emails


def user_post_save(sender, instance, created, **kwargs):
    """
    Дает права на изменение профиля проекта после появление менеджера в связанной модели.
    """
    users = instance
    if Users:
        assign_perm('authapp.change_users', users, users)


post_save.connect(user_post_save, sender=Users)


class CompanyUsers(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT, verbose_name='Компания', related_name='employees')
    user = models.ForeignKey(Users, on_delete=models.PROTECT, verbose_name='Сотрудник', related_name='company')
    position = models.CharField(verbose_name='Должность', max_length=50, blank=True)
    works = models.BooleanField(verbose_name='Работает в компании', default=True, null=True)

    class Meta:
        verbose_name = 'Компания - работодатель'
        verbose_name_plural = 'Компании - работодатели'
