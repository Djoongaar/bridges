from django.contrib.auth.decorators import user_passes_test
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from productsapp.forms import ProductUpdateForm, ProductForm, TechSolHasServiceForm, ProductWorkForm
from django.views.generic import ListView, DetailView
from productsapp.models import TechnicalSolutions, TechnicalSolutionsHasService, ProductWork


@method_decorator(cache_page(3600), name='dispatch')
class ProductsView(ListView):
    template_name = 'productsapp/products.html'
    context_object_name = 'all_products'
    extra_context = {
        'page_title': 'Технические решения для транспортного строительства',
        'bred_title': 'Технические решения'
    }

    def get_queryset(self):
        return TechnicalSolutions.objects.all().order_by('pk').filter(is_active=True)


@method_decorator(cache_page(3600), name='dispatch')
class ProductRead(DetailView):
    model = TechnicalSolutions
    extra_context = {}
    not_empty_url = reverse_lazy('products:product')
    template_name = 'productsapp/product.html'

    def get_queryset(self):
        if self.request.user.is_staff:
            return TechnicalSolutions.objects.all()
        else:
            return TechnicalSolutions.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super(ProductRead, self).get_context_data(**kwargs)
        product = self.object
        if self.request.user.is_staff:
            projects = product.get_projects
        else:
            projects = product.get_active_projects
        context.update({'page_title': product,
                        'bred_title': product,
                        'projects': projects,
                        'publications': product.get_publications,
                        'researches': product.get_researches,
                        'documents': product.get_documents,
                        'materials': product.get_materials,
                        })
        return context


@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    product = get_object_or_404(TechnicalSolutions, pk=pk)
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
def product_service_update(request, pk):
    product = get_object_or_404(TechnicalSolutions, pk=pk)
    product_form = ProductForm(instance=product)
    product_formset = inlineformset_factory(TechnicalSolutions, TechnicalSolutionsHasService,
                                            form=TechSolHasServiceForm,
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
def product_work_update(request, pk):
    product = get_object_or_404(TechnicalSolutions, pk=pk)
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
