from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, Http404, FileResponse, JsonResponse
from .models import Pet, MedicalRecord, ScanHistory, Contact, Profile, Order, CollarReview
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, ContactForm, PetForm, MedicalRecordForm
from django.utils import timezone
from PIL import Image
import os
import requests
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
import json



# --- STATIC PAGES ---
def home(request):
    public_reviews = CollarReview.objects.all().order_by('-created_at')[:4]
    return render(request, 'main.html', {'public_reviews': public_reviews})

def aboutpage(request):
    return render(request, 'about.html')

def contactpage(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'message': 'Message sent successfully!', 'redirect_url': '/' })
            messages.success(request, 'Message sent successfully!')
            return redirect('home')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def how_it_works(request):
    return render(request, 'how_it_works.html')

# --- AUTHENTICATION ---
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now login.')
            login(request, user) # Auto-login after register
            return redirect('dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def logoutpage(request):
    logout(request)
    return redirect('home')

@login_required
def deactivate_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, 'Your account has been successfully deactivated.')
        return redirect('home')
    return redirect('profile')

# --- USER DASHBOARD & PROFILE ---
@login_required
def dashboard(request):
    try:
        # Failsafe: Create profile if missing
        if not hasattr(request.user, 'profile'):
            Profile.objects.create(user=request.user, phone='', address='')
    except Exception as e:
        print(f"Error checking/creating profile: {e}")

    try:
        pets = Pet.objects.filter(owner=request.user)
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        
        # Calculate Real Stats
        total_scans = ScanHistory.objects.filter(pet__owner=request.user).count()
        lost_pets_count = pets.filter(lost_status=True).count()
        
        # Fetch recent scans
        recent_scans = ScanHistory.objects.filter(pet__owner=request.user).order_by('-scanned_at')[:10]
        
        context = {
            'pets': pets,
            'orders': orders,
            'total_scans': total_scans,
            'lost_pets_count': lost_pets_count,
            'total_pets': pets.count(),
            'recent_scans': recent_scans,
        }
        
        return render(request, 'dashboard.html', context)
    except Exception as e:
        print(f"DASHBOARD ERROR: {e}")
        # In production, returning a simple error page or message is better than 500
        return HttpResponse(f"Error loading dashboard: {e}")

@login_required
def profile_view(request):
    try:
        # Ensure profile exists (failsafe)
        if not hasattr(request.user, 'profile'):
            Profile.objects.create(user=request.user, phone='', address='')
    except Exception:
        pass
    
    
    # Get user's pets to display on profile
    pets = Pet.objects.filter(owner=request.user)
    
    context = {
        'pets': pets
    }
    
    return render(request, 'accounts/profile.html', context)

@login_required
def edit_profile(request):
    try:
        # Failsafe: Create profile if missing
        if not hasattr(request.user, 'profile'):
            Profile.objects.create(user=request.user, phone='', address='')
    except Exception:
        pass

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'accounts/edit_profile.html', context)

# --- PET MANAGEMENT ---
@login_required
def pet_create(request):
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                pet = form.save(commit=False)
                pet.owner = request.user
                pet.save()
                messages.success(request, f'{pet.name} has been added!')
                return redirect('dashboard')
            except Exception as e:
                print(f"Error adding pet: {e}")
                messages.error(request, f"Error adding pet: {e}")
    else:
        form = PetForm()
    return render(request, 'pet_form.html', {'form': form, 'title': 'Add Pet'})

@login_required
def pet_update(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    if pet.owner != request.user and not request.user.is_staff:
        raise Http404("You are not allowed to edit this pet.")

    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            messages.success(request, f'{pet.name} details updated!')
            return redirect('dashboard') if not request.user.is_staff else redirect('staff_dashboard')
    else:
        form = PetForm(instance=pet)
    return render(request, 'pet_form.html', {'form': form, 'title': 'Edit Pet'})

@login_required
def pet_delete(request, pk):
    print(f"Attempting to delete pet {pk} by user {request.user}")
    pet = get_object_or_404(Pet, pk=pk)
    if pet.owner != request.user and not request.user.is_staff:
        print(f"Permission denied: Pet owner {pet.owner} != Request user {request.user}")
        raise Http404("You are not allowed to delete this pet.")

    if request.method == 'POST':
        pet.delete()
        messages.success(request, 'Pet removed successfully.')
        return redirect('dashboard') if not request.user.is_staff else redirect('staff_dashboard')
    return render(request, 'pet_confirm_delete.html', {'pet': pet})

@login_required
def toggle_lost_mode(request, pk):
    pet = get_object_or_404(Pet, pk=pk, owner=request.user)
    pet.lost_status = not pet.lost_status
    pet.save()
    status = "Active" if pet.lost_status else "Inactive"
    if pet.lost_status:
        messages.warning(request, f'Lost Mode is now {status} for {pet.name}. You can now download the MISSING poster from the pet menu.')
    else:
        messages.success(request, f'Lost Mode is now {status} for {pet.name}. Glad your pet is safe!')
    return redirect('dashboard')

@login_required
def download_qr(request, pk):
    pet = get_object_or_404(Pet, pk=pk, owner=request.user)
    if pet.qr_code_image:
        return FileResponse(pet.qr_code_image.open(), as_attachment=True, filename=f'qr_{pet.name}.png')
    raise Http404("QR Code not found")

# --- STAFF DASHBOARD ---
@login_required
def staff_dashboard(request):
    if not request.user.is_staff:
        messages.error(request, "Access denied. Staff only area.")
        return redirect('dashboard')
    
    today = timezone.now().date()
    context = {
        'total_users': User.objects.count(),
        'total_pets': Pet.objects.count(),
        'total_scans': ScanHistory.objects.count(),
        'total_orders': Order.objects.count(),
        'scans_today': ScanHistory.objects.filter(scanned_at__date=today).count(),
        'recent_users': User.objects.order_by('-date_joined')[:5],
        'recent_pets': Pet.objects.order_by('-created_at')[:5],
        'recent_scans': ScanHistory.objects.order_by('-scanned_at')[:5],
        'recent_orders': Order.objects.order_by('-created_at')[:5],
    }
    return render(request, 'staff_dashboard_v2.html', context)

@login_required
def staff_edit_user(request, pk):
    if not request.user.is_staff:
        messages.error(request, "Access denied.")
        return redirect('dashboard')
    
    target_user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=target_user)
        # Assuming Profile exists as it's created on signal or manually
        profile, created = Profile.objects.get_or_create(user=target_user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"User {target_user.username} updated successfully!")
            return redirect('staff_dashboard')
    else:
        u_form = UserUpdateForm(instance=target_user)
        profile, created = Profile.objects.get_or_create(user=target_user)
        p_form = ProfileUpdateForm(instance=profile)
        
    return render(request, 'staff_edit_user.html', {
        'u_form': u_form,
        'p_form': p_form,
        'target_user': target_user
    })

@login_required
def staff_delete_user(request, pk):
    if not request.user.is_staff:
        messages.error(request, "Access denied.")
        return redirect('dashboard')
    
    user_to_delete = get_object_or_404(User, pk=pk)
    if user_to_delete.is_staff:
        messages.error(request, "Cannot delete other staff/admin accounts.")
        return redirect('staff_dashboard')
    
    if request.method == 'POST':
        user_to_delete.delete()
        messages.success(request, f"User {user_to_delete.username} has been deleted.")
        return redirect('staff_dashboard')
    
    return render(request, 'pet_confirm_delete.html', {'pet': None, 'custom_obj': user_to_delete, 'verb': 'Delete User'})

@login_required
def staff_users_list(request):
    if not request.user.is_staff:
        messages.error(request, "Access denied.")
        return redirect('dashboard')
    
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'staff_users_list.html', {'users': users})

# --- MEDICAL RECORDS ---
@login_required
def medical_records(request, pk):
    pet = get_object_or_404(Pet, pk=pk, owner=request.user)
    records = MedicalRecord.objects.filter(pet=pet).order_by('-vaccination_date')
    
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST, request.FILES)
        if form.is_valid():
            record = form.save(commit=False)
            record.pet = pet
            record.save()
            messages.success(request, 'Medical record added!')
            return redirect('medical_records', pk=pk)
    else:
        form = MedicalRecordForm()
    
    return render(request, 'medical_records.html', {'pet': pet, 'records': records, 'form': form})

# --- PUBLIC PROFILE & SCAN TRACKING ---



def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_location_from_ip(ip):
    try:
        # Use ip-api.com, which is free for non-commercial use (up to 45 requests/minute)
        if ip == '127.0.0.1': return "Localhost Test"
        
        # In production (e.g. Heroku), x-forwarded-for might have comma separated values
        # We handle this in get_client_ip, but for good measure:
        clean_ip = ip.split(',')[0].strip()

        # Timeout added to avoid hanging requests if the API is slow
        response = requests.get(f"http://ip-api.com/json/{clean_ip}?fields=status,city,regionName,country,lat,lon", timeout=5)
        data = response.json()
        
        if data.get('status') == 'success':
            city = data.get('city', 'Unknown City')
            region = data.get('regionName', '')
            country = data.get('country', '')
            return f"{city}, {region}, {country}"
    except Exception as e:
        print(f"Location Error: {e}")
        pass
    return "Unknown Location"

def pet_detail_public(request, unique_slug):
    pet = get_object_or_404(Pet, unique_slug=unique_slug)
    
    # Track Scan
    print(f"TRACKING: Scan attempted for {pet.name} by user {request.user}")
    ip = get_client_ip(request)
    location_data = get_location_from_ip(ip) # Real Location
    
    ScanHistory.objects.create(
        pet=pet,
        ip_address=ip,
        location=location_data
    )

    # --- EMAIL NOTIFICATION SYSTEM ---
    try:
        from django.core.mail import send_mail
        from django.conf import settings
        
        subject = f"ALERT: Your pet {pet.name} was just scanned!"
        message = f"""
        Warning!
        
        Your pet '{pet.name}' was just scanned.
        
        Time: {timezone.now()}
        Location Estimate: {location_data}
        IP Address: {ip}
        
        If this wasn't you, please check your pet's safety.
        
        - Smart Pet QR Safety System
        """
        
        # Send email to the pet owner
        if pet.owner.email:
            print(f"SENDING EMAIL ALERT TO {pet.owner.email}...")
            send_mail(
                subject,
                message,
                'noreply@smartpetqr.com',
                [pet.owner.email],
                fail_silently=True,
            )
            print("EMAIL SENT SUCCESSFULLY")
    except Exception as e:
        print(f"Email Error: {e}")
    
    # Determine the best phone number to display
    display_phone = None
    try:
        if hasattr(pet.owner, 'profile') and pet.owner.profile.phone:
            display_phone = pet.owner.profile.phone
    except Exception:
        pass
        
    if not display_phone:
        display_phone = pet.emergency_contact
    
    return render(request, 'pet_detail_public.html', {
        'pet': pet, 
        'display_phone': display_phone,
        'is_public_view': True
    })

@login_required
def place_order(request):
    print("DEBUG: place_order called", request.method)
    if request.method == 'POST':
        try:
            pet_id = request.POST.get('pet_id')
            design = request.POST.get('design')
            full_name = request.POST.get('full_name')
            shipping_address = request.POST.get('shipping_address')
            phone_number = request.POST.get('phone_number')
            
            if not pet_id:
                return JsonResponse({'status': 'error', 'message': 'Missing Pet ID.'})

            try:
                pet = Pet.objects.get(id=pet_id, owner=request.user)
            except (Pet.DoesNotExist, ValueError):
                return JsonResponse({'status': 'error', 'message': 'Pet not found or unauthorized.'})

            order = Order.objects.create(
                user=request.user,
                pet=pet,
                full_name=full_name,
                phone_number=phone_number,
                shipping_address=shipping_address,
                design=design
            )
            
            from django.urls import reverse
            return JsonResponse({
                'status': 'success', 
                'redirect_url': reverse('order_success', kwargs={'order_id': order.id})
            })
        except Exception as e:
            # Helpful for debugging in terminal
            print(f"ORDER ERROR: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': f"Internal Server Error: {str(e)}"
            })
    return JsonResponse({'status': 'error', 'message': 'Only POST requests allowed.'})

@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Estimated delivery: 7-10 days
    from datetime import timedelta
    est_delivery_start = order.created_at + timedelta(days=7)
    est_delivery_end = order.created_at + timedelta(days=10)
    
    context = {
        'order': order,
        'shipping_addr': order.shipping_address,
        'est_delivery_start': est_delivery_start,
        'est_delivery_end': est_delivery_end,
    }
    return render(request, 'order_success.html', context)

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    # Fetch reviews for the specific design
    design_reviews = CollarReview.objects.filter(design=order.design).order_by('-created_at')[:10]
    
    # Check if user has already reviewed
    user_has_reviewed = CollarReview.objects.filter(user=request.user, pet=order.pet, design=order.design).exists()
    
    return render(request, 'order_detail.html', {
        'order': order,
        'design_reviews': design_reviews,
        'user_has_reviewed': user_has_reviewed,
    })

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.status in ['Pending', 'Processing']:
        order.status = 'Cancelled'
        order.save()
        messages.success(request, f"Order #ORD-{order.id} has been cancelled.")
    else:
        messages.error(request, f"Order #ORD-{order.id} cannot be cancelled at this stage.")
        
    return redirect('order_detail', order_id=order.id)

@login_required
def collar_review(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'collar_review.html', {'order': order})

@login_required
def submit_review(request):
    if request.method == 'POST':
        try:
            order_id = request.POST.get('order_id')
            rating = request.POST.get('rating')
            comment = request.POST.get('comment')
            
            order = get_object_or_404(Order, id=order_id, user=request.user)
            
            CollarReview.objects.create(
                user=request.user,
                pet=order.pet,
                design=order.design,
                rating=rating,
                comment=comment
            )
            
            return JsonResponse({'status': 'success', 'message': 'Review submitted! Thank you.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid method.'})

@login_required
def all_reviews(request):
    reviews = CollarReview.objects.all().order_by('-created_at')
    return render(request, 'all_reviews.html', {'reviews': reviews})

@login_required
def download_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {
        'order': order,
        'invoice_date': order.created_at,
        'invoice_number': f"INV-2024-{order.id:04d}"
    }
    return render(request, 'invoice.html', context)

@login_required
def generate_lost_poster(request, pk):
    pet = get_object_or_404(Pet, pk=pk, owner=request.user)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="MISSING_POSTER_{pet.name}.pdf"'

    p_w, p_h = A4
    c = canvas.Canvas(response, pagesize=A4)
    
    # --- COLORS ---
    C_BG = colors.HexColor("#FFEB3B")      # Vivid Yellow
    C_BLACK = colors.HexColor("#000000")
    C_RED = colors.HexColor("#D50000")     # Strong Red
    C_WHITE = colors.HexColor("#FFFFFF")
    
    # 1. Background
    c.setFillColor(C_BG)
    c.rect(0, 0, p_w, p_h, fill=1, stroke=0)
    
    # Center X for main text
    cx = p_w / 2 
    
    # 2. Header
    c.setFillColor(C_BLACK)
    c.setFont("Helvetica-Bold", 90)
    c.drawCentredString(p_w/2, p_h - 90, "MISSING")
    
    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(p_w/2, p_h - 130, "PLEASE HELP BRING ME HOME")
    
    # 3. Photo Area - Slightly Smaller to fit everything
    img_w = 460
    img_h = 340 # Reduced height
    img_x = (p_w - img_w) / 2
    img_y = 360 # Top at ~700
    
    # Black Border
    c.setFillColor(C_BLACK)
    c.rect(img_x - 6, img_y - 6, img_w + 12, img_h + 12, fill=1, stroke=0)
    
    # White canvas
    c.setFillColor(C_WHITE)
    c.rect(img_x, img_y, img_w, img_h, fill=1, stroke=0)
    
    if pet.image:
        try:
            img_path = pet.image.path
            with Image.open(img_path) as pimg:
                w, h = pimg.size
                aspect = h / w
                display_w = img_w
                display_h = display_w * aspect
                if display_h > img_h:
                    display_h = img_h
                    display_w = display_h / aspect
                dx = img_x + (img_w - display_w) / 2
                dy = img_y + (img_h - display_h) / 2
                c.drawImage(img_path, dx, dy, width=display_w, height=display_h)
        except: pass

    # 4. Pet Name
    c.setFillColor(C_RED)
    c.setFont("Helvetica-Bold", 60)
    c.drawCentredString(cx, 290, pet.name.upper()) 
    
    # 5. Details Section
    # Shift text slightly left to avoid hitting QR code on the right if it gets tight
    text_cx = cx - 30 
    
    c.setFillColor(C_BLACK)
    c.setFont("Helvetica-Bold", 19)
    
    def safe_str(val): return str(val or "N/A")
    c.drawCentredString(text_cx, 260, f"{safe_str(pet.breed)}  •  {safe_str(pet.color)}")
    c.drawCentredString(text_cx, 235, f"{safe_str(pet.gender)}  •  Age: {safe_str(pet.age)}")
    
    # Owner Mobile
    try:
        if hasattr(request.user, 'profile') and request.user.profile.phone:
            owner_phone = request.user.profile.phone
        else:
            owner_phone = None
    except: owner_phone = None
    
    if not owner_phone: owner_phone = pet.emergency_contact
    final_phone = owner_phone if owner_phone else "No Phone"

    c.setFont("Helvetica-Bold", 21)
    c.drawCentredString(text_cx, 205, f"Owner Mobile: {final_phone}")

    # 6. Reward Badge
    r_x = p_w - 70
    r_y = p_h - 70
    r_r = 55
    c.setFillColor(C_RED)
    c.circle(r_x, r_y, r_r, fill=1, stroke=1)
    c.setStrokeColor(C_WHITE)
    c.setLineWidth(3)
    c.circle(r_x, r_y, r_r - 4, fill=0, stroke=1)
    c.setFillColor(C_WHITE)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(r_x, r_y + 8, "REWARD")
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(r_x, r_y - 10, "OFFERED")

    # 7. Contact Section (Black Bar)
    bar_h = 130
    c.setFillColor(C_BLACK)
    c.rect(0, 0, p_w, bar_h, fill=1, stroke=0)
    
    c.setFillColor(C_BG)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(p_w/2, 100, "IF SEEN PLEASE CALL IMMEDIATELY")
    
    c.setFont("Helvetica-Bold", 65)
    c.drawCentredString(p_w/2, 35, final_phone)
    
    # 8. QR Code - Bottom Right, safely positioned
    if pet.qr_code_image:
        try:
            qc_size = 90
            qc_x = p_w - qc_size - 15
            qc_y = bar_h + 15 # Starts at y=145
            
            # White backing
            c.setFillColor(C_WHITE)
            c.rect(qc_x - 5, qc_y - 5, qc_size + 10, qc_size + 10, fill=1, stroke=1)
            c.drawImage(pet.qr_code_image.path, qc_x, qc_y, width=qc_size, height=qc_size)
            
            c.setFillColor(C_BLACK)
            c.setFont("Helvetica-Bold", 8)
            c.drawCentredString(qc_x + qc_size/2, qc_y - 4, "SCAN INFO") 
        except: pass

    c.showPage()
    c.save()
    return response

@login_required
def poster_preview(request, pk):
    pet = get_object_or_404(Pet, pk=pk, owner=request.user)
    return render(request, 'lost_poster_preview.html', {'pet': pet})

@login_required
def delete_scan(request, pk):
    scan = get_object_or_404(ScanHistory, pk=pk, pet__owner=request.user)
    if request.method == 'POST':
        scan.delete()
        messages.success(request, 'Scan history entry deleted successfully.')
    return redirect('dashboard')

@login_required
def delete_order(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    # Only allow deleting cancelled orders to keep history clean
    if order.status == 'Cancelled':
        order.delete()
        messages.success(request, 'Order removed from history.')
    else:
        messages.error(request, 'Only cancelled orders can be removed.')
    return redirect('dashboard')
