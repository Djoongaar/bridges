from django.urls import path
from partnersapp import views as partnersapp

app_name = 'partnersapp'

urlpatterns = [
    path('', partnersapp.partners_list, name='partners_list'),
    path('partner/<int:pk>/', partnersapp.partner_detail, name='partner_detail'),
    path('partner/create/', partnersapp.partner_create, name='partner_create'),
    path('partner/delete/<int:pk>/', partnersapp.partner_delete, name='partner_delete'),
    path('partner/delete/confirm/<int:pk>/', partnersapp.partner_delete_confirm, name='partner_delete_confirm'),
    path('users/update/<int:pk>/', partnersapp.partner_user_update, name='partner_user_update'),
    path('search/', partnersapp.company_search, name='company_search'),

]
