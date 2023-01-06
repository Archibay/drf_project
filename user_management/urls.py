from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as token_view


app_name = 'user_management'
urlpatterns = [
    path('registration/', views.RegistrationView.as_view(), name='registration'),

    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("user-detail/", views.UserDetailView.as_view(), name="user_detail"),
    path("user-update/", views.UserUpdateView.as_view(), name="user_update"),
    path("user-detail-pub/<int:pk>/", views.UserProfilePublicDetailView.as_view(), name="user_detail_pub"),
    path('api-token-auth/', token_view.obtain_auth_token)

]

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename="user")
