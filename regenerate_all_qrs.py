import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qrpet.settings")
django.setup()

from pet.models import Pet

print(f"Starting QR code regeneration for {Pet.objects.count()} pets...")

for pet in Pet.objects.all():
    print(f"Updating QR for {pet.name}...")
    pet.save()

print("All QR codes updated successfully!")
