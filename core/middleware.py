from django.http import HttpResponseForbidden
from django.urls import resolve
from .models import Route, Access

class DynamicAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        
        # Ignorar rutas estáticas, admin y autenticación
        if path.startswith('/admin/') or path.startswith('/static/') or path.startswith('/media/') or path.startswith('/login/') or path == '/logout/':
            return self.get_response(request)

        # Buscar si la ruta está registrada (usando prefijo más largo para soportar IDs como /clients/1/)
        # Ordenamos por longitud de url_rut de mayor a menor en memoria
        todas_rutas = list(Route.objects.all())
        todas_rutas.sort(key=lambda r: len(r.url_rut), reverse=True)
        
        ruta_db = None
        for r in todas_rutas:
            if path.startswith(r.url_rut):
                ruta_db = r
                break
        
        if ruta_db:
            # Si requiere autenticación o acceso explícito, validamos
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Debes iniciar sesión para acceder a esta ruta.")
            
            # Superusuario siempre tiene acceso
            if request.user.is_superuser:
                return self.get_response(request)
            
            # Revisar si el usuario tiene Perfil
            if not hasattr(request.user, 'perfil_app'):
                return HttpResponseForbidden("Tu usuario no tiene un perfil asociado.")
            
            perfil = request.user.perfil_app
            acceso = Access.objects.filter(perfil=perfil, ruta=ruta_db).first()

            if not acceso:
                return HttpResponseForbidden("No tienes permiso (Access) para ver esta página.")
            
            # Validar métodos POST/PUT/DELETE
            if request.method in ['POST', 'PUT']:
                # Simplificación: asumimos inserta o actualiza
                if acceso.inserta_acc == 'N' and acceso.update_acc == 'N':
                    return HttpResponseForbidden("No tienes permiso para modificar datos en esta ruta.")
            
            if request.method == 'DELETE':
                if acceso.delete_acc == 'N':
                    return HttpResponseForbidden("No tienes permiso para borrar datos en esta ruta.")

        # Si la ruta no está registrada en RUTAS, la dejamos pasar por defecto (o se podría denegar, pero pasar permite que el sistema funcione si olvidan registrar rutas menores)
        return self.get_response(request)
