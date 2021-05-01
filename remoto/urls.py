"""remoto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from rest_framework import routers
from app import views

admin.site.site_header = 'Gestión de datos y administación de usuarios SFPC'

router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('groups', views.GroupViewSet)
router.register('clientes', views.ClienteViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/', include('app.urls', namespace='app')),
    path('appremoto/', include('appremoto.urls', namespace='appremoto')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', RedirectView.as_view(url='/accounts/login/', permanent=True)),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
