from django.contrib import admin
from .models import Profile, Pet, MedicalRecord, ScanHistory, Contact, Order, CollarReview

# --- Custom Admin Site Branding ---
admin.site.site_header = "PetQR Administration"
admin.site.site_title = "PetQR Admin Portal"
admin.site.index_title = "Welcome to PetQR Management"

# --- Inlines ---
class MedicalRecordInline(admin.TabularInline):
    model = MedicalRecord
    extra = 0
    classes = ('collapse',)

class ScanHistoryInline(admin.TabularInline):
    model = ScanHistory
    extra = 0
    readonly_fields = ('scanned_at', 'ip_address', 'location')
    classes = ('collapse',)
    can_delete = False

class PetInline(admin.TabularInline):
    model = Pet
    extra = 0
    fields = ('name', 'breed', 'lost_status')
    readonly_fields = ('unique_slug',)
    show_change_link = True

# --- Model Admins ---

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address', 'pet_count')
    search_fields = ('user__username', 'user__email', 'phone')
    list_filter = ('user__is_active', 'user__date_joined')

    def pet_count(self, obj):
        return obj.user.pets.count()
    pet_count.short_description = 'Pets Owned'

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'breed', 'lost_status', 'created_at', 'scan_count')
    list_filter = ('lost_status', 'gender', 'created_at')
    search_fields = ('name', 'owner__username', 'owner__email', 'microchip_number', 'unique_slug')
    inlines = [MedicalRecordInline, ScanHistoryInline]
    readonly_fields = ('unique_slug', 'qr_code_image', 'created_at')
    date_hierarchy = 'created_at'
    list_per_page = 20
    actions = ['mark_lost', 'mark_found', 'regenerate_qr_code']

    def scan_count(self, obj):
        return obj.scan_history.count()
    scan_count.short_description = 'Total Scans'

    @admin.action(description='Mark selected pets as LOST 🚨')
    def mark_lost(self, request, queryset):
        queryset.update(lost_status=True)

    @admin.action(description='Mark selected pets as FOUND ✅')
    def mark_found(self, request, queryset):
        queryset.update(lost_status=False)
        
    @admin.action(description='Regenerate QR Codes (Update URL) 🔄')
    def regenerate_qr_code(self, request, queryset):
        count = 0
        for pet in queryset:
            pet.save() # Trigger save() which regenerates QR
            count += 1
        self.message_user(request, f"Successfully regenerated QR codes for {count} pets.")

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('pet', 'vaccine_name', 'vaccination_date', 'next_due_date')
    list_filter = ('vaccination_date', 'next_due_date')
    search_fields = ('pet__name', 'vaccine_name', 'pet__owner__username')
    date_hierarchy = 'vaccination_date'

@admin.register(ScanHistory)
class ScanHistoryAdmin(admin.ModelAdmin):
    list_display = ('pet', 'scanned_at', 'location', 'ip_address')
    list_filter = ('scanned_at',)
    search_fields = ('pet__name', 'location', 'ip_address')
    readonly_fields = ('scanned_at', 'ip_address', 'location')
    date_hierarchy = 'scanned_at'

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'short_message')
    search_fields = ('name', 'email', 'message')
    
    def short_message(self, obj):
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message
    short_message.short_description = 'Message Preview'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'pet', 'design', 'status', 'created_at', 'amount_display')
    list_filter = ('status', 'design', 'created_at')
    search_fields = ('user__username', 'pet__name', 'full_name', 'phone_number')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    actions = ['mark_shipped', 'mark_delivered', 'mark_cancelled']

    def amount_display(self, obj):
        # Assuming fixed price for now as it's not in the model
        return "$29.99" 
    amount_display.short_description = 'Value'

    @admin.action(description='Mark selected orders as SHIPPED 🚚')
    def mark_shipped(self, request, queryset):
        queryset.update(status='Shipped')

    @admin.action(description='Mark selected orders as DELIVERED ✅')
    def mark_delivered(self, request, queryset):
        queryset.update(status='Delivered')

    @admin.action(description='Mark selected orders as CANCELLED ❌')
    def mark_cancelled(self, request, queryset):
        queryset.update(status='Cancelled')

@admin.register(CollarReview)
class CollarReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'pet', 'rating', 'design', 'created_at')
    list_filter = ('rating', 'design')
    search_fields = ('user__username', 'pet__name', 'comment')
