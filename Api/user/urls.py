# user/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('token/refresh/', views.TokenRefreshView.as_view(), name='token-refresh'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.update_profile_view, name='update-profile'),
    path('profile/delete/', views.delete_account_view, name='delete-account'),
    path('change-password/', views.change_password_view, name='change-password'),
    path('count/', views.count_users_view, name='count-users'),
    # Password Reset endpoints
    path('password-reset/request/', views.RequestPasswordResetView.as_view(), name='request-password-reset'),
    path('password-reset/verify/', views.VerifyResetCodeView.as_view(), name='verify-reset-code'),
    path('password-reset/confirm/', views.ResetPasswordView.as_view(), name='reset-password'),
]