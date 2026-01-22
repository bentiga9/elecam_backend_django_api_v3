from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DepartmentStatViewSet

router = DefaultRouter()
router.register(r'departments', DepartmentStatViewSet, basename='department-stat')

urlpatterns = [
    path('', include(router.urls)),
]
