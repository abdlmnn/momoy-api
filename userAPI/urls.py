from django.urls import path
from .views import TestView


urlpatterns = [
    path('type/', TestView.as_view() ),
]

# localhost:8000/api/v1.0/user/test