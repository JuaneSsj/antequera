import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gym_project.settings')
django.setup()

from core.models import Route, Access, Role, Profile
from django.contrib.auth.models import User

def seed_routes():
    # Roles
    admin_rol, _ = Role.objects.get_or_create(nombre_rol="Admin")
    entrenador_rol, _ = Role.objects.get_or_create(nombre_rol="Entrenador")
    cliente_rol, _ = Role.objects.get_or_create(nombre_rol="Cliente")
    
    # Perfiles Base
    admin_user = User.objects.filter(is_superuser=True).first()
    admin_perfil = admin_user.perfil_app if admin_user and hasattr(admin_user, 'perfil_app') else None

    # Definir Rutas
    rutas_def = [
        {"nombre": "Dashboard Principal", "url": "/"},
        {"nombre": "Lista de Clientes", "url": "/clients/"},
        {"nombre": "Detalle/Edición Cliente", "url": "/clients/"},  # Cubre /clients/1/
        {"nombre": "Crear Cliente", "url": "/clients/new/"},
        {"nombre": "Agenda Entrenador", "url": "/agenda/trainer/"},
        {"nombre": "Reservar Cliente", "url": "/agenda/client/"},
        {"nombre": "Detalle Entrenador", "url": "/trainer/"},
        {"nombre": "Información del Negocio", "url": "/business/"},
    ]

    rutas_creadas = []
    for r in rutas_def:
        ruta, _ = Route.objects.get_or_create(url_rut=r["url"], defaults={"nombre_rut": r["nombre"]})
        rutas_creadas.append(ruta)

    print("Rutas creadas en Base de Datos.")

    def ensure_access(perfil, ruta, inserta='N', update='N', delete='N'):
        Access.objects.get_or_create(
            perfil=perfil,
            ruta=ruta,
            defaults={
                "inserta_acc": inserta,
                "update_acc": update,
                "delete_acc": delete,
            }
        )

    if not admin_perfil:
         print("Asegúrate de atar tu superusuario a un Perfil de 'Admin' en el panel para tener acceso total explícito (aunque el middleware te lo perdone).")
    else:
        for r in rutas_creadas:
            Access.objects.get_or_create(perfil=admin_perfil, ruta=r, defaults={"inserta_acc": 'S', "update_acc": 'S', "delete_acc": 'S'})
        print("Accesos completos dados al Admin principal.")

    # Asignar accesos a perfiles existentes según su rol
    trainer_route_urls = ['/', '/clients/', '/clients/new/', '/agenda/trainer/', '/clients/archive/', '/trainer/']
    cliente_route_urls = ['/', '/agenda/client/', '/trainer/']

    for perfil in Profile.objects.filter(rol=entrenador_rol):
        for ruta_url in trainer_route_urls:
            ruta = Route.objects.filter(url_rut=ruta_url).first()
            if ruta:
                delete_perm = 'S' if ruta_url == '/clients/' else 'N'
                ensure_access(perfil, ruta, inserta='S', update='S', delete=delete_perm)

    for perfil in Profile.objects.filter(rol=cliente_rol):
        for ruta_url in cliente_route_urls:
            ruta = Route.objects.filter(url_rut=ruta_url).first()
            if ruta:
                ensure_access(perfil, ruta, inserta='N', update='N', delete='N')

    print("Accesos básicos asignados a entrenadores y clientes existentes.")

if __name__ == '__main__':
    seed_routes()
