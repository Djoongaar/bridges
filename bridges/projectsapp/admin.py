from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from .models import *


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 0


class ProjectHasTechnicalSolutionsInline(admin.TabularInline):
    model = ProjectHasTechnicalSolutions
    extra = 0


class ProjectCompanyInline(admin.TabularInline):
    model = ProjectCompany
    extra = 0


class ProjectManagersInline(admin.TabularInline):
    model = ProjectManagers
    extra = 0
    # fields = ('role', 'manager', 'is_active', 'description',)


class ProjectDiscussItemInline(admin.TabularInline):
    model = ProjectDiscussItem
    extra = 0


@admin.register(Project)
class ProjectAdmin(GuardedModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'city',)
    list_display_links = ('name', 'city',)
    search_fields = ('name',)
    exclude = ['map_mark']
    inlines = [
        ProjectManagersInline,
        ProjectCompanyInline,
        ProjectHasTechnicalSolutionsInline,
        ProjectImageInline,
        ProjectDiscussItemInline
    ]


@admin.register(ProjectHasTechnicalSolutions)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)


@admin.register(ProjectManagers)
class ProjectManagersAdmin(admin.ModelAdmin):
    list_display = ('manager',)
    list_display_links = ('manager',)


@admin.register(ProjectCompany)
class ProjectCompanyAdmin(admin.ModelAdmin):
    list_display = ('company',)
    list_display_links = ('company',)
