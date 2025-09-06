from django.db import models

class Type(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)   # AOZI CAT FOOD DRY - ALL STAGES
    description = models.TextField(blank=True)
    # category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="products")
    product_type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True, related_name="products")
    # stage = models.CharField(max_length=10, choices=STAGE_CHOICES, default="all")  # Kitten, Adult, All Stages
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    is_new = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    size = models.CharField(max_length=50)  # "1KG", "20KG (SACK)"
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="products/variants/", blank=True, null=True)
    is_available= models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product.name} - {self.size}"
    
