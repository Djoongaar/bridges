from django.urls import path

from productsapp import views as productsapp
from productsapp.views import ProductsView, ProductRead

app_name = 'productsapp'

urlpatterns = [
    path('', ProductsView.as_view(), name='products'),
    # path('<slug:slug>', productsapp.product, name='product'),
    path('<int:pk>', ProductRead.as_view(), name='product'),
    path('product/<int:pk>', productsapp.product_update, name='product_update'),
    path('product/service/update/<int:pk>', productsapp.product_service_update, name='product_service_update'),
    path('product/work/update/<int:pk>', productsapp.product_work_update, name='product_work_update')
]
