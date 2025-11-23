from django.urls import path
from .views import ProfileView, DashboardView, AdminDashboardView, UserCreateView

app_name = 'users'

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('admin/users/create/', UserCreateView.as_view(), name='user_create'),
]