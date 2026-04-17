from django.urls import path
from .views import *

urlpatterns = [
    path('',ArticleListView.as_view(),name='articles'),
    path('<slug:slug>/',ArticleDetailView.as_view(),name='article_detail'),
    path('create/',ArticleCreateView.as_view(),name='article_create'),
    path('<slug:slug>/edit/',ArticleUpdateView.as_view(),name='article_update'),
    path('my/',MyArticles.as_view(),name='my_articles'),
    path('submit/<slug:slug>/',ArticleSubmitForReviewView.as_view(),name='article_submit'),
    path('review/',ReviewListView.as_view(),name='article_review'),
    path('<slug:slug>/publish/',PostPublishView.as_view(),name='article_publish'),
    path('<slug:slug>/reject/',PostRejectView.as_view(),name='article_reject'),
]
