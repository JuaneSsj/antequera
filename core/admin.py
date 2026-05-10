from django.contrib import admin
from .models import (
    Role, Profile, Route, Access, 
    Trainer, Client, Measurement, ClientImage, 
    BusinessProfile, TrainingSession, NotificationLog
)
from .forms import ClientForm, TrainerForm

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_rol')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_per', 'rol', 'usuario')

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_rut', 'url_rut')

@admin.register(Access)
class AccessAdmin(admin.ModelAdmin):
    list_display = ('id', 'perfil', 'ruta', 'inserta_acc', 'update_acc', 'delete_acc')

@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    form = TrainerForm
    list_display = ('id', 'name', 'perfil')

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    form = ClientForm
    list_display = ('id', 'full_name', 'perfil', 'entrenador_asignado')

@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'date', 'weight', 'imc')

@admin.register(ClientImage)
class ClientImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'date')

@admin.register(BusinessProfile)
class BusinessProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'description')

@admin.register(TrainingSession)
class TrainingSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'entrenador', 'fecha_hora', 'estado')
    list_filter = ('estado', 'fecha_hora', 'entrenador')

@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'sesion', 'fecha_programada', 'estado_envio')
