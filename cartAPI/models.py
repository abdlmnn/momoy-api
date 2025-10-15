from django.db import models
from django.conf import settings

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carts')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart #{self.id} - {self.user.email}"

class CartLine(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='lines'
    )
    inventory = models.ForeignKey(
        'inventoryAPI.Inventory',
        on_delete=models.CASCADE,
        related_name='cart_lines'
    )
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cart.user.email} - {self.inventory.product.name} x{self.quantity}"

    class Meta:
        unique_together = ('cart', 'inventory')