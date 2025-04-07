from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

# Set up the router
router = DefaultRouter()
router.register(r'users', views.UserViewSet)

# URL patterns
urlpatterns = [
    # API endpoints
    path('', include(router.urls)),

    # User profile endpoint
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),

    # Login endpoint
    path('login/', views.UserViewSet.as_view({'post': 'login'}), name='login'),

    # Department filtering
    path('users-by-department/',
         views.UserViewSet.as_view({'get': 'by_department'}), name='users-by-department'),
]
