from django.urls import path
from .views import InventoryView, InventoryDetailView

urlpatterns = [
    path('', InventoryView.as_view(), name='inventory'),
    path('<int:pk>/', InventoryDetailView.as_view(), name='inventory-detail'),
]