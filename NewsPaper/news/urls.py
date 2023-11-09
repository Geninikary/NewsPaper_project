from django.urls import path
from .views import (PostList, PostDetail, NewsPostCreate, ArticlePostCreate, NewsPostDelete, ArticlePostDelete,
                    NewsPostUpdate, ArticlePostUpdate, PostSearch, IndexView, upgrade_me)

urlpatterns = [
    path('news/', PostList.as_view(), name='posts_list'),
    path('news/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('news/search/', PostSearch.as_view(), name='news_search'),
    path('news/create/', NewsPostCreate.as_view(), name='news_create'),
    path('articles/create/', ArticlePostCreate.as_view(), name='article_create'),
    path('news/<int:pk>/delete/', NewsPostDelete.as_view(), name='news_delete'),
    path('articles/<int:pk/delete/', ArticlePostDelete.as_view(), name='articles_delete'),
    path('news/<int:pk>/edit/', NewsPostUpdate.as_view(), name='news_update'),
    path('articles/<int:pk>/edit/', ArticlePostUpdate.as_view(), name='article_update'),
    path('profile/', IndexView.as_view(), name='profile'),
    path('profile/upgrade/', upgrade_me, name='upgrade'),
]
