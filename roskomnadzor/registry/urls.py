from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'registries', views.RegistryViewSet)
router.register(r'block-requests', views.BlockRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
