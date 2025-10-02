from django.urls import path
from .views import WishlistView, WishlistDetailView

urlpatterns = [
    path('', WishlistView.as_view(), name='wishlist'),
    path('<int:pk>/', WishlistDetailView.as_view(), name='wishlist-detail'),
]