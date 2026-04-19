from django.urls import path
from .views import *

urlpatterns = [
    path('',CommunityListView.as_view(),name='communities'),
    path('create/',CommunityCreateView.as_view(),name='community_create'),
    path('<slug:slug>/',CommunityDetailView.as_view(),name='community_detail'),
    path('<slug:slug>/messages/', CommunityMessageListView.as_view(), name='community_message_list'),
    path('join/<slug:slug>/',JoinCommunityView.as_view(),name='community_join'),
    path('leave/<slug:slug>/',LeaveCommunityView.as_view(),name='community_leave'),
    path('messages/send/<slug:slug>/',CommunityMessageSendView.as_view(),name='community_message_send'),
]
