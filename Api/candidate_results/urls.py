from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CandidateGlobalResultViewSet,
    CandidateRegionResultViewSet,
    CandidateDepartmentResultViewSet,
    CandidateDiasporaResultViewSet
)

router = DefaultRouter()
router.register(r'global', CandidateGlobalResultViewSet, basename='candidate-global-result')
router.register(r'regional', CandidateRegionResultViewSet, basename='candidate-region-result')
router.register(r'departmental', CandidateDepartmentResultViewSet, basename='candidate-department-result')
router.register(r'diaspora', CandidateDiasporaResultViewSet, basename='candidate-diaspora-result')

urlpatterns = [
    path('', include(router.urls)),
]
