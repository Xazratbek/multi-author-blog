from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    # path("ckeditor5/", include("django_ckeditor_5.urls")),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
    path('categories/', include('categories.urls')),
    path('comments/', include('comments.urls')),
    path('notifications/', include('notifications.urls')),
    path('community/', include('community.urls')),
    path('', include('articles.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()

    # import debug_toolbar
    # urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]