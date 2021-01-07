from django.urls import path
# from .views import *
from . import views
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView
urlpatterns = [
    # path('accounts/profile/', views.home, name='home'), # home urls for django LoginView url path should be accounts/profile after login this url will be redirected
    # path('login/', LoginView.as_view(), name='login'),  # Url for django LoginView template location must be /registration/login.html
    # path('logout/', LogoutView.as_view(), name='logout'),
    path('', views.home, name='home'),
    path('signup/', views.user_creation, name='signup'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('password-reset/', PasswordResetView.as_view(template_name='password_reset/password_reset.html'), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='password_reset/password_reset_done.html'), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='password_reset/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset/completed/', PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_complete.html'), name='password_reset_complete'),  
    path('profile/<str:id>/<slug:slug>/', views.profile, name='profile'),
    path('profile-update/<str:id>/<slug:slug>/', views.update_profile, name='update_profile'),
    path('profile_list/', views.profile_list, name='profile_list'),
    path('change-password/', PasswordChangeView.as_view(template_name='change_password/change_password.html'), name='password_change'),
    path('change-password/done/', PasswordChangeDoneView.as_view(template_name='change_password/change_password_done.html'), name='password_change_done'),
    path('follow-user/', views.follow_user, name='follow_user'),
]   