from django.contrib.auth.decorators import user_passes_test, login_required
from django.db.models import Q
from django.forms import inlineformset_factory, modelformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from guardian.decorators import permission_required_or_403
from projectsapp.utils import CreateMixin, DeleteMixin
from .forms import *
from projectsapp.models import ProjectImage, ProjectManagers
from django.views.generic import View
from django.views.generic import ListView, DetailView, CreateView
from projectsapp.models import Project, ProjectHasTechnicalSolutions, ProjectCompany
from authapp.models import Users

from django.http import HttpResponseRedirect, Http404

from django.urls import reverse_lazy

#  ------------------------------------ PROJECT'S CRUD ----------------------------------------------


class ProjectsList(ListView):
    """docstring for ProductList"""
    paginate_by = 6
    model = Project
    template_name = 'projectsapp/grid.html'
    extra_context = {}

    def get_queryset(self):
        if self.request.user.is_staff:
            return Project.objects.all()
        else:
            return Project.objects.filter(status__iexact='завершен')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = TechnicalSolutions.objects.all()
        values = ProjectHasTechnicalSolutions.objects.all()
        context.update({'products': products,
                        'values': values,
                        'page_title': 'Проекты компании',
                        'bred_title': 'Проекты компании'
                        })
        return context


class ProjectRead(DetailView):
    model = Project
    extra_context = {}    
    not_empty_url = reverse_lazy('projects:project')

    def get_queryset(self):
        if self.request.user.is_staff:
            return Project.objects.all()
        else:
            return Project.objects.filter(status__exact='завершен')

    def get_context_data(self, **kwargs):
        context = super(ProjectRead, self).get_context_data(**kwargs)
        context.update({'page_title': 'Детальная информация о проекте',
                        'bred_title': 'Информация о проекте'
                        })
        return context


class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectUpdateForm
    template_name = 'projectsapp/gallery_update.html'
    extra_context = {
        'page_title': 'Создать новый проект',
        'bred_title': 'Новый проект'
    }


def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.user.has_perm('change_project', project):
        project_form = ProjectUpdateForm(instance=project)
        if request.method == 'POST':
            project_form = ProjectUpdateForm(request.POST, request.FILES, instance=project)
            if project_form.is_valid():
                project_form.save()
                return HttpResponseRedirect(project.get_absolute_url())
        context = {
            'project_form': project_form,
            'page_title': 'Редактирование основной информации',
            'bred_title': 'Обновление проекта',
            'project': project,
        }
        return render(request, 'projectsapp/gallery_update.html', context)
    else:
        raise Http404


#  ------------------------------------ PROJECT'S SOLUTIONS CRUD ----------------------------------------------


class ProjectsSolutionsCreateView(CreateMixin, View):
    form_model = ProjectHasTechnicalSolutions
    form = ProjectSolutionsCreateForm
    template = 'projectsapp/projectitems_form.html'
    FormSet = modelformset_factory(form_model, fields='__all__')
    variable = 'techsol'
    viriable_model = TechnicalSolutions
    page_title = 'Добавление технического решения'
    bred_title = 'Техническое решение'


class ProjectsSolutionsDeleteView(DeleteMixin, View):
    form_model = ProjectHasTechnicalSolutions
    template = 'projectsapp/projectitems_confirm_delete.html'
    page_title = 'Удаление технического решения'
    bred_title = 'Техническое решение'


#  ------------------------------------ PROJECT'S COMPANIES CruD ----------------------------------------------


class ProjectsCompanyCreateView(CreateMixin, View):
    form_model = ProjectCompany
    form = ProjectCompanyCreateForm
    template = 'projectsapp/projectitems_form.html'
    FormSet = modelformset_factory(form_model, fields='__all__')
    variable = 'company'
    viriable_model = Company
    page_title = 'Добавление контрагента проекта'
    bred_title = 'Контрагент проекта'


class ProjectsCompanyDeleteView(DeleteMixin, View):
    form_model = ProjectCompany
    template = 'projectsapp/projectitems_confirm_delete.html'
    page_title = 'Удаление контрагента проекта'
    bred_title = 'Контрагент проекта'


#  ------------------------------------ PROJECT'S MANAGERS CruD ----------------------------------------------

class ProjectsManagerCreateView(CreateMixin, View):
    form_model = ProjectManagers
    form = ProjectManagerCreateForm
    template = 'projectsapp/projectitems_form.html'
    FormSet = modelformset_factory(form_model, fields='__all__')
    variable = 'manager'
    viriable_model = Users
    page_title = 'Добавление участника проекта'
    bred_title = 'Участник проекта'


class ProjectsManagerDeleteView(DeleteMixin, View):
    form_model = ProjectManagers
    template = 'projectsapp/projectitems_confirm_delete.html'
    page_title = 'Удаление участника проекта'
    bred_title = 'Участник проекта'


#  ------------------------------------ PROJECT'S GALLERY crUd----------------------------------------------


def gallery_update(request, pk):
    project = Project.objects.get(pk=pk)
    if request.user.has_perm('change_project', project):
        project_form = ProjectForm(instance=project)
        BookInlineFormSet = inlineformset_factory(Project, ProjectImage, form=ProjectImageForm, extra=3)
        formset = BookInlineFormSet(instance=project)
        if request.method == "POST":
            project_form = ProjectForm(request.POST, instance=project)
            formset = BookInlineFormSet(request.POST, request.FILES)
            if project_form.is_valid():
                created_project = project_form.save(commit=False)
                formset = BookInlineFormSet(request.POST, request.FILES, instance=created_project)
                if formset.is_valid():
                    created_project.save()
                    formset.save()
                    return HttpResponseRedirect(created_project.get_absolute_url())
        context = {
            'project_form': project_form,
            'formset': formset,
            'page_title': 'Добавление фотографий',
            'bred_title': 'Добавление фотографий',
            'project': project
        }
        return render(request, "projectsapp/gallery_update.html", context)
    else:
        raise Http404


#  ------------------------------------ PROJECT'S GALLERY crUd----------------------------------------------

@login_required
def project_discuss_items(request, pk):
    """ добавление сообщения """
    project = Project.objects.get(pk=pk)
    user = request.user
    if request.method == 'POST':
        report_form = ProjectDiscussItemForm(data=request.POST)
        if report_form.is_valid():
            new_report_form = report_form.save(commit=False)
            new_report_form.project = project
            new_report_form.user = user
            new_report_form.save()
            return redirect(project.get_absolute_url())
    else:
        report_form = ProjectDiscussItemForm(initial={
            'project': project,
            'user': user
        })
    context = {
        'project': project,
        'user': user,
        'form': report_form,
        'page_title': 'Комментарий',
        'bred_title': 'Комментарии',
    }
    return render(request, 'projectsapp/project_discuss_detail.html', context)


@login_required
def comment_update(request, comment_pk):
    """ updating comments """
    comment = ProjectDiscussItem.objects.get(pk=comment_pk)
    if request.user.is_superuser or comment.user == request.user:
        if request.method == 'POST':
            report_form = ProjectDiscussItemForm(data=request.POST, instance=comment)
            if report_form.is_valid():
                new_report_form = report_form.save(commit=False)
                new_report_form.project = comment.project
                new_report_form.user = comment.user
                new_report_form.save()
                return redirect(comment.project.get_absolute_url())
        else:
            report_form = ProjectDiscussItemForm(initial={
                'project': comment.project,
                'user': comment.user,
                'comment': comment.comment
            })
        context = {
            'project': comment.project,
            'user': comment.user,
            'form': report_form,
            'page_title': 'Комментарий',
            'bred_title': 'Комментарии',
        }
        return render(request, 'projectsapp/project_discuss_detail.html', context)


# @login_required
# def comment_delete(request, comment_pk):
#     """ deleting comments """
#     comment = ProjectDiscussItem.objects.get(pk=comment_pk)
#     if comment.user == request.user:
#         comment.delete()
#     else:
#         raise Http404
#     context = {
#         'page_title': 'Комментарий',
#         'bred_title': 'Комментарии',
#     }
#     return render(request, 'projectsapp/projectitems_confirm_delete.html', context)


class CommentDeleteView(DeleteMixin, View):
    form_model = ProjectDiscussItem
    template = 'projectsapp/projectitems_confirm_delete.html'
    page_title = 'Удаление комментария'
    bred_title = 'Комментарий'
