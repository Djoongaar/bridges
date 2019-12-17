from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404

from authapp.models import Users
from projectsapp.models import Project


class ObjectCreateMixin:
    form_model = None
    template = None

    def get(self, request):
        form = self.form_model()
        return render(request, self.template, context={'form': form})

    def post(self, request):
        bound_form = self.form_model(request.POST)
        if bound_form.is_valid():
            bound_form.save()
            return redirect('projectsapp:projects')
        return render(request, self.template, context={'form': bound_form})


class CreateMixin:
    form_model = None
    form = None
    template = None
    variable = None
    viriable_model = None
    page_title = None
    bred_title = None

    def get(self, request, project_pk):
        project = Project.objects.get(pk=project_pk)
        if request.user.has_perm('change_project', project):
            form = self.form(initial={
                'project': project,
                f'{self.variable}': self.variable
            })
            context = {
                'form': form,
                'project': project,
                'page_title': self.page_title,
                'bred_title': self.bred_title
            }
            return render(request, template_name=self.template, context=context)
        else:
            raise Http404

    def post(self, request, project_pk):
        project = Project.objects.get(pk=project_pk)
        form = self.form(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.project = project
            obj.variable = self.variable
            obj.save()
            return HttpResponseRedirect(project.get_absolute_url())
        return HttpResponse(status=400)


class DeleteMixin:
    form_model = None
    template = None
    page_title = None
    bred_title = None

    def get(self, request, project_pk, pk):
        project = Project.objects.get(pk=project_pk)
        obj = get_object_or_404(self.form_model, pk=pk)
        if request.user.has_perm('change_project', project) or obj.user == request.user:
            context = {
                'obj': obj,
                'project': project,
                'page_title': self.page_title,
                'bred_title': self.bred_title
            }
            return render(request, self.template, context=context)
        else:
            raise Http404

    def post(self, request, project_pk, pk):
        item = get_object_or_404(self.form_model, pk=pk)
        project = item.project
        item.delete()
        return HttpResponseRedirect(project.get_absolute_url())
