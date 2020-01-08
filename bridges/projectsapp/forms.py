from django import forms
from django.core.exceptions import NON_FIELD_ERRORS

from .models import *


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = []


class ProjectUpdateForm(forms.ModelForm):
    DEVELOPMENT = 'разработка'
    EXPERTISE = 'экспертиза'
    TENDER = 'аукцион'
    EXECUTING = 'строительство'
    FINISHING = 'сдача'
    PAYMENT = 'выплата'
    DONE = 'завершен'
    STATUS_CHOICES = (
        (DEVELOPMENT, 'Статус проекта: разработка'),
        (EXPERTISE, 'Статус проекта: экспертиза'),
        (TENDER, 'Статус проекта: аукцион'),
        (EXECUTING, 'Статус проекта: строительство'),
        (FINISHING, 'Статус проекта: сдача'),
        (PAYMENT, 'Статус проекта: выплата'),
        (DONE, 'Статус проекта: завершен'),
    )
    name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': "Название проекта *",
        'tabindex': "1"
    }))
    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select(attrs={
        'placeholder': "Статус проекта *",
        'style': 'color: grey; border: 1px solid #eaeaea;',
        'tabindex': "2"
    }))
    city = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': "Город",
        'tabindex': "3"
    }))
    coordinate = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': "Координаты",
        'tabindex': "4"
    }))
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'placeholder': "Описание проекта",
        'rows': '5',
        'tabindex': "5"
    }))
    address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': "Адрес",
        'tabindex': "5"
    }))

    class Meta:
        model = Project
        fields = ['name', 'status', 'city', 'image', 'address', 'coordinate', 'description', 'is_active']


class ProjectSolutionsForm(forms.ModelForm):
    class Meta:
        model = ProjectHasTechnicalSolutions
        fields = ['techsol', 'name', 'value', 'is_active']


class ProjectImageForm(forms.ModelForm):
    class Meta:
        model = ProjectImage
        fields = ['image']


class ProjectManagerCreateForm(forms.ModelForm):
    project = forms.ModelChoiceField(queryset=Project.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = ProjectManagers
        fields = ['manager', 'role', 'is_active']


class ProjectCompanyCreateForm(forms.ModelForm):
    project = forms.ModelChoiceField(queryset=Project.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = ProjectCompany
        fields = ['company', 'role', 'is_active']


class ProjectSolutionsCreateForm(forms.ModelForm):
    project = forms.ModelChoiceField(queryset=Project.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = ProjectHasTechnicalSolutions
        fields = ['techsol', 'value', 'name', 'is_active']


class ProjectDiscussItemForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': "Ваш комментарий *",
        'rows': '5',
        'tabindex': "1"
    }))

    class Meta:
        model = ProjectDiscussItem
        fields = ['project', 'user', 'comment']
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
            }
        }
