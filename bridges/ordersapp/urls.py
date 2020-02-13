from django.urls import path
from ordersapp import views as ordersapp

app_name = 'ordersapp'

urlpatterns = [
    path('order/create/<int:pk>/', ordersapp.order_create, name='order_create'),
    path('order/create/', ordersapp.order_create_no_product, name='order_create_no_product'),
    # path('order/list', ordersapp.order_create, name='order_create'),
]
