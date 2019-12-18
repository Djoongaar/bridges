from django import forms
from productsapp.models import TechnicalSolutions, TechnicalSolutionsHasService, ProductWork


class ProductForm(forms.ModelForm):
    class Meta:
        model = TechnicalSolutions
        fields = []


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = TechnicalSolutions
        fields = ['name', 'short_desc', 'description', 'image', 'is_active']


class TechSolHasServiceForm(forms.ModelForm):
    class Meta:
        model = TechnicalSolutionsHasService
        exclude = ()


class ProductWorkForm(forms.ModelForm):
    class Meta:
        model = ProductWork
        fields = ['work', 'material', 'price']
