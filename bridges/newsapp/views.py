# -*- coding: utf-8 -*-
from django.db import transaction, IntegrityError
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, render_to_response
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from django.contrib.auth.mixins import PermissionRequiredMixin
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


class NewsCreateView(PermissionRequiredMixin, CreateView):
    """docstring for ProductList"""    
    model = News

    template_name = 'newsapp/blog.html'
    extra_context = {}


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


# class NewsCommentCreate(UpdateView):
#     model = News
#     fields = []
#     template_name = 'newsapp/newsdiscussitem_form.html'
#
#     def get_context_data(self, **kwargs):
#         data = super(NewsDiscussItemUpdateView, self).get_context_data(**kwargs)
#         NewsFormSet = inlineformset_factory(News, NewsDiscussItem, form=NewsDiscussItemForm, extra=1)
#         if self.request.POST:
#             data['comments'] = NewsFormSet(self.request.POST, instance=self.object)
#         else:
#             data['comments'] = NewsFormSet(instance=self.object)
#         return data
#
#     def form_valid(self, form):
#         context = self.get_context_data()
#         comments = context['comments']
#
#         if form.is_valid():
#             # form.instance.author = self.request.user
#             self.object = form.save()
#             if comments.is_valid():
#                 comments.instance = self.object
#                 comments.save()
#                 return HttpResponseRedirect(reverse_lazy('news:news_list'))
#         return HttpResponse(status=400)


# ==================   В этом классе выходит ошибка Integrity Error ======================

class NewsCommentCreate(View):
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
        form = self.form(request.POST)
        if form.is_valid():
            hacked = {
                "news": News.objects.get(pk=form.data["news"]),
                "user": Users.objects.get(pk=form.data["user"])
            }
            data = {**form.data, **hacked}
            data = {k: v[0] if isinstance(v, list) else v for k, v in data.items() if
                    k in {f.name for f in self.form_model._meta.fields}}
            obj = self.form_model(**data)
            obj.save()
            return HttpResponseRedirect(news.get_absolute_url())
        return HttpResponse(status=400)
