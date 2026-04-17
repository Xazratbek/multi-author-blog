from django.urls import path
from .views import *

urlpatterns = [
    path('register/',RegisterView.as_view(),name='signup'),
    path('profile/<str:username>/',ProfileDetailView.as_view(),name='see_profile'),
    path("profile/my/", MyProfileDetailView.as_view(), name="my_profile"),
    path('profile/edit/',ProfileUpdateView.as_view(),name='update_profile'),
    path('authors/',ProfileListView.as_view(),name='author_profiles')
]
