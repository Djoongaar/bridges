from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('mainapp.urls', namespace='main')),
    path('contact/', include('contactapp.urls', namespace='contact')),
    path('products/', include('productsapp.urls', namespace='products')),
    path('projects/', include('projectsapp.urls', namespace='projects')),
    path('map/', include('ymapapp.urls', namespace='ymap')),
    path('admin/', admin.site.urls),
    path('research/', include('researchapp.urls', namespace='research')),
    path('auth/', include('authapp.urls')),
    path('partners/', include('partnersapp.urls', namespace='partners')),
    path('services/', include('servicesapp.urls', namespace='services')),
    path('orders/', include('ordersapp.urls', namespace='orders')),
    # path('news/', include('newsapp.urls', namespace='news')),
    url(r'^accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
