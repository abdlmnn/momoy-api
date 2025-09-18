from django.urls import path
from .views import LoginView, VerifyEmailView, GoogleLoginView, TestView, EmailSignupView, CheckVerificationView, CreateAccountView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('test', TestView.as_view() ),
    
    path("login/", LoginView.as_view(), name="signup"),

    path("email-signup/", EmailSignupView.as_view(), name="email-signup"),
    path("verify-email/<uidb64>/<token>/", VerifyEmailView.as_view(), name="verify-email"),

    path("check-verification/", CheckVerificationView.as_view(), name="check-verification"),

     path("create-account/", CreateAccountView.as_view(), name="create-account"),

    path("google/", GoogleLoginView.as_view(), name="google-login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
