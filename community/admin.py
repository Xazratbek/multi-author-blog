from django.contrib import admin
from .models import Community, CommunityMembership, CommunityMessage


class CommunityMembershipInline(admin.TabularInline):
    model = CommunityMembership
    extra = 1
    autocomplete_fields = ['user']
    fields = ('user', 'role')
    show_change_link = True


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'slug', 'created_at')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'slug', 'owner__username')
    list_filter = ('created_at',)
    prepopulated_fields = {'slug': ('name',)}
    autocomplete_fields = ['owner']
    inlines = [CommunityMembershipInline]
    readonly_fields = ('slug',)
    ordering = ('-created_at',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('owner')


@admin.register(CommunityMembership)
class CommunityMembershipAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'community', 'role', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('user__username', 'community__name')
    autocomplete_fields = ['user', 'community']
    ordering = ('-created_at',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'community')


@admin.register(CommunityMessage)
class CommunityMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'community', 'author', 'short_content', 'created_at')
    search_fields = ('community__name', 'author__username', 'content')
    autocomplete_fields = ['community', 'author']
    ordering = ('-created_at',)

    def short_content(self, obj):
        return obj.content[:50]
    short_content.short_description = "Content"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('community', 'author')