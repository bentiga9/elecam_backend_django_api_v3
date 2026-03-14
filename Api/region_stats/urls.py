from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegionStatViewSet

router = DefaultRouter()
router.register(r'', RegionStatViewSet, basename='region-stats')

urlpatterns = [
    path('', include(router.urls)),
]
