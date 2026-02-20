
import os
import django
import sys
from django.test import RequestFactory
# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qrpet.settings')
django.setup()

from django.contrib.auth.models import User, AnonymousUser
from pet.models import Pet, ScanHistory
from pet.views import pet_detail_public, dashboard

def verify_flow():
    print("Starting Full Flow Verification...")
    
    # 1. Setup Data
    username = "flow_test_user"
    if User.objects.filter(username=username).exists():
         User.objects.filter(username=username).delete()
    
    user = User.objects.create_user(username=username, password="password123")
    print(f"Created User: {user.username}")

    pet = Pet.objects.create(owner=user, name="FlowPet", breed="TestBreed")
    print(f"Created Pet: {pet.name} (Slug: {pet.unique_slug})")

    # 2. Simulate Public Scan (Anonymous User)
    factory = RequestFactory()
    url = f"/p/{pet.unique_slug}/"
    request = factory.get(url)
    request.user = AnonymousUser()
    
    print(f"Simulating Public Scan at {url}...")
    response = pet_detail_public(request, unique_slug=pet.unique_slug)
    
    if response.status_code == 200:
        print("PASS: Public Profile Page loaded successfully (200 OK).")
    else:
        print(f"FAIL: Public Profile Page returned {response.status_code}.")

    # 3. Verify Scan History
    scans = ScanHistory.objects.filter(pet=pet)
    if scans.exists():
        print(f"PASS: Scan History recorded {scans.count()} visit(s).")
    else:
        print("FAIL: No Scan History recorded.")

    # 4. Verify Dashboard (Logged In User)
    request_dash = factory.get('/dashboard/')
    request_dash.user = user
    response_dash = dashboard(request_dash)
    
    if response_dash.status_code == 200:
        print("PASS: Dashboard loaded successfully for logged-in user.")
        # In a real test we'd check context, but here status code is a good proxy for 'no crash'
    else:
         print(f"FAIL: Dashboard returned {response_dash.status_code}.")

    print("Full Flow Verification Complete.")

if __name__ == "__main__":
    verify_flow()
