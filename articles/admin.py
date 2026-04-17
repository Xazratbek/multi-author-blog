from django.contrib import admin
from .models import Article, ArticleView

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'published_at', 'created_at')
    list_filter = ('status', 'author', 'created_at')
    search_fields = ('title', 'author__username', 'content')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'author', 'status')
        }),
        ('Kontent', {
            'fields': ('content', 'published_at')
        }),
        ('Tizim ma\'lumotlari', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
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
    readonly_fields = ('article', 'user', 'session_key', 'created_at', 'updated_at')
