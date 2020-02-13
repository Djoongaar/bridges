from django.urls import path

from newsapp.views import NewsListView, NewsDetailView, NewsUpdateView, NewsCreateView, NewsDeleteView, \
    NewsCommentCreate, NewsListAPI, NewsDetailAPI, NewsCreateAPI, NewsUpdateDestroyAPI, CommentCreateAPI, \
    CommentUpdateDestroyAPI

app_name = 'newsapp'

urlpatterns = [
    path('', NewsListView.as_view(), name='news_list'),
    path('<int:pk>/', NewsDetailView.as_view(), name='news_detail'),
    path('update/<int:pk>/', NewsUpdateView.as_view(), name='news_update'),
    path('create/', NewsCreateView.as_view(), name='news_create'),
    path('delete/<int:pk>/', NewsDeleteView.as_view(), name='news_delete'),
    path('create_comment/<int:news_pk>/', NewsCommentCreate.as_view(), name='comment_create'),

    # REST FRAMEWORK
    path('api/v1/news/list/', NewsListAPI.as_view()),
    path('api/v1/news/create/', NewsCreateAPI.as_view()),
    path('api/v1/news/detail/<int:pk>/', NewsDetailAPI.as_view()),
    path('api/v1/news/update/<int:pk>/', NewsUpdateDestroyAPI.as_view()),
    # path('api/v1/news/update/<int:pk>/comment/create/', CommentCreateAPI.as_view()),
    # path('api/v1/news/update/<int:pk>/comment/update/', CommentUpdateDestroyAPI.as_view())
]
