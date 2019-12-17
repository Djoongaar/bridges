from django.urls import path
from projectsapp import views as projectsapp
from .views import ProjectsList, ProjectRead, ProjectCreateView

# from .views import ProjectsList, ProjectRead, ProductManagersUpdate

app_name = 'projectsapp'

urlpatterns = [
    path('', ProjectsList.as_view(), name='projects'),
    path('<int:pk>', ProjectRead.as_view(), name='project'),
    path('create', ProjectCreateView.as_view(), name='project_create'),
    path('update/<int:pk>', projectsapp.project_update, name='project_update'),
    path('product/create/<int:project_pk>', projectsapp.ProjectsSolutionsCreateView.as_view(), name='product_create'),
    path('product/delete/<int:project_pk>/<int:pk>', projectsapp.ProjectsSolutionsDeleteView.as_view(), name='product_delete'),
    path('company/create/<int:project_pk>', projectsapp.ProjectsCompanyCreateView.as_view(), name='company_create'),
    path('company/delete/<int:project_pk>/<int:pk>', projectsapp.ProjectsCompanyDeleteView.as_view(), name='company_delete'),
    path('manager/create/<int:project_pk>', projectsapp.ProjectsManagerCreateView.as_view(), name='manager_create'),
    path('manager/delete/<int:project_pk>/<int:pk>', projectsapp.ProjectsManagerDeleteView.as_view(), name='manager_delete'),
    path('gallery/update/<int:pk>', projectsapp.gallery_update, name='gallery_update'),
    path('discuss/items/<int:pk>', projectsapp.project_discuss_items, name='project_discuss_items'),
]
