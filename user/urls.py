from django.urls import path
from .views import *

urlpatterns = [
    path('users', UserListView.as_view(), name='user-list'),
    path('users/<uuid:id>', UserDetailView.as_view(), name='user-detail'),
    path('login', LoginAPIView.as_view(), name='login'),
    path('logout', LogoutAPIView.as_view(), name='api-logout'),
    path('forgotpassword', ForgotPasswordAPIView.as_view(), name='forgotpassword'),
    path('reset-password/<uidb64>/<token>', PasswordResetConfirmAPIView.as_view(), name='password-reset-confirm'),
    path('users/<uuid:user_id>/profile', UserProfileDetailView.as_view(), name='user-profile-detail'),
    
]
