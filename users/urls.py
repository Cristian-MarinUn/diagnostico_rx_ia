from django.urls import path
from . import views
from .views import Verify2FAView
app_name = 'users'

urlpatterns = [
    # CU-017: Comparar Estudios
    path('compare-studies/', views.compare_studies_view, name='compare_studies'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('profile/change-password/', views.change_password_view, name='change_password'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/user/', views.user_dashboard_view, name='user_dashboard'),
    path('dashboard/admin/', views.admin_dashboard_view, name='admin_dashboard'),
    path('dashboard/admin/user/create/', views.user_create_view, name='user_create'),
    path('dashboard/admin/list/', views.user_list_view, name='user_list'),
    path('dashboard/patient/create/', views.patient_create_view, name='patient_create'),
    path('diagnosis/request/', views.request_diagnosis_ia_view, name='request_diagnosis_ia'),
    
    # CU-018: Búsqueda de Pacientes
    path('search-patient/', views.search_patient_view, name='search_patient'),
    path('patient/<int:patient_id>/', views.patient_detail_view, name='patient_detail'),
    path('diagnosis/history/', views.diagnosis_history_view, name='diagnosis_history'),

# ========== CU-006: Autenticación de Dos Factores ==========
    path(
        '2fa/verify/',
        Verify2FAView.as_view(),
        name='2fa-verify'
    ),
    
    # TODO: Implement remaining 2FA views in views.py
    # - Enable2FAView
    # - Disable2FAView
    # - Request2FACodeView
    # - TwoFactorStatusView
    # Once implemented, uncomment the URL patterns below:
    
    # path(
    #     '2fa/enable/',
    #     Enable2FAView.as_view(),
    #     name='2fa-enable'
    # ),
    # path(
    #     '2fa/disable/',
    #     Disable2FAView.as_view(),
    #     name='2fa-disable'
    # ),
    # path(
    #     '2fa/request-code/',
    #     Request2FACodeView.as_view(),
    #     name='2fa-request-code'
    # ),
    # path(
    #     '2fa/status/',
    #     TwoFactorStatusView.as_view(),
    #     name='2fa-status'
    # ),
]


