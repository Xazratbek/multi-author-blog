from django.urls import path
from .views import *

urlpatterns = [
    path('api/tags/', TagApiView.as_view(), name='tag_api'),
    path('',ArticleListView.as_view(),name='articles'),
    path('create/',ArticleCreateView.as_view(),name='article_create'),
    path('edit/<slug:slug>/',ArticleUpdateView.as_view(),name='article_update'),
    path('my/',MyArticles.as_view(),name='my_articles'),
    path('submit/<slug:slug>/',ArticleSubmitForReviewView.as_view(),name='article_submit'),
    path('review/',ReviewListView.as_view(),name='article_review'),
    path('publish/<slug:slug>/',PostPublishView.as_view(),name='article_publish'),
    path('reject/<slug:slug>/',PostRejectView.as_view(),name='article_reject'),
    path('<slug:slug>/',ArticleDetailView.as_view(),name='article_detail'),
]
