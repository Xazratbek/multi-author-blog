from django.contrib import admin
from django.utils import timezone
from .models import Article, ArticleView
from .forms import ArticleAdminForm


class TagInline(admin.TabularInline):
    model = Article.tags.through
    extra = 1


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    inlines = [TagInline]
    list_display = ('title', 'author', 'status', 'published_at', 'created_at')
    list_filter = ('status', 'author', 'created_at')
    list_editable = ['status']
    search_fields = ('title', 'author__username', 'content')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Kontent', {
            'fields': ('title', 'slug', 'author', 'category', 'content', 'published_at')
        }),
    )
    actions = ['make_published']

    @admin.action(description='Tanlangan maqolalarni chop etish')
    def make_published(self, request, queryset):
        for article in queryset:
            article.status = 'published'
            article.published_at = timezone.now()
            article.save()

@admin.register(ArticleView)
class ArticleViewAdmin(admin.ModelAdmin):
    list_display = ('article', 'user', 'session_key', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('article__title', 'user__username', 'session_key')
    readonly_fields = ('article', 'user', 'session_key',)
