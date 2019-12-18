from django.contrib.auth.decorators import user_passes_test
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from productsapp.forms import ProductUpdateForm, ProductForm, TechSolHasServiceForm, ProductWorkForm
from django.views.generic import ListView
from productsapp.models import TechnicalSolutions, TechnicalSolutionsHasService, ProductWork
from researchapp.models import Document
from servicesapp.models import Service


class ProductsView(ListView):
    template_name = 'productsapp/products.html'
    context_object_name = 'all_products'
    extra_context = {
        'page_title': 'Технические решения для транспортного строительства',
        'bred_title': 'Технические решения'
    }

    def get_queryset(self):
        return TechnicalSolutions.objects.all().order_by('pk').filter(is_active=True)


def product(request, slug):
    item = get_object_or_404(TechnicalSolutions, slug=slug)
    docs = Document.objects.filter(techsol__pk=item.pk)
    publications = docs.filter(type_id=5)
    researches = docs.filter(type__in=(2, 3,))
    documents = docs.filter(type__id=1)
    product_services = Service.objects.filter(technicalsolutionshasservice__technicalsolutions__slug=slug)
    feedback = docs.filter(type__id=4).order_by('pk')
    if request.user.is_staff:
        projects = item.get_projects()
    else:
        projects = item.get_projects().filter(project__status='завершен')

    content = {
        'projects': projects,
        'works': item.get_works(),
        'materials': item.get_materials(),
        'page_title': item,
        'bred_title': item,
        'product': item,
        'researches': researches,
        'documents': documents,
        'feedback': feedback,
        'publications': publications,
        'product_services': product_services,
    }
    return render(request, 'productsapp/product.html', content)


@user_passes_test(lambda u: u.is_superuser)
def product_update(request, slug):
    product = get_object_or_404(TechnicalSolutions, slug=slug)
    product_form = ProductUpdateForm(instance=product)
    if request.method == 'POST':
        product_form = ProductUpdateForm(request.POST, request.FILES, instance=product)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(product.get_absolute_url())
    context = {
        'product_form': product_form,
        'page_title': 'Обновление технических решений',
        'bred_title': 'Обновление техрешений',
        'product': product
    }
    return render(request, 'productsapp/product_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_service_update(request, slug):
    product = get_object_or_404(TechnicalSolutions, slug=slug)
    product_form = ProductForm(instance=product)
    product_formset = inlineformset_factory(TechnicalSolutions, TechnicalSolutionsHasService, form=TechSolHasServiceForm,
                                            extra=1)
    formset = product_formset(instance=product)
    if request.method == 'POST':
        product_form = ProductForm(request.POST, instance=product)
        formset = product_formset(request.POST)
        if product_form.is_valid():
            updated_product = product_form.save(commit=False)
            formset = product_formset(request.POST, instance=updated_product)
            if formset.is_valid():
                updated_product.save()
                formset.save()
                return HttpResponseRedirect(updated_product.get_absolute_url())
    context = {
        'product_form': product_form,
        'formset': formset,
        'product': product,
        'page_title': 'Обновление технических решений',
        'bred_title': 'Обновление техрешений',
    }
    return render(request, 'productsapp/product_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_work_update(request, slug):
    product = get_object_or_404(TechnicalSolutions, slug=slug)
    product_form = ProductForm(instance=product)
    product_formset = inlineformset_factory(TechnicalSolutions, ProductWork, form=ProductWorkForm,
                                            extra=1)
    formset = product_formset(instance=product)
    if request.method == 'POST':
        product_form = ProductForm(request.POST, instance=product)
        formset = product_formset(request.POST)
        if product_form.is_valid():
            updated_product = product_form.save(commit=False)
            formset = product_formset(request.POST, instance=updated_product)
            if formset.is_valid():
                updated_product.save()
                formset.save()
                return HttpResponseRedirect(updated_product.get_absolute_url())
    context = {
        'product_form': product_form,
        'formset': formset,
        'product': product,
        'page_title': 'Обновление технических решений',
        'bred_title': 'Обновление техрешений',
    }
    return render(request, 'productsapp/product_update.html', context)