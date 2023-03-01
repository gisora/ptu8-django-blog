from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('posts/', views.PostListView.as_view(), name="posts"),
    path('posts/<int:pk>', views.PostDetailView.as_view(), name='post-detail'),
    path('authors', views.AuthorListView.as_view(), name='authors'),
    path('authors/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('posts/my/', views.AuthorPostsListView.as_view(), name="author-posts-list"),
]