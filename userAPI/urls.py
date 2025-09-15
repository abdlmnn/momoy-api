from django.urls import path
from .views import TestView, GoogleLoginView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('test', TestView.as_view() ),
    path("google/", GoogleLoginView.as_view(), name="google-login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

# localhost:8000/api/v1.0/user/test