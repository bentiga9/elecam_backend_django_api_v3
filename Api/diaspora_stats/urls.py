from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DiasporaStatViewSet

router = DefaultRouter()
router.register(r'diaspora-stats', DiasporaStatViewSet, basename='diaspora-stats')

urlpatterns = [
    path('', include(router.urls)),
]
