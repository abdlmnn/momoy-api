from django.urls import path
from .views import CartView, CartDetailView

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('<int:pk>/', CartDetailView.as_view(), name='cart-detail'),
]
