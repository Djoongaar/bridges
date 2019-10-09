from django.contrib import admin
from .models import Users, CategoryCompany, Company, FormCompany


# Register your models here.

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    # поля, которые не нужно редактировать в админке
    readonly_fields = ('password', 'is_superuser', 'last_login', 'date_joined')  # 'user_permissions', 'groups')

    # какие поля выводить в админке
    list_display = ('username', 'first_name', 'last_name', 'is_staff', 'is_active', 'phone', 'email')

    # по каким полям может осуществляться поиск в админке
    search_fields = ('username',
                     'first_name',
                     'last_name',
                     'patronymic',
                     'company',
                     'position',
                     'project',
                     'phone',
                     'email',)

    # укажем быстрые фильтры для фильтрации записей
    list_filter = ('is_staff', 'is_active', 'gender', 'company', 'city')

    # в админке поля формы можно группировать
    fieldsets = (
        ('Личные данные',
         {'fields': ('username', 'password', 'first_name', 'last_name', 'patronymic', 'gender', 'birthday')}),
        ('Контактные данные', {'fields': ('phone', 'email')}),
        ('Данные сотрудника',
         {'fields': ('is_staff', 'is_active', 'company', 'groups', 'position', 'project',)}),
    )


@admin.register(FormCompany)
class CategoryCompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description',)


@admin.register(CategoryCompany)
class CategoryCompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description',)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'inn', 'city', 'logo')
    search_fields = ('name_company',
                     'short_name',
                     'form_company',
                     'logo',
                     'category',
                     'inn',
                     'city',
                     'address',
                     'phone',
                     'email',)
    # укажем быстрые фильтры для фильтрации записей
    list_filter = ('category', 'city')
