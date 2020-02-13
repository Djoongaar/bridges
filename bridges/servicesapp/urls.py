from django.urls import path
from servicesapp import views as servicesapp

app_name = 'servicesapp'

urlpatterns = [
    path('all/', servicesapp.services_list, name='services_list'),
    path('single/<int:pk>/', servicesapp.services_single, name='services_single'),
]
