from django.urls import path
from .views import *

urlpatterns = [
    path("list/",NotificationListView.as_view(),name='notification_list'),
    path("read/<int:id>/",NotificationReadView.as_view(),name='notification_read'),
    path("mark/as/read/all/",MarkAsReadAllNotifications.as_view(),name='mark_as_read'),
]
