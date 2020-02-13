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
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from authapp.models import Users
from newsapp.forms import NewsDiscussItemForm, NewsForm
from newsapp.models import News, NewsDiscussItem
from newsapp.serializers import NewsListSerializer, NewsDetailSerializer, NewsCommentsSerializer
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
    extra_context = {
        'page_title': 'Новая статья',
        'bred_title': 'Новая статья'
    }

    def get_initial(self):
        initial = super(NewsCreateView, self).get_initial()
        initial['author'] = self.request.user
        return initial


class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    """docstring for ProductList"""    
    model = News
    fields = '__all__'
    permission_required = 'news.can_change'

    template_name = 'newsapp/newscreate_form.html'
    extra_context = {}


class NewsDeleteView(PermissionRequiredMixin, DeleteView):
    """docstring for ProductList"""    
    model = News
    permission_required = 'news.can_delete'
    success_url = reverse_lazy('news:news_list')
    template_name = 'newsapp/news_confirm_delete.html'
    extra_context = {
        'page_title': 'Удалить новость',
        'bred_title': 'Удалить новость'
    }


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


#  ------------------------------------ REST FRAMEWORK API ---------------------------------------------

class NewsListAPI(generics.ListAPIView):
    serializer_class = NewsListSerializer

    def get_queryset(self):
        user = self.request.user
        return News.objects.all()


class NewsDetailAPI(generics.RetrieveAPIView):
    serializer_class = NewsDetailSerializer

    def get_queryset(self):
        user = self.request.user
        return News.objects.all()


class NewsCreateAPI(generics.CreateAPIView):
    serializer_class = NewsDetailSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class NewsUpdateDestroyAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NewsDetailSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        print(user)
        if user.is_superuser:
            return News.objects.all()
        else:
            objects = user.get_news()
            return objects


class CommentCreateAPI(generics.CreateAPIView):
    serializer_class = NewsCommentsSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CommentUpdateDestroyAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NewsCommentsSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        print(user)
        if user.is_superuser:
            return NewsDiscussItem.objects.all()
        else:
            comments = user.get_comments()
            users_comments = [i.comments.pk for i in comments]
            return NewsDiscussItem.objects.filter(pk__in=users_comments)
