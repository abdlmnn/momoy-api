from django.db import models

class Orderline(models.Model):
    order = models.ForeignKey('orderAPI.Order', on_delete=models.CASCADE, related_name='orderlines')
    inventory = models.ForeignKey('inventoryAPI.Inventory', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price at time of order

    def __str__(self):
        return f"{self.order.id} - {self.inventory.product.name} x{self.quantity}"
