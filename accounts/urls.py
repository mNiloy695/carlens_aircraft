from .views import RegistrationView,LoginView,LogoutView,ActivateAccountView,ForgotPasswordView,ResetView
from django.urls import path
urlpatterns = [
    path('register/',RegistrationView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('activate/',ActivateAccountView.as_view(),name='active_account'),
    path('forgot-password/',ForgotPasswordView.as_view(),name="forgot-password"),
    path('reset-password/',ResetView.as_view(),name='reset-password'),
]



#262499