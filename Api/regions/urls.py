from django.urls import path
from .views import RegionListCreateAPIView, RegionDetailAPIView

app_name = 'regions'

urlpatterns = [
    path('', RegionListCreateAPIView.as_view(), name='list-create'),
    path('<int:pk>/', RegionDetailAPIView.as_view(), name='detail'),
]