import os
import sys
import django
from django.conf import settings
from django.test import Client
from django.urls import reverse

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qrpet.settings')
django.setup()
settings.ALLOWED_HOSTS += ['testserver', '127.0.0.1']

from django.contrib.auth.models import User
from pet.models import Profile

def run_diag(username, email, post_data):
    print(f"\n--- Testing Diag for {username} ---")
    user, _ = User.objects.get_or_create(username=username, email=email)
    user.set_password('pass')
    user.save()
    if not hasattr(user, 'profile'):
        Profile.objects.create(user=user)
        
    client = Client()
    client.login(username=username, password='pass')
    
    response = client.post(reverse('edit_profile'), post_data)
    
    if response.status_code == 302:
        print(f"SUCCESS: Redirected to {response.url}")
    else:
        print(f"FAILURE: Status {response.status_code}")
        if 'u_form' in response.context:
            print("UserUpdateForm Errors:", response.context['u_form'].errors.as_json())
        if 'p_form' in response.context:
            print("ProfileUpdateForm Errors:", response.context['p_form'].errors.as_json())

try:
    # Scenario 1: Basic valid update
    run_diag('tester_valid', 'v@example.com', {
        'username': 'tester_valid',
        'email': 'v@example.com',
        'first_name': 'Valid',
        'last_name': 'Tester',
        'phone': '123456',
        'address': 'Test St'
    })
    
    # Scenario 2: Empty phone and address (should work now)
    run_diag('tester_empty', 'e@example.com', {
        'username': 'tester_empty',
        'email': 'e@example.com',
        'first_name': 'Empty',
        'last_name': 'Tester',
        'phone': '',
        'address': ''
    })

    # Scenario 3: Invalid Email
    run_diag('tester_inv_email', 'ie@example.com', {
        'username': 'tester_inv_email',
        'email': 'not-an-email',
        'first_name': 'Inv',
        'last_name': 'Email',
        'phone': '123',
        'address': 'Test'
    })

except Exception as e:
    print(f"Global Error: {e}")
