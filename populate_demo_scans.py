import os
import django
from datetime import datetime, timedelta
import random

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qrpet.settings')
django.setup()

from pet.models import Pet, ScanHistory
from django.contrib.auth.models import User

def add_demo_scans():
    # Get the first active user
    user = User.objects.filter(is_superuser=False).first()
    if not user:
        print("No user found. Please create a user first.")
        return

    pets = Pet.objects.filter(owner=user)
    if not pets.exists():
        print(f"No pets found for user {user.username}. Please add a pet first.")
        return

    locations = [
        "Kochi, Kerala",
        "Bangalore, Karnataka",
        "Mumbai, Maharashtra",
        "Trivandrum, Kerala",
        "Chennai, Tamil Nadu"
    ]

    ips = [
        "103.252.144.12",
        "157.119.204.58",
        "49.36.128.45",
        "106.51.135.210"
    ]

    print(f"Adding demo scans for user: {user.username}")

    for _ in range(5):
        pet = random.choice(pets)
        loc = random.choice(locations)
        ip = random.choice(ips)
        # Create a scan in the past
        scanned_at = datetime.now() - timedelta(hours=random.randint(1, 48), minutes=random.randint(1, 59))
        
        scan = ScanHistory.objects.create(
            pet=pet,
            scanned_at=scanned_at,
            ip_address=ip,
            location=loc
        )
        print(f"Added scan: {pet.name} at {loc} ({scanned_at.strftime('%Y-%m-%d %H:%M')})")

    print("\nSuccess! Now check your dashboard to see the 'Recent Tag Scans'.")

if __name__ == "__main__":
    add_demo_scans()
