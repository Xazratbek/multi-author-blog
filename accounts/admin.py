from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile, AuthorFollow

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profil ma\'lumotlari'
    fk_name = 'user'

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    list_display = ('username', 'email', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'telegram_url')
    search_fields = ('user__username', 'bio')

from django.contrib import admin
from .models import AuthorFollow


@admin.register(AuthorFollow)
class AuthorFollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author', 'created_at')
    list_display_links = ('id', 'user')
    search_fields = ('user__username', 'author__username', 'user__email', 'author__email')
    list_filter = ('created_at',)
    autocomplete_fields = ['user', 'author']
    ordering = ('-created_at',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'author')

    def save_model(self, request, obj, form, change):
        if obj.user == obj.author:
            from django.core.exceptions import ValidationError
            raise ValidationError("User cannot follow themselves.")
        super().save_model(request, obj, form, change)