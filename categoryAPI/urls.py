from django.urls import path
from .views import CategoryView, CategoryDetailView

urlpatterns = [
    path('', CategoryView.as_view(), name='categories'),
    path('<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
]