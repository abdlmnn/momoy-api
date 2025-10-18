import os
import django

# Set Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from inventoryAPI.models import Inventory

# -----------------------------
# STEP 1: Map Inventory IDs to Cloudinary URLs
# Replace these IDs and URLs with your actual Inventory IDs and Cloudinary URLs
image_map = {
    1: "https://res.cloudinary.com/dlk1dzj2o/image/upload/v1760809249/TOPBREED_DOG_FOOD_DRY_-_PUPPY_20KG_SACK_tmpydl.png",
    2: "https://res.cloudinary.com/dlk1dzj2o/image/upload/v1760809242/AOZI_DOG_FOOD_DRY_-_PUPPY_SILVER_1KG_gd9x3q.png",
    3: "https://res.cloudinary.com/dlk1dzj2o/image/upload/v1760809242/AOZI_DOG_FOOD_DRY_SILVER_-_PUPPY_20KG_SACK_-_P3900_gblcxx.png",
    4: "https://res.cloudinary.com/dlk1dzj2o/image/upload/v1760809242/AOZI_CAT_FOOD_DRY_-_ALL_STAGES_1KG_biqggw.png",
    5: "https://res.cloudinary.com/dlk1dzj2o/image/upload/v1760809241/ALPHAPRO_DOG_FOOD_DRY_REGULAR_BITES_-_P1300_ducg6q.png",
    6: "https://res.cloudinary.com/dlk1dzj2o/image/upload/v1760809241/ALPHAPRO_DOG_FOOD_DRY_PUPPY_BITES_hgltou.png",
    7: "https://res.cloudinary.com/dlk1dzj2o/image/upload/v1760809242/AZU_DOG_FOOD_DRY_-_ALL_STAGES_1KG_rfyywp.png",
    8: "https://res.cloudinary.com/dlk1dzj2o/image/upload/v1760809242/AOZI_CAT_FOOD_DRY_-_ALL_STAGES_20KG_SACK_dbfgph.png",
    9: "https://res.cloudinary.com/dlk1dzj2o/image/upload/v1760809243/ROYAL_CANIN_CAT_FOOD_WET_-_ADULT_85G_POUCH_HAIR_SKIN_xvzizd.png",
    10: "https://res.cloudinary.com/dlk1dzj2o/image/upload/v1760809244/ROYAL_CANIN_CAT_FOOD_WET_-_ADULT_85G_POUCH_HAIRBALL_flunk3.png",
    11: "https://res.cloudinary.com/dlk1dzj2o/image/upload/v1760809244/AZU_DOG_FOOD_DRY_-_ALL_STAGES_20KG_-_P3200_vkk1ps.png",
    12: "https://res.cloudinary.com/dlk1dzj2o/image/upload/v1760809249/TOPBREED_DOG_FOOD_DRY_-_PUPPY_1KG_vyfdmy.png",
}
# -----------------------------

# -----------------------------
# STEP 2: Update Inventory records
for inv_id, url in image_map.items():
    try:
        inv = Inventory.objects.get(id=inv_id)
        inv.image = url  # set Cloudinary URL
        inv.save()
        print(f"✅ Updated Inventory {inv_id} -> {url}")
    except Inventory.DoesNotExist:
        print(f"⚠️ Inventory {inv_id} not found")
# -----------------------------

print("✅ Finished updating images!")
