from django.urls import path
from .views import (
    RegisterView,
    LogoutView,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    AdminUserListView,
    AdminUserDetailView,
    AdminPasswordResetView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('admin/users/', AdminUserListView.as_view(), name='admin_user_list'),
    path('admin/users/<int:pk>/', AdminUserDetailView.as_view(), name='admin_user_detail'),
    path('admin/users/<int:user_id>/reset-password/', AdminPasswordResetView.as_view(), name='admin_password_reset'),
]
