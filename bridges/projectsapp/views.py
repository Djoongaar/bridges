from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.forms import inlineformset_factory, modelformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from projectsapp.serializers import ProjectDetailSerializer, ProjectListSerializer, ProjectCommentSerializer, \
    CommentCreateSerializer
from projectsapp.utils import CreateMixin, DeleteMixin
from .forms import *
from projectsapp.models import ProjectImage, ProjectManagers
from django.views.generic import View
from django.views.generic import ListView, CreateView
from projectsapp.models import Project, ProjectHasTechnicalSolutions, ProjectCompany
from authapp.models import Users
from django.http import HttpResponseRedirect, Http404

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


class ProjectRead(View):
    form_model = ProjectDiscussItem
    form = ProjectDiscussItemForm
    template = 'projectsapp/project_detail.html'

    def get(self, request, pk):
        project = Project.objects.get(pk=pk)
        user = request.user
        report_form = ProjectDiscussItemForm(initial={'project': project, 'user': user})
        context = {
            'form': report_form,
            'object': project,
            'page_title': 'Информация о проекте',
            'bred_title': 'О проекте'
        }
        return render(request, template_name=self.template, context=context)

    def post(self, request, pk):
        project = Project.objects.get(pk=pk)
        user = request.user
        report_form = ProjectDiscussItemForm(data=request.POST)
        if report_form.is_valid():
            new_report_form = report_form.save(commit=False)
            new_report_form.project = project
            new_report_form.user = user
            new_report_form.save()
            return redirect(project.get_absolute_url())


class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectUpdateForm
    template_name = 'projectsapp/project_create.html'
    extra_context = {
        'page_title': 'Создать новый проект',
        'bred_title': 'Новый проект'
    }


def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.user.has_perm('change_project', project):
        form = ProjectUpdateForm(instance=project)
        if request.method == 'POST':
            form = ProjectUpdateForm(request.POST, request.FILES, instance=project)
            if form.is_valid():
                form.save()
                print(request.POST)
                return HttpResponseRedirect(project.get_absolute_url())
        context = {
            'form': form,
            'page_title': 'Редактирование основной информации',
            'bred_title': 'Обновление проекта',
            'project': project,
        }
        return render(request, 'projectsapp/project_create.html', context)
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


#  ------------------------------------ COMMENTS TO THE PROJECT crUd ---------------------------------------------


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


class CommentDeleteView(DeleteMixin, View):
    form_model = ProjectDiscussItem
    template = 'projectsapp/projectitems_confirm_delete.html'
    page_title = 'Удаление комментария'
    bred_title = 'Комментарий'


#  ------------------------------------ REST FRAMEWORK API ---------------------------------------------


class ProjectListAPI(generics.ListAPIView):
    serializer_class = ProjectListSerializer

    def get_queryset(self):
        user = self.request.user
        print(user)
        return Project.objects.all()
        # if user.is_superuser:
        #     return Project.objects.all()
        # elif user.is_authenticated:
        #     projects = self.request.user.get_projects()
        #     users_projects = [i.project.pk for i in projects]
        #     return Project.objects.filter(
        #         Q(status__iexact="завершен") |
        #         Q(pk__in=users_projects)
        #     )
        # else:
        #     return Project.objects.filter(
        #         Q(status__iexact="завершен"),
        #         Q(is_active=True)
        #     )


class ProjectDetailAPI(generics.RetrieveAPIView):
    serializer_class = ProjectDetailSerializer

    def get_queryset(self):
        user = self.request.user
        print(user)
        return Project.objects.all()
        # if user.is_superuser:
        #     return Project.objects.all()
        # elif user.is_authenticated:
        #     projects = user.get_projects()
        #     users_projects = [i.project.pk for i in projects]
        #     return Project.objects.filter(
        #         Q(status__iexact="завершен") |
        #         Q(pk__in=users_projects)
        #     )
        # else:
        #     return Project.objects.filter(
        #         Q(status__iexact="завершен"),
        #         Q(is_active=True)
        #     )


class ProjectCreateAPI(generics.CreateAPIView):
    serializer_class = ProjectDetailSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ProjectUpdateDestroyAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectDetailSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        print(user)
        if user.is_superuser:
            return Project.objects.all()
        else:
            projects = user.get_projects()
            users_projects = [i.project.pk for i in projects]
            return Project.objects.filter(pk__in=users_projects)


class CommentListAPI(generics.ListAPIView):
    serializer_class = ProjectCommentSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return ProjectDiscussItem.objects.filter(project__pk=self.kwargs['pk'])


class CommentCreateAPI(generics.CreateAPIView):
    serializer_class = CommentCreateSerializer
    permission_classes = (IsAuthenticated,)


class CommentUpdateDestroyAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentCreateSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return ProjectDiscussItem.objects.all()
        else:
            return ProjectDiscussItem.objects.filter(user__pk=user.pk)

