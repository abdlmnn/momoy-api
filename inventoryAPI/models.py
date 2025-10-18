from django.db import models

class Inventory(models.Model):
    product = models.ForeignKey('productAPI.Product', on_delete=models.CASCADE, related_name="variants")
    size = models.CharField(max_length=50)  # "1KG", "20KG (SACK)"
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.CharField(max_length=255, blank=True, null=True)  # Store Cloudinary public_id
    is_new = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product.name} - {self.size}"
