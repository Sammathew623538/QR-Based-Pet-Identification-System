
import os
import django
import sys

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qrpet.settings')
django.setup()

from django.contrib.auth.models import User
from pet.models import Pet, MedicalRecord, ScanHistory
from django.utils import timezone
import time

def verify():
    print("Starting verification...")
    
    # 1. Create User
    username = f"testuser_{int(time.time())}"
    user = User.objects.create_user(username=username, password="password123")
    print(f"Created User: {user.username}")

    # 2. Create Pet
    pet = Pet.objects.create(
        owner=user,
        name="Buddy",
        breed="Golden Retriever",
        age="2 years",
        gender="Male",
        medical_conditions="None",
        emergency_contact="555-0199"
    )
    print(f"Created Pet: {pet.name}")

    # 3. Verify Auto-Generation
    print(f"Unique Slug: {pet.unique_slug}")
    if pet.unique_slug:
        print("PASS: Slug generated automatically.")
    else:
        print("FAIL: Slug not generated.")

    print(f"QR Code Path: {pet.qr_code_image}")
    if pet.qr_code_image:
        print("PASS: QR Code generated automatically.")
    else:
        print("FAIL: QR Code not generated.")

    # 4. Create Medical Record
    med_record = MedicalRecord.objects.create(
        pet=pet,
        vaccine_name="Rabies",
        vaccination_date=timezone.now().date(),
        notes="Annual shot"
    )
    print(f"Created Medical Record: {med_record}")

    # 5. Create Scan History
    scan = ScanHistory.objects.create(
        pet=pet,
        location="Central Park, NY",
        ip_address="192.168.1.1"
    )
    print(f"Created Scan History: {scan}")

    print("Verification Complete.")

if __name__ == "__main__":
    verify()
