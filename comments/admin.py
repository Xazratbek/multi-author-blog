from django.contrib import admin
from .models import Comment, Like

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'is_approved', 'is_parent', 'created_at')
    list_filter = ('is_approved', 'created_at', 'parent')
    search_fields = ('content', 'user__username', 'article__title')
    actions = ['approve_comments', 'disapprove_comments']

    @admin.action(description='Tanlangan kommentlarni tasdiqlash')
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)

    @admin.action(description='Tanlangan kommentlarni bekor qilish')
    def disapprove_comments(self, request, queryset):
        queryset.update(is_approved=False)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'created_at')
    list_filter = ('created_at', 'article')
    search_fields = ('user__username', 'article__title')
    readonly_fields = ('user', 'article')
