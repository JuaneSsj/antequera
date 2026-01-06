from django import forms
from .models import Client, Measurement, Trainer, ClientImage, BusinessProfile

class BusinessProfileForm(forms.ModelForm):
    class Meta:
        model = BusinessProfile
        fields = ['description', 'instagram_profile', 'tiktok_profile']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

class MeasurementForm(forms.ModelForm):
    class Meta:
        model = Measurement
        exclude = ['client', 'imc', 'imc_category', 'basal_metabolic_rate', 'total_caloric_expenditure']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'rm_date': forms.DateInput(attrs={'type': 'date'}),
            'activity_level': forms.Select(attrs={'class': 'form-select'}),
        }

class TrainerForm(forms.ModelForm):
    class Meta:
        model = Trainer
        fields = ['name', 'bio', 'contact_info', 'email', 'phone', 'profile_picture']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'contact_info': forms.TextInput(attrs={'placeholder': 'Dirección, Ciudad...'}),
        }

class ClientImageForm(forms.ModelForm):
    class Meta:
        model = ClientImage
        fields = ['image', 'date', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
