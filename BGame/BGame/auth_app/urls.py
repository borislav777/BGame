from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from BGame.auth_app.views import RegisterUserView, LoginUserView, LogOutView, ProfileDetails, EditProfileVIew, \
    ChangeUserPasswordView, ResetUserPasswordView, ResetUserPasswordDoneView, ResetUserPasswordConfirmView, \
    ResetUserPasswordCompleteView, DeleteProfileView

urlpatterns = (
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),

    path('profile/edit/<int:pk>', EditProfileVIew.as_view(), name='edit profile'),
    path('profile/delete/<int:pk>', DeleteProfileView.as_view(), name='delete profile'),
    path('profile/<int:pk>', ProfileDetails.as_view(), name='profile'),


    path('profile/change/password/', ChangeUserPasswordView.as_view(), name='change password'),
    path('reset_password/', ResetUserPasswordView.as_view(), name='reset_password'),
    path('reset_password_sent/', ResetUserPasswordDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', ResetUserPasswordConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', ResetUserPasswordCompleteView.as_view(), name='password_reset_complete'),


)


