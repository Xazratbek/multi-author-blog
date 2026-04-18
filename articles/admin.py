from django.contrib import admin
from .models import Article, ArticleView
from .forms import ArticleAdminForm

class CategoryInline(admin.TabularInline):
    model = Article.categories.through
    extra = 1

class TagInline(admin.TabularInline):
    model = Article.tags.through
    extra = 1

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    inlines = [CategoryInline,TagInline]
    list_display = ('title', 'author', 'status', 'published_at', 'created_at')
    list_filter = ('status', 'author', 'created_at')
    search_fields = ('title', 'author__username', 'content')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Kontent', {
            'fields': ('title','slug','author','content', 'published_at')
        }),
    )
    actions = ['make_published']

    @admin.action(description='Tanlangan maqolalarni chop etish')
    def make_published(self, request, queryset):
        queryset.update(status='published')

@admin.register(ArticleView)
class ArticleViewAdmin(admin.ModelAdmin):
    list_display = ('article', 'user', 'session_key', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('article__title', 'user__username', 'session_key')
    readonly_fields = ('article', 'user', 'session_key',)
