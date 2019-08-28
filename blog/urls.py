from django.urls import path, include, re_path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('author/<username>/', views.UserPostListView.as_view(), name='author-post-list'),
]