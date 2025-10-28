from django.db import models
from cloudinary.models import CloudinaryField
import os

class Inventory(models.Model):
    product = models.ForeignKey('productAPI.Product', on_delete=models.CASCADE, related_name="variants")
    size = models.CharField(max_length=50)  # "1KG", "20KG (SACK)"
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = CloudinaryField('image', folder='products/variants/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    is_new = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product.name} - {self.size}"

    @property
    def display_image(self):
        """
        Returns a full URL for the image:
        1. Prefer Cloudinary image
        2. Fall back to old Cloudinary URL
        3. For Expo/React Native, ensure full Cloudinary URL
        """
        if self.image:
            # Cloudinary already provides full URLs
            return self.image.url
        elif self.image_url:
            # If it's already a full URL, return as-is
            if self.image_url.startswith('http'):
                return self.image_url
            # If it's a relative path, construct full Cloudinary URL
            cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME')
            if cloud_name and self.image_url:
                return f"https://res.cloudinary.com/{cloud_name}/image/upload/{self.image_url}"
            return self.image_url
        return None

    # @property
    # def display_image(self):
    #     if self.image:
    #         return self.image.url
    #     return self.image_url if hasattr(self, 'image_url') else None