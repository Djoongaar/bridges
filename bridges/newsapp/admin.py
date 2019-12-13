# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import *


class NewsProductInline(admin.TabularInline):
    model = NewsProduct
    extra = 0


class NewsDiscussItemInline(admin.TabularInline):
    model = NewsDiscussItem
    extra = 0


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name',)
    inlines = [
        NewsProductInline,
        NewsDiscussItemInline,
    ]
