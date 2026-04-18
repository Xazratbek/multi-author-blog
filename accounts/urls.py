from django.urls import path
from .views import *

urlpatterns = [
    path('register/',RegisterView.as_view(),name='signup'),
    path("profile/my/", MyProfileDetailView.as_view(), name="my_profile"),
    path('profile/edit/',ProfileUpdateView.as_view(),name='update_profile'),
    path('profile/<str:username>/',ProfileDetailView.as_view(),name='see_profile'),
    path('authors/',ProfileListView.as_view(),name='author_profiles'),
    path("follow/<str:username>/", FollowToAuthorView.as_view(), name="follow_to_author"),
    path('unfollow/<str:username>/',UnFollowView.as_view(),name='unfollow'),
    path('my/followers/',MyFollowersView.as_view(),name='my_followers'),
    path('my/followings/',MyFollowingsView.as_view(),name='my_followings'),
]
