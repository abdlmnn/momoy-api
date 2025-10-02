from django.urls import path
from .views import OrderlineView

urlpatterns = [
    path('', OrderlineView.as_view(), name='orderlines'),
]
