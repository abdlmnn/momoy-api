from django.core.management.base import BaseCommand
from inventoryAPI.models import Inventory
import cloudinary.uploader
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Migrate existing local images to Cloudinary'

    def handle(self, *args, **options):
        inventories = Inventory.objects.exclude(image='')

        for inventory in inventories:
            if inventory.image and hasattr(inventory.image, 'path'):
                try:
                    # Upload to Cloudinary
                    result = cloudinary.uploader.upload(
                        inventory.image.path,
                        folder="products/variants/",
                        public_id=f"{inventory.product.name}_{inventory.size}".replace(" ", "_").replace("-", "_")
                    )

                    # Update the image field with Cloudinary public_id (without extension)
                    inventory.image = result['public_id']
                    inventory.save()

                    self.stdout.write(
                        self.style.SUCCESS(f'Successfully migrated image for {inventory.product.name} - {inventory.size}')
                    )

                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Failed to migrate image for {inventory.product.name} - {inventory.size}: {str(e)}')
                    )
            else:
                self.stdout.write(
                    self.style.WARNING(f'No local image found for {inventory.product.name} - {inventory.size}')
                )

        self.stdout.write(self.style.SUCCESS('Migration completed!'))