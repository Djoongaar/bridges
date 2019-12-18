from django.contrib import admin
from .models import *


# -----------------------    МОДЕЛИ МАТЕРИАЛОВ   -------------------------------------


class MaterialCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name', )

    class Meta:
        model = MaterialCategory


admin.site.register(MaterialCategory, MaterialCategoryAdmin)


class MeasureTypesAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name',)

    class Meta:
        model = MeasureTypes


admin.site.register(MeasureTypes, MeasureTypesAdmin)


class MaterialImageInline(admin.TabularInline):
    model = MaterialImage
    extra = 0


class MaterialAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'category', 'measure',)
    list_display_links = ('name',)
    search_fields = ('name',)
    inlines = [MaterialImageInline]

    class Meta:
        model = Material


admin.site.register(Material, MaterialAdmin)


class MaterialImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'is_active', 'created', 'updated',)
    list_display_links = ('id', 'image',)

    class Meta:
        model = MaterialImage


admin.site.register(MaterialImage, MaterialImageAdmin)


class ProductMaterialAdmin(admin.ModelAdmin):
    list_display = ('pk', 'product',)
    list_display_links = ('product',)
    search_fields = ('product', )

    class Meta:
        model = ProductMaterial


admin.site.register(ProductMaterial, ProductMaterialAdmin)


# -----------------------    МОДЕЛИ РАБОТ   -------------------------------------


class WorkCategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name',)
    list_display_links = ('name',)
    search_fields = ('name', )

    class Meta:
        model = WorkCategory


admin.site.register(WorkCategory, WorkCategoryAdmin)


class WorkImageInline(admin.TabularInline):
    model = WorkImage
    extra = 0


class ProductWorkInline(admin.TabularInline):
    model = ProductWork
    extra = 0


class WorkAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'measure',)
    list_display_links = ('name',)
    search_fields = ('name',)
    inlines = [WorkImageInline]

    class Meta:
        model = Material


admin.site.register(Work, WorkAdmin)


class WorkImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'is_active', 'created', 'updated',)
    list_display_links = ('id', 'image',)

    class Meta:
        model = WorkImage


admin.site.register(WorkImage, WorkImageAdmin)


class ProductWorkAdmin(admin.ModelAdmin):
    list_display = ('pk', 'product',)
    list_display_links = ('product',)
    search_fields = ('product', )

    class Meta:
        model = ProductWork


admin.site.register(ProductWork, ProductWorkAdmin)


# -----------------------    МОДЕЛИ ПРОДУКТОВ (ТЕХНИЧЕСКИХ РЕШЕНИЙ)   -------------------------------------


class TechnicalSolutionsImageInline(admin.TabularInline):
    model = TechnicalSolutionsImage
    extra = 0


class ProductServicesInline(admin.TabularInline):
    model = TechnicalSolutionsHasService
    extra = 0


class TechnicalSolutionsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', )
    list_display_links = ('name',)
    search_fields = ('name',)
    inlines = [TechnicalSolutionsImageInline, ProductWorkInline, ProductServicesInline]

    class Meta:
        model = TechnicalSolutions


admin.site.register(TechnicalSolutions, TechnicalSolutionsAdmin)


class TechnicalSolutionsImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'is_active', 'created', 'updated',)
    list_display_links = ('id', 'image',)

    class Meta:
        model = TechnicalSolutionsImage


admin.site.register(TechnicalSolutionsImage, TechnicalSolutionsImageAdmin)

