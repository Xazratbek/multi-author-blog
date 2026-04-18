from django.urls import path
from .views import *

urlpatterns = [
    path('categories/',CategoryListView.as_view() ,name='category_list'),
    path('categories/<slug:slug>/',CategoryDetailView.as_view(),name='category_articles'),
    path('tags/<slug:slug>/',TagDetailView.as_view(),name='tag_articles'),
]
