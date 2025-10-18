import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from inventoryAPI.models import Inventory

# Loop through all Inventory objects
for inv in Inventory.objects.all():
    if inv.image and inv.image.url.startswith("http"):
        # Move URL to image_url field
        inv.image_url = inv.image.url
        inv.image = None  # clear the old image field
        inv.save()
        print(f"✅ Inventory {inv.id} moved URL -> image_url")
    else:
        print(f"ℹ️ Inventory {inv.id} has no Cloudinary URL or already migrated")

print("✅ Migration finished!")
