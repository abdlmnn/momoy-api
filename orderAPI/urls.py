from django.urls import path
from .views import OrderView, OrderDetailView, AdminOrderListView, AdminOrderDetailView

urlpatterns = [
    path('', OrderView.as_view(), name='orders'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('admin/', AdminOrderListView.as_view(), name='admin-orders'),
    path('admin/<int:pk>/', AdminOrderDetailView.as_view(), name='admin-order-detail'),
]
