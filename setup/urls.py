"""
URL configuration for setup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from adocao.views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register('animais', AnimalViewSet, basename='animais')
router.register('racas', RacaViewSet, basename='racas')
router.register('tags', TagViewSet, basename='tags')
router.register('cores-pelagem', CorPelagemViewSet, basename='cores-pelagem')
router.register('tipos-pelo', TipoPeloViewSet, basename='tipos-pelo')
router.register('user', UserViewSet, basename='user')
router.register('galeria-animal', GaleriaAnimalViewSet, basename='galeria-animal')
router.register('animal-galeria', AnimalGaleriaViewSet, basename='animal-galeria')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('animal/<int:user_pk>/user', UsuarioAnimais.as_view()),
    path('animal-filtro', AnimaisFilter.as_view()),
    path('um-animal/<int:pk>/', UmAnimalViewSet.as_view(), name='um-animal-detail'),
    path('um-galeria-animal/<int:pk>/', UmGaleriaAnimal.as_view(), name='um-galeria-animal'),
    path('animal-galeria-filtro', AnimalGaleriaFiltro.as_view(), name='animal-galeria-filtro'),
    path("um-user/<int:pk>", UmUserProfileViewSet.as_view(), name='um-user-profile'),
    path("user-profile-page/<int:pk>", UmUserProfilePageViewSet.as_view(), name='user-profile-page')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
