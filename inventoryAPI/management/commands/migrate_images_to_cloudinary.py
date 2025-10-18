from django.core.management.base import BaseCommand
from inventoryAPI.models import Inventory
from django.conf import settings
import os
import cloudinary.uploader

class Command(BaseCommand):
    help = 'Upload existing Inventory images to Cloudinary'

    def handle(self, *args, **options):
        inventories = Inventory.objects.all()
        total = inventories.count()
        success_count = 0

        for inventory in inventories:
            if inventory.image and not inventory.image.url.startswith('http'):
                # Build absolute path to local file
                local_path = os.path.join(settings.MEDIA_ROOT, inventory.image.name)
                if os.path.exists(local_path):
                    # Upload to Cloudinary
                    try:
                        result = cloudinary.uploader.upload(local_path, folder='products/variants')
                        cloud_url = result.get('secure_url')
                        if cloud_url:
                            # Save Cloudinary URL back to model
                            inventory.image = cloud_url
                            inventory.save()
                            self.stdout.write(self.style.SUCCESS(
                                f'Successfully uploaded {inventory.id} -> {cloud_url}'
                            ))
                            success_count += 1
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(
                            f'Error uploading {inventory.id}: {str(e)}'
                        ))
                else:
                    self.stdout.write(self.style.WARNING(
                        f'File not found for {inventory.id}: {local_path}'
                    ))
            else:
                self.stdout.write(f'Skipping {inventory.id}, already has valid URL.')

        self.stdout.write(self.style.SUCCESS(
            f'Finished uploading {success_count}/{total} images to Cloudinary.'
        ))
