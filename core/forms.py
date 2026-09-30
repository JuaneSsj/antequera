from django import forms
from .models import Client, Measurement, Trainer, ClientImage, BusinessProfile, Profile, Role
from django.contrib.auth.models import User

class BusinessProfileForm(forms.ModelForm):
    class Meta:
        model = BusinessProfile
        fields = ['description', 'instagram_profile', 'tiktok_profile']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class BaseUserForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=False, help_text="Déjalo en blanco para autogenerar el usuario.")
    password = forms.CharField(widget=forms.PasswordInput(render_value=False), required=False, help_text="Ingresa una contraseña para actualizarla. Déjalo en blanco para mantener la actual.")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk and getattr(instance, 'perfil', None) and getattr(instance.perfil, 'usuario', None):
            self.fields['username'].initial = instance.perfil.usuario.username
            self.fields['username'].help_text = "Puedes modificar el nombre de usuario actual aquí."


    def clean_username(self):
        uname = self.cleaned_data.get('username')
        if not uname:
            return uname
            
        instance = getattr(self, 'instance', None)
        user = None
        if instance and getattr(instance, 'perfil', None):
            user = getattr(instance.perfil, 'usuario', None)
            
        qs = User.objects.filter(username=uname)
        if user:
            qs = qs.exclude(pk=user.pk)
            
        if qs.exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso. Elige otro por favor.")
            
        return uname

    def save(self, commit=True):
        instance = super().save(commit=False)
        is_new = instance.pk is None
        
        uname = self.cleaned_data.get('username')
        pwd = self.cleaned_data.get('password')

        if is_new and not instance.perfil:
            if hasattr(self, 'get_default_username') and not uname:
                uname = self.get_default_username()
                
            if not uname:
                uname = "usuario"
                
            counter = 1
            base_uname = uname
            while User.objects.filter(username=uname).exists():
                 uname = f"{base_uname}{counter}"
                 counter += 1
                 
            if not pwd:
                pwd = "usuario123"
            
            user = User.objects.create_user(username=uname, email=self.cleaned_data.get('email', ''), password=pwd)
            role_name = getattr(self, 'role_name', 'Cliente')
            role, _ = Role.objects.get_or_create(nombre_rol=role_name)
            name_val = getattr(instance, 'name', None) or getattr(instance, 'full_name', 'Usuario')
            profile = Profile.objects.create(nombre_per=name_val, rol=role, usuario=user)
            instance.perfil = profile
            
            
        elif instance.perfil and getattr(instance.perfil, 'usuario', None):
            user = instance.perfil.usuario
            updated = False
            if uname and user.username != uname:
                user.username = uname
                updated = True
            if pwd:
                # Si escribió algo en password al editar, asumimos que quiere actualizarlo
                user.set_password(pwd)
                updated = True
                
            if updated:
                user.save()

        if commit:
            instance.save()
            if hasattr(self, 'save_m2m'):
                self.save_m2m()
        return instance

class ClientForm(BaseUserForm):
    role_name = "Cliente"
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and user.is_authenticated:
            is_admin = False
            if user.is_superuser:
                is_admin = True
            elif hasattr(user, 'perfil_app') and user.perfil_app.rol:
                if 'admin' in user.perfil_app.rol.nombre_rol.lower():
                    is_admin = True
            if not is_admin:
                if 'entrenador_asignado' in self.fields:
                    del self.fields['entrenador_asignado']
                    
    class Meta:
        model = Client
        exclude = ['perfil']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }
        
    def get_default_username(self):
        email = self.cleaned_data.get('email')
        phone = self.cleaned_data.get('phone', '')
        fn = self.cleaned_data.get('full_name', '')
        return email.split('@')[0] if email else (fn.split()[0].lower() + phone[-4:]) if phone else fn.replace(" ", "").lower()

class MeasurementForm(forms.ModelForm):
    class Meta:
        model = Measurement
        exclude = ['client']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'rm_date': forms.DateInput(attrs={'type': 'date'}),
            'activity_level': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'fat_percentage': 'Porcentaje de Grasa (%) [Manual / Opcional]',
            'colmen_fat_mass': 'Masa libre de grasa (kg) [Manual / Opcional]',
        }
        help_texts = {
            'fat_percentage': 'Porcentaje medido manualmente (calibrador, báscula, etc.). Deja en blanco si no se midió.',
            'colmen_fat_mass': 'Masa libre de grasa medida. Deja en blanco si no se dispone del dato.',
        }

class TrainerForm(BaseUserForm):
    role_name = "Entrenador"
    
    class Meta:
        model = Trainer
        exclude = ['perfil']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'contact_info': forms.TextInput(attrs={'placeholder': 'Dirección, Ciudad...'}),
        }
        
    def get_default_username(self):
        email = self.cleaned_data.get('email')
        fn = self.cleaned_data.get('name', '')
        return email.split('@')[0] if email else fn.replace(" ", "").lower()

class ClientImageForm(forms.ModelForm):
    class Meta:
        model = ClientImage
        fields = ['image', 'date', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

from .models import TrainerSchedule

class TrainerScheduleForm(forms.ModelForm):
    class Meta:
        model = TrainerSchedule
        fields = ['day_of_week', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }
