# Generated by Django 2.2 on 2019-11-04 08:58

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=50, unique=True, verbose_name='Логин*')),
                ('first_name', models.CharField(max_length=50, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('patronymic', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='Отчество')),
                ('avatar', models.ImageField(blank=True, default='users/avatar/no_avatar.png', upload_to='users/avatar', verbose_name='Аватар')),
                ('description', models.TextField(blank=True, max_length=5000, verbose_name='Подробно о себе')),
                ('gender', models.CharField(blank=True, choices=[(None, 'не указан'), ('male', 'муж'), ('female', 'жен')], max_length=6, null=True, verbose_name='Пол')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='День рождения')),
                ('phone', models.CharField(default='не указан', max_length=50, verbose_name='Телефон*')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'users',
                'ordering': ['-date_joined'],
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='CategoryCompany',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Категория компании*')),
                ('description', models.CharField(blank=True, default='', max_length=300, null=True, verbose_name='Описание категории')),
            ],
            options={
                'verbose_name': 'Категорию компании',
                'verbose_name_plural': 'Категории компаний',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70, verbose_name='Полное название*')),
                ('short', models.CharField(blank=True, max_length=30, null=True, verbose_name='Короткое название')),
                ('logo', models.ImageField(blank=True, default='logo_company/no_logo.jpg', null=True, upload_to='logo_company', verbose_name='Логотип')),
                ('inn', models.BigIntegerField(unique=True, verbose_name='ИНН*')),
                ('city', models.CharField(blank=True, default='', max_length=30, null=True, verbose_name='Город')),
                ('address', models.CharField(blank=True, default='', max_length=300, null=True, verbose_name='Адрес')),
                ('phone', models.CharField(blank=True, default='', max_length=30, null=True, verbose_name='Телефон')),
                ('email', models.CharField(blank=True, default='', max_length=30, null=True, verbose_name='Эл. почта')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='authapp.CategoryCompany', verbose_name='Категория компании*')),
            ],
            options={
                'verbose_name': 'Новую компанию',
                'verbose_name_plural': 'Компании',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='FormCompany',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='Форма компании*')),
                ('description', models.CharField(blank=True, default='', max_length=300, null=True, verbose_name='Описание формы')),
            ],
            options={
                'verbose_name': 'Форму компании',
                'verbose_name_plural': 'Формы компаний',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='CompanyUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(blank=True, max_length=50, verbose_name='Должность')),
                ('works', models.BooleanField(default=True, null=True, verbose_name='Работает в компании')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='authapp.Company', verbose_name='Компания')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='company', to=settings.AUTH_USER_MODEL, verbose_name='Сотрудник')),
            ],
            options={
                'verbose_name': 'Компания - работодатель',
                'verbose_name_plural': 'Компании - работодатели',
            },
        ),
        migrations.AddField(
            model_name='company',
            name='form',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='authapp.FormCompany', verbose_name='Форма'),
        ),
    ]
