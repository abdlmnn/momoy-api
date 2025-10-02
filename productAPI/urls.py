from django.urls import path
from .views import ProductView, ProductDetailView, ProductSearchView

urlpatterns = [
    path('', ProductView.as_view(), name='products'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('search/', ProductSearchView.as_view(), name='product-search'),
]