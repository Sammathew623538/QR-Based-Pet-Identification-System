from django.db import models
from django.contrib.auth.models import User
import uuid
import qrcode
from io import BytesIO
from django.core.files import File
from django.utils.text import slugify
from django.utils import timezone
from PIL import Image, ImageDraw
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to="profile", blank=True, null=True)

    def __str__(self):
        return self.user.username

class Pet(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pets')
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100, blank=True, null=True)
    age = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    microchip_number = models.CharField(max_length=100, blank=True, null=True)
    
    # Medical & Emergency
    medical_conditions = models.TextField(blank=True, null=True)
    vaccination_details = models.TextField(blank=True, null=True)
    emergency_contact = models.CharField(max_length=100, blank=True, null=True)
    
    # Media
    image = models.ImageField(upload_to="pets/", blank=True, null=True)
    
    # System Fields
    unique_slug = models.SlugField(unique=True, blank=True)
    qr_code_image = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    lost_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        # Auto-generate unique slug if not exists
        if not self.unique_slug:
            self.unique_slug = slugify(f"{self.name}-{str(uuid.uuid4())[:8]}")

        # Always regenerate QR code to capture updates (e.g., changed profile pic)
        qr_data = f"{settings.BASE_URL}/p/{self.unique_slug}"
        
        # Configure QR with High Error Correction
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white").convert('RGBA')
        
        # Embed Pet Image (Logo) if available
        if self.image:
            try:
                # Ensures the directory for pet images exists
                import os
                pets_dir = os.path.join(settings.MEDIA_ROOT, 'pets')
                os.makedirs(pets_dir, exist_ok=True)

                # Open pet image - handle both file-like and path-like
                icon = Image.open(self.image)
                icon = icon.convert('RGBA')
                
                img_w, img_h = img.size
                factor = 4
                size_w = int(img_w / factor)
                size_h = int(img_h / factor)
                
                icon = icon.resize((size_w, size_h), Image.Resampling.LANCZOS)
                
                mask = Image.new('L', (size_w, size_h), 0)
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0, 0, size_w, size_h), fill=255)
                
                icon_circular = Image.new('RGBA', (size_w, size_h), (0, 0, 0, 0))
                icon_circular.paste(icon, (0, 0), mask=mask)
                
                w = int((img_w - size_w) / 2)
                h = int((img_h - size_h) / 2)
                img.paste(icon_circular, (w, h), icon_circular)
            except Exception as e:
                print(f"Error embedding image in QR: {e}")

        # Save to buffer and reset pointer
        canvas = BytesIO()
        img.save(canvas, format='PNG')
        canvas.seek(0)
        
        file_name = f'qr-{self.unique_slug}.png'
        
        # Ensure directory exists
        import os
        qr_dir = os.path.join(settings.MEDIA_ROOT, 'qr_codes')
        os.makedirs(qr_dir, exist_ok=True)

        try:
            # save=False avoids recursive save() calls
            self.qr_code_image.save(file_name, File(canvas), save=False)
        except Exception as e:
            print(f"Error saving QR code image: {e}")
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class MedicalRecord(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='medical_records')
    vaccine_name = models.CharField(max_length=200)
    vaccination_date = models.DateField()
    next_due_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    document = models.FileField(upload_to='medical_docs/', blank=True, null=True)

    def __str__(self):
        return f"{self.vaccine_name} for {self.pet.name}"

class ScanHistory(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='scan_history')
    scanned_at = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return f"Scan for {self.pet.name} at {self.scanned_at}"

class Order(models.Model):
    DESIGN_CHOICES = (
        ('Classic', 'Classic Black'),
        ('Sporty', 'Sporty Red'),
        ('Luxury', 'Luxury Gold'),
        ('Glow', 'Glow in Dark'),
    )
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='orders')
    full_name = models.CharField(max_length=200)
    shipping_address = models.TextField()
    phone_number = models.CharField(max_length=15)
    design = models.CharField(max_length=20, choices=DESIGN_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    payment_method = models.CharField(max_length=20, default='Cash on Delivery')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} for {self.pet.name} ({self.design})"

class CollarReview(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    design = models.CharField(max_length=50)
    rating = models.IntegerField(default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} - {self.rating}Stars"

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name