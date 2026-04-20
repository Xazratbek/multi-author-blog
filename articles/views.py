import json
from django.db import transaction
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from .models import Article, ArticleView, ArticleStatusChoice
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView
from .forms import ArticleForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.db.models import Q
from notifications.tasks import enqueue_new_post_notifications
from accounts.models import AuthorFollow
from categories.models import Category, Tag

class TagApiView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '')
        tags_qs = Tag.objects.all()
        if query:
            tags_qs = tags_qs.filter(name__icontains=query)

        tags = tags_qs.order_by('name')[:20]
        tag_list = [{'id': tag.id, 'text': tag.name} for tag in tags]
        return JsonResponse(tag_list, safe=False)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            name = data.get('name', '').strip()
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        if not name:
            return JsonResponse({'error': 'Tag name cannot be empty'}, status=400)

        if len(name) > Tag._meta.get_field('name').max_length:
            return JsonResponse({'error': f'Tag name cannot be more than {Tag._meta.get_field("name").max_length} characters'}, status=400)

        tag, created = Tag.objects.get_or_create(name=name)

        status_code = 201 if created else 200
        return JsonResponse({'id': tag.id, 'text': tag.name}, status=status_code)


class ArticleFormTagOptionsMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = context.get('form')
        cid = None
        if form:
            if form.is_bound:
                v = form.data.get('category')
                if v:
                    try:
                        cid = int(v)
                    except (TypeError, ValueError):
                        pass
            else:
                obj = getattr(self, 'object', None)
                if obj is not None and getattr(obj, 'pk', None) and obj.category_id:
                    cid = obj.category_id
        context['category_initial_id_json'] = json.dumps(cid)
        return context


class ArticleListView(ListView):
    model = Article
    template_name = 'article/list.html'
    context_object_name = 'articles'
    paginate_by = 12

    def get_queryset(self):
        queryset = (
            Article.objects.filter(status='published')
            .select_related('category')
            .prefetch_related('views')
            .order_by('-created_at')
        )
        q = self.request.GET.get('q','')
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q)
                | Q(content__icontains=q)
                | Q(category__name__icontains=q)
                | Q(tags__name__icontains=q)
                | Q(author__username__icontains=q)
            )

        category = self.request.GET.get('category','')
        if category:
            queryset = queryset.filter(category__slug=category)

        tag = self.request.GET.get('tag','')
        if tag:
            queryset = queryset.filter(tags__slug=tag)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.order_by('name')
        context['tags'] = Tag.objects.order_by('name')
        return context

class ArticleCreateView(LoginRequiredMixin, ArticleFormTagOptionsMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'article/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('article_detail', kwargs={'slug': self.object.slug})

class ArticleDetailView(View):
    def get(self, request, slug):
        article = get_object_or_404(Article, slug=slug)

        if not request.session.session_key:
            request.session.save()

        session_key = request.session.session_key
        user = request.user if request.user.is_authenticated else None

        if user:
            ArticleView.objects.get_or_create(article=article, user=user)
        else:
            ArticleView.objects.get_or_create(article=article, session_key=session_key)

        is_following_author = (
            request.user.is_authenticated
            and request.user != article.author
            and AuthorFollow.objects.filter(user=request.user, author=article.author).exists()
        )

        return render(request, 'article_detail.html', {'article': article, 'is_following_author': is_following_author})

class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, ArticleFormTagOptionsMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'article/update.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def test_func(self):
        article = self.get_object()
        return article.author == self.request.user

    def get_success_url(self):
        return reverse_lazy('article_detail', kwargs={'slug': self.object.slug})


class MyArticles(LoginRequiredMixin,ListView):
    model = Article
    template_name = 'article/my_articles.html'
    context_object_name = 'article'

    def get_queryset(self):
        queryset = Article.objects.filter(author=self.request.user).prefetch_related('views')
        status_filter = self.request.GET.get('status')

        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_status'] = self.request.GET.get('status', 'all')
        return context

class ArticleSubmitForReviewView(LoginRequiredMixin, UserPassesTestMixin,View):
    def test_func(self):
        article = get_object_or_404(Article, slug=self.kwargs.get('slug'))
        return article.author == self.request.user

    def post(self,request,slug):
        article = get_object_or_404(Article,slug=slug,author=request.user)
        if article:
            article.status = 'in_progress'
            article.save()
            next_url = request.POST.get('next')
            if next_url:
                return redirect(next_url)
            return JsonResponse({"status": 201,"message": "Maqola tekshiruvga yuborildi"})
        else:
            return JsonResponse({"status": 400,'message': "Maqola topilmadi"})

class ReviewListView(LoginRequiredMixin,UserPassesTestMixin,ListView):
    model = Article
    template_name = 'admin/article_reviews.html'
    context_object_name = 'articles'
    paginate_by = 12

    def test_func(self):
        return self.request.user.is_superuser

    def get_queryset(self):
        return Article.objects.filter(status='in_progress').prefetch_related('views')

class PostPublishView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def post(self, request, slug):
        article = get_object_or_404(Article, slug=slug)

        if article.status == ArticleStatusChoice.PUBLISHED:
            return JsonResponse({"status": 200, 'message': 'Maqola allaqachon chop etilgan.'})

        article.status = ArticleStatusChoice.PUBLISHED
        article.published_at = timezone.now()
        article.save(update_fields=['status', 'published_at'])

        transaction.on_commit(
            lambda: enqueue_new_post_notifications(article.slug)
        )

        next_url = request.POST.get('next')
        if next_url:
            return redirect(next_url)
        return JsonResponse({"status": 200, 'message': 'Maqola chop etildi va obunachilarga xabar yuborilmoqda.'})

class PostRejectView(LoginRequiredMixin,UserPassesTestMixin,View):
    def test_func(self):
        return self.request.user.is_superuser

    def post(self, request, slug):
        article = Article.objects.filter(slug=slug).first()
        if article:
            article.status = 'draft'
            article.save()
            next_url = request.POST.get('next')
            if next_url:
                return redirect(next_url)
            return JsonResponse({"status": 200, 'message': 'Maqola chop etilishi bekor qilindi'})

        else:
            return JsonResponse({"status": 400,'message': 'Maqola mavjud emas'})
