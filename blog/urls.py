from django.urls import path
from django.shortcuts import render
from . import views

app_name = 'blog'
urlpatterns = [
    # path('', views.index_view, name='index'),
    path('post-add/', views.post_new, name='add_post'),
    # path('post-detail/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post-detail/<int:pk>/', views.post_detail, name='post_detail'),
    path('', views.PostsListView.as_view(), name='posts_all'),
    path('user-posts/', views.LoginUserPostsAllView.as_view(), name='user_posts'),
    path('post/<int:pk>/comments', views.CommentAddView.as_view(), name='comment_add'),
    path('post-update/<int:pk>/', views.PostUpdateView.as_view(), name='post_update'),
    path('contact-us/', views.contact_us_view, name='contact_us'),
    path('user_post-detail/<int:pk>/', views.UserPostDetailView.as_view(), name='user_post_detail'),
    path('post-delete/<int:pk>/', views.PostDeleteView.as_view(), name='post_delete'),

]
