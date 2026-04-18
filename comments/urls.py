from django.urls import path
from .views import *

urlpatterns = [
    path('<slug:slug>/comment/',CommentCreateView.as_view(),name='comment_create'),
    path('<int:id>/delete/',CommentDeleteView.as_view(),name='comment_delete'),
    path('<slug:slug>/like/',LikeToggleView.as_view(),name='like_article'),
]
