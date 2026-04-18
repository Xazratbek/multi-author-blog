from django.shortcuts import render
from django.views.generic import ListView, DetailView
from articles.models import Article
from .models import Category
from django.db.models import Q

class CategoryListView(ListView):
    model = Category
    template_name = 'categories/list.html'
    context_object_name = 'categories'

class CategoryDetailView(ListView):
    model = Article
    template_name = 'categories/category_articles.html'
    context_object_name = 'category_articles'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    paginate_by = 12

    def get_queryset(self):
        queryset = Article.objects.filter(categories__slug=self.kwargs.get("slug"),status='published').order_by('-created_at')

        q = self.request.GET.get('q','')
        if q:
            queryset =  queryset.filter(Q(title__icontains=q) | Q(content__icontains=q) | Q(categories__name__icontains=q) | Q(tags__name__icontains=q))

        category = self.request.GET.get('category','')
        if category:
            queryset = queryset.filter(categories__name=category)

        tag = self.request.GET.get('tag','')
        if tag:
            queryset = queryset.filter(tags__name=tag)

        author = self.request.GET.get('author','')
        if author:
            queryset = queryset.filter(author=author)

        return queryset

class TagDetailView(ListView):
    model = Article
    template_name = 'categories/tag_articles.html'
    context_object_name = 'tag_articles'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    paginate_by = 12

    def get_queryset(self):
        return Article.objects.filter(tags__slug=self.kwargs.get("slug"),status='published').order_by('-created_at')
