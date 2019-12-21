from django.shortcuts import render
from django.views.decorators.cache import cache_page

from productsapp.models import TechnicalSolutions
from projectsapp.models import Project


@cache_page(3600)
def index(request):
    latest_projects = Project.objects.all().order_by('-updated')[:6]
    products = TechnicalSolutions.objects.all()
    context = {
        'latest_projects': latest_projects,
        'products': products,
        'page_title': 'Мосты ТемпСтройСистемы',
        'bred_title': 'Мосты ТемпСтройСистемы'
    }
    return render(request, 'mainapp/index.html', context)


