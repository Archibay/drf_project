"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.views.generic import RedirectView

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from blog import views
from user_management import views as user_views


router = DefaultRouter()
router.register(r'post', views.PostViewSet, basename="post")
router.register(r'comments', views.CommentsViewSet, basename="comments")
router.register(r'users', user_views.UserViewSet, basename="user")


urlpatterns = [
    path('', RedirectView.as_view(url='/blog/', permanent=True)),
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('user/', include('user_management.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
]
