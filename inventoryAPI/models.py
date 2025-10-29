from django.db import models
from cloudinary.models import CloudinaryField
import os

class Inventory(models.Model):
    product = models.ForeignKey('productAPI.Product', on_delete=models.CASCADE, related_name="variants")
    size = models.CharField(max_length=50)  # "1KG", "20KG (SACK)"
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    # This is the single source of truth for the image.
    image = CloudinaryField('image', folder='products/variants/', blank=True, null=True)
    # The image_url field is now redundant because the serializer handles URL generation.
    # image_url = models.URLField(blank=True, null=True) # This can be removed after migrating data.
    is_new = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product.name} - {self.size}"\
    
    @property
    def image_url(self):
        """Always return full Cloudinary URL"""
        if self.image and hasattr(self.image, 'url'):
            url = self.image.url
            if url.startswith('http'):
                return url
            # Construct full URL for development
            from django.conf import settings
            cloud_name = getattr(settings, 'CLOUDINARY_STORAGE', {}).get('CLOUD_NAME', 'dlk1dzj2o')
            if url.startswith('/'):
                image_path = url.lstrip('/')
                return f"https://res.cloudinary.com/{cloud_name}/image/upload/{image_path}"
            else:
                return f"https://res.cloudinary.com/{cloud_name}/image/upload/{url}"
        return None

    # @property
    # def display_image(self):
    #     """Returns the full image URL from the CloudinaryField."""
    #     if self.image and hasattr(self.image, 'url'):
    #         return self.image.url
    #     return None

    # @property
    # def display_image(self):
    #     """
    #     Returns a full URL for the image:
    #     1. Prefer Cloudinary image
    #     2. Fall back to old Cloudinary URL
    #     """
    #     if self.image:
    #         return self.image.url
    #     return self.image_url

    # @property
    # def display_image(self):
    #     if self.image:
    #         return self.image.url
    #     return self.image_url if hasattr(self, 'image_url') else None