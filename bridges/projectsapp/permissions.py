# from rest_framework import permissions
#
# from projectsapp.models import Project
#
#
# class CanChangeOrReadOnly(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj, **kwargs):
#         project = Project.objects.get(pk=kwargs['pk'])
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         elif request.user.has_perm('change_project', project):
#             return True
#         else:
#             return False
