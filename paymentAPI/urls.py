from django.urls import path
from .views import PaymentView, create_payment_intent

urlpatterns = [
    path('', PaymentView.as_view(), name='payments'),
    path('create-payment-intent/', create_payment_intent, name='create-payment-intent'),
]
