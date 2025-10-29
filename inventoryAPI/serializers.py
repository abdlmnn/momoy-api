from rest_framework import serializers
from .models import Inventory
# import os
# from cloudinary import utils

class InventorySerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    # image = serializers.SerializerMethodField()
    # Use ImageField to handle both file uploads (write) and URL generation (read).
    # `use_url=True` ensures that when serializing, it returns the full URL (e.g., from Cloudinary).
    # `required=False` makes the image optional during creation/updates.
    # image = serializers.ImageField(use_url=True, required=False, allow_null=True)

    image = serializers.SerializerMethodField()
    isNew = serializers.BooleanField(source='is_new', read_only=True)


    class Meta:
        model = Inventory
        fields = ['id', 'product', 'product_name', 'size', 'price', 'stock', 'image', 'isNew']
        # The 'image' field is now handled by ImageField, so we don't need to make it read-only.
        # It will be included in write operations (like POST) and read operations (like GET).

    def get_image(self, obj):
        """Always return full Cloudinary URL"""
        if obj.image and hasattr(obj.image, 'url'):
            # CloudinaryField.url should give full URL in production
            # But let's ensure it for all environments
            url = obj.image.url
            if url.startswith('http'):
                return url
            # Fallback: construct full URL
            from django.conf import settings
            cloud_name = getattr(settings, 'CLOUDINARY_STORAGE', {}).get('CLOUD_NAME', 'dlk1dzj2o')
            if url.startswith('/'):
                # Remove leading slash and construct Cloudinary URL
                image_path = url.lstrip('/')
                return f"https://res.cloudinary.com/{cloud_name}/image/upload/{image_path}"
            else:
                return f"https://res.cloudinary.com/{cloud_name}/image/upload/{url}"
        return None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make image field writable for POST/PUT operations
        if self.context.get('request') and self.context['request'].method in ['POST', 'PUT', 'PATCH']:
            # Replace SerializerMethodField with ImageField for write operations
            self.fields['image'] = serializers.ImageField(required=False, allow_null=True)
            
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Exclude image field for POST/PUT operations
    #     if self.context.get('request') and self.context['request'].method in ['POST', 'PUT', 'PATCH']:
    #         self.fields.pop('image', None)

    # def get_image(self, obj):
    #     return obj.display_image

    # def get_image(self, obj):
    #     if obj.image:
    #         # Cloudinary URLs are already full URLs
    #         return obj.image.url
    #     return None

    # def get_image(self, obj):
    #     if obj.image:
    #         # Cloudinary already returns full URL in production
    #         request = self.context.get('request')
    #         if request and obj.image.url.startswith('/'):
    #             # Build full URL for local files
    #             return request.build_absolute_uri(obj.image.url)
    #         return obj.image.url
    #     return None
    
    # def get_image(self, obj):
    #     if obj.image:
    #         # Use full URL so Expo can access it
    #         request = self.context.get('request')
    #         if request:
    #             return request.build_absolute_uri(obj.image.url)
    #         # fallback: manually prepend domain
    #         return f"https://momoy-api.onrender.com{obj.image.url}"
    #     return None

    # def get_image(self, obj):
    #     if obj.image:
    #         request = self.context.get('request')
    #         if request:
    #             return request.build_absolute_uri(obj.image.url)  # full URL
    #         return obj.image.url  # fallback relative URL
    #     return None

    # def get_image(self, obj):
    #     if obj.image:
    #         return f"https://momoy-api.onrender.com{obj.inventory.image.url}"
    #     return None
    
    # def get_image(self, obj):
    #     if obj.image:
    #         # Always return the full URL from the image field
    #         # Cloudinary will handle production URLs automatically
    #         return obj.image.url
    #     return None
    # def get_image(self, obj):
    #     """
    #     Ensures a full, absolute URL is returned for the image,
    #     which is required for mobile clients like Expo.
    #     """
    #     if obj.image and hasattr(obj.image, 'url'):
    #         return obj.image.url
    #     # Fallback for legacy data that might be in the `image_url` field
    #     return obj.image_url or None