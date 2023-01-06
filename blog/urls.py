from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter


app_name = 'blog'
urlpatterns = [
    # path('', views.index_view, name='index'),
    path('post-add/', views.post_new, name='add_post'),
    # path('post-detail/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post-detail/<int:pk>/', views.post_detail, name='post_detail'),
    path('', views.PostsListView.as_view(), name='posts_all'),
    path('comments/', views.CommentsListView.as_view(), name='comments_all'),
    path('user-posts/', views.LoginUserPostsAllView.as_view(), name='user_posts'),
    path('user-comments/', views.LoginUserCommentsAllView.as_view(), name='user_comments'),
    path('post/<int:pk>/comments/', views.CommentAddView.as_view(), name='comment_add'),
    path('post-update/<int:pk>/', views.PostUpdateView.as_view(), name='post_update'),
    path('comment-update/<int:pk>/', views.CommentUpdateView.as_view(), name='comment_update'),
    path('contact-us/', views.contact_us_view, name='contact_us'),
    path('user_post-detail/<int:pk>/', views.UserPostDetailView.as_view(), name='user_post_detail'),
    path('user_comment-detail/<int:pk>/', views.UserCommentDetailView.as_view(), name='comment_detail'),
    path('post-delete/<int:pk>/', views.PostDeleteView.as_view(), name='post_delete'),
    path('comment-delete/<int:pk>/', views.CommentDeleteView.as_view(), name='comment_delete'),

]

router = DefaultRouter()
router.register(r'post', views.PostViewSet, basename="post")
router.register(r'comments', views.CommentsViewSet, basename="comments")
