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
        {"nombre": "Archivo de Clientes", "url": "/clients/archive/"},
        {"nombre": "Agenda Entrenador", "url": "/agenda/trainer/"},
        {"nombre": "Reservar Cliente", "url": "/agenda/client/"},
        {"nombre": "Estado Sesión", "url": "/agenda/session/"},
        {"nombre": "Detalle Entrenador", "url": "/trainer/"},
        {"nombre": "Horario Entrenador", "url": "/trainer/schedule/"},
        {"nombre": "Información del Negocio", "url": "/business/"},
    ]

    rutas_creadas = []
    for r in rutas_def:
        ruta, _ = Route.objects.get_or_create(url_rut=r["url"], defaults={"nombre_rut": r["nombre"]})
        rutas_creadas.append(ruta)

    print("Rutas creadas en Base de Datos.")

    def ensure_access(perfil, ruta, inserta='N', update='N', delete='N'):
        access, created = Access.objects.get_or_create(
            perfil=perfil,
            ruta=ruta,
            defaults={
                "inserta_acc": inserta,
                "update_acc": update,
                "delete_acc": delete,
            }
        )
        if not created:
            access.inserta_acc = inserta
            access.update_acc = update
            access.delete_acc = delete
            access.save()

    if not admin_perfil:
         print("Asegúrate de atar tu superusuario a un Perfil de 'Admin' en el panel para tener acceso total explícito (aunque el middleware te lo perdone).")
    else:
        for r in rutas_creadas:
            ensure_access(admin_perfil, r, inserta='S', update='S', delete='S')
        print("Accesos completos dados al Admin principal.")

    # Asignar accesos a perfiles existentes según su rol
    from core.models import get_default_routes_for_role
    for perfil in Profile.objects.all():
        role_name = perfil.rol.nombre_rol
        routes_perms = get_default_routes_for_role(role_name)
        for url, perms in routes_perms.items():
            ruta = Route.objects.filter(url_rut=url).first()
            if ruta:
                ensure_access(perfil, ruta, inserta=perms['inserta'], update=perms['update'], delete=perms['delete'])

    print("Accesos básicos asignados a entrenadores y clientes existentes.")

if __name__ == '__main__':
    seed_routes()
