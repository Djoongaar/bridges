# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.db import transaction, IntegrityError
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, render_to_response
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic.base import View

from authapp.models import Users
from newsapp.forms import NewsDiscussItemForm, NewsForm
from newsapp.models import News, NewsDiscussItem
from productsapp.models import TechnicalSolutions


class NewsListView(ListView):
    """docstring for ProductList"""    
    model = News

    template_name = 'newsapp/blog.html'
    extra_context = {}

    def get_queryset(self):
        return News.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = TechnicalSolutions.objects.all()
        latest_news = context['object_list'][:3]

        context.update({'products': products,
                        'latest_news': latest_news,
                        'page_title': 'Новости',
                        'bred_title': 'Новости'
                        })
        return context


class NewsDetailView(DetailView):
    """docstring for ProductList"""    
    model = News

    template_name = 'newsapp/blog_detail.html'
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = TechnicalSolutions.objects.all()
        latest_news = News.objects.all()[:3]
        context.update({
            'products': products,
            'latest_news': latest_news,
            'page_title': 'Новости',
            'bred_title': 'Новости'
        })
        return context


class NewsCreateView(LoginRequiredMixin, CreateView):
    """docstring for ProductList"""    
    model = News
    fields = '__all__'
    template_name = 'newsapp/newscreate_form.html'
    extra_context = {}

    def get_initial(self):
        initial = super(NewsCreateView, self).get_initial()
        initial['author'] = self.request.user
        return initial


class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    """docstring for ProductList"""    
    model = News

    template_name = 'newsapp/blog.html'
    extra_context = {}


class NewsDeleteView(PermissionRequiredMixin, DeleteView):
    """docstring for ProductList"""    
    model = News

    template_name = 'newsapp/blog.html'
    extra_context = {}


# ==================   В этом классе выходит ошибка Integrity Error ======================

class NewsCommentCreate(LoginRequiredMixin, View):
    login_url = '/auth/login/'
    form_model = NewsDiscussItem
    template = 'newsapp/newsdiscussitem_form.html'
    form = NewsDiscussItemForm

    def get(self, request, news_pk):
        news = News.objects.get(pk=news_pk)
        user = request.user
        form = self.form(initial={
            "news": news,
            "user": user})
        context = {
            'form': form,
            'news': news,
            "user": user
        }
        return render(request, template_name=self.template, context=context)

    def post(self, request, news_pk):
        news = News.objects.get(pk=news_pk)
        user = request.user
        form = self.form(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.news = news
            obj.user = user
            obj.save()
            return HttpResponseRedirect(news.get_absolute_url())
        return HttpResponse(status=400)
