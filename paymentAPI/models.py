from django.db import models

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cod', 'Cash on Delivery'),
        ('gcash', 'GCash'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('delivery', 'Delivery'),
    ]
    order = models.OneToOneField('orderAPI.Order', related_name='payment', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    proof_image = models.ImageField(upload_to='payments/', blank=True, null=True)  # For GCash proof of payment
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order {self.order.id}"
