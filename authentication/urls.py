from django.urls import path
from .views import LoginView, LogoutView, LogoutCancelView
from . import views



app_name = 'authentication'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logout/cancel/', LogoutCancelView.as_view(), name='logout_cancel'),
    path(
        'password-recovery/',
        views.password_recovery_view,
        name='password_recovery'
    ),
    path(
        'password-reset/<str:token>/',
        views.password_reset_view,
        name='password_reset'
    ),
]
