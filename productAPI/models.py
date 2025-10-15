from django.db import models

class Product(models.Model):
    PRODUCT_TYPE_CHOICES = [
        ('dry_food', 'Dry Food'),
        ('wet_food', 'Wet Food'),
        ('pet_care', 'Pet Care'),
        ('pet_treats', 'Pet Treats'),
        ('pet_milk', 'Pet Milk'),
        ('cat_litter', 'Cat Litter'),
        ('other_essentials', 'Other Essentials'),
        ('merch', 'Merch'),
    ]
    name = models.CharField(max_length=200)
    category = models.ForeignKey('categoryAPI.Category', on_delete=models.PROTECT, null=False, blank=False, related_name="products")
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPE_CHOICES, blank=True, null=True)
    brand = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
