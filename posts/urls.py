from django.urls import path

from .views import (
    PostCreateView,
    PostDeleteView,
    PostDetailView,
    PostListView,
    PostUpdateView,
)

app_name = 'posts'


urlpatterns = [
    path('create/', PostCreateView.as_view(), name='post_create'),
    path(
        '<int:post_id>/edit/',
        PostUpdateView.as_view(),
        name='post_update',
    ),
    path(
        '<int:post_id>/delete/',
        PostDeleteView.as_view(),
        name='post_delete',
    ),
    path(
        '<int:post_id>/',
        PostDetailView.as_view(),
        name='post_detail',
    ),
    path('', PostListView.as_view(), name='post_list'),
]
