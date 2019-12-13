from django.urls import path

from newsapp.views import NewsListView, NewsDetailView, NewsUpdateView, NewsCreateView, NewsDeleteView, \
    NewsDiscussItemUpdateView

app_name = 'newsapp'

urlpatterns = [
    path('', NewsListView.as_view(), name='news_list'),
    path('<int:pk>', NewsDetailView.as_view(), name='news_detail'),
    path('update/<int:pk>', NewsUpdateView.as_view(), name='news_update'),
    path('create', NewsCreateView.as_view(), name='news_create'),
    path('delete/<int:pk>', NewsDeleteView.as_view(), name='news_delete'),
    path('create_comment/<int:news_pk>', NewsDiscussItemUpdateView.as_view(), name='comment_update')
]
