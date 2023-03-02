from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('posts/', views.PostListView.as_view(), name="posts"),
    path('posts/<int:pk>', views.PostDetailView.as_view(), name='post-detail'),
    path('comments/<int:pk>/delete', views.CommentDeleteView.as_view(), name='delete-comment'),
    path('authors', views.AuthorListView.as_view(), name='authors'),
    path('authors/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('posts/my/', views.AuthorPostsListView.as_view(), name='author-posts-list'),
    path('posts/my/new', views.PostCreateView.as_view(), name='create-new-post'),
    path('posts/my/<int:pk>/update/', views.PostUpdateView.as_view(), name='update-post'),
    path('posts/my/<int:pk>/delete/', views.PostDeleteView.as_view(), name='delete-post'),
]