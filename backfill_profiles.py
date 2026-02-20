import os
import django
import sys

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qrpet.settings')
django.setup()

from django.contrib.auth.models import User
from pet.models import Profile

def backfill_profiles():
    users = User.objects.all()
    count = 0
    for user in users:
        if not hasattr(user, 'profile'):
            Profile.objects.create(user=user)
            print(f"Created profile for {user.username}")
            count += 1
    print(f"Backfilled {count} profiles.")

if __name__ == "__main__":
    backfill_profiles()
