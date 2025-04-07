from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from . import views


# Set up the router
router = DefaultRouter()
router.register(r'stadiums', views.StadiumViewSet)
router.register(r'departments', views.DepartmentViewSet)
router.register(r'schedules', views.ScheduleViewSet)
router.register(r'checks', views.ChecksViewSet)

# URL patterns
urlpatterns = [
    # API endpoints
    path('', include(router.urls)),
    # Custom action URLs
    path('schedules/available-slots/',
         views.ScheduleViewSet.as_view({'get': 'available_slots'}), name='available-slots'),
    path('checks/increment-counter/', views.ChecksViewSet.as_view(
        {'post': 'increment_counter'}), name='increment-counter'),
    path('checks/usage-stats/',
         views.ChecksViewSet.as_view({'get': 'usage_stats'}), name='usage-stats'),
]
