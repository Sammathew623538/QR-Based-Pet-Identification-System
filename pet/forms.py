from django import forms
from .models import Contact, Pet, MedicalRecord, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address', 'image']

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        exclude = ['owner', 'unique_slug', 'qr_code_image', 'lost_status', 'created_at']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pet Name'}),
            'breed': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Breed'}),
            'age': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Age (e.g. 2 years)'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Color'}),
            'microchip_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional'}),
            'medical_conditions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Allergies, chronic conditions...'}),
            'vaccination_details': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Recent vaccinations...'}),
            'emergency_contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Emergency Phone'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class MedicalRecordForm(forms.ModelForm):
    vaccination_date = forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    next_due_date = forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})

    class Meta:
        model = MedicalRecord
        fields = ['vaccine_name', 'vaccination_date', 'next_due_date', 'notes', 'document']
        widgets = {
            'vaccine_name': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'document': forms.FileInput(attrs={'class': 'form-control'}),
        }
