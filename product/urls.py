from django.urls import path
from .views import ProductView, TypeView, InventoryView


urlpatterns = [
    # GET, POST, PUT, DELETE
    path('type/', TypeView.as_view() ),
    path('product/', ProductView.as_view() ),
    path('inventory/', InventoryView.as_view() ),

]

# localhost:8000/api/type