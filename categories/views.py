from django.views.generic import ListView
from django.views import View
from django.http import JsonResponse
from articles.models import Article
from .models import Category
from django.db.models import Q

class CategoryListApiView(View):
    def get(self, request):
        rows = [
            {'id': c.pk, 'name': c.name, 'slug': c.slug}
            for c in Category.objects.order_by('name')
        ]
        return JsonResponse(
            {
                'status': 200,
                'message': 'Mavjud kategoriyalar',
                'categories': rows,
            }
        )


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
        queryset = Article.objects.filter(
            category__slug=self.kwargs.get("slug"), status='published'
        ).order_by('-created_at')

        q = self.request.GET.get('q','')
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q)
                | Q(content__icontains=q)
                | Q(category__name__icontains=q)
                | Q(tags__name__icontains=q)
            )

        category = self.request.GET.get('category','')
        if category:
            queryset = queryset.filter(category__name=category)

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
