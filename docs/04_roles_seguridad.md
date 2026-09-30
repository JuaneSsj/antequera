# Roles y Seguridad

El sistema está diseñado desde su núcleo para ser multi-rol, restringiendo el acceso a vistas, menús y datos dependiendo del tipo de usuario que ha iniciado sesión.

## 1. Autenticación Base
- El login y logout se manejan a través de las vistas estándar de autenticación de Django (`auth_views.LoginView` y `LogoutView`), lo que garantiza la seguridad y encriptación de las contraseñas.
- Si un usuario no está autenticado e intenta entrar, es redirigido a la pantalla de login.

## 2. Control de Acceso Basado en Roles (RBAC)
Cada cuenta (`User`) puede tener asociado un `Profile` (Perfil), y este perfil se enmarca en un `Role` (Rol). Los permisos fluyen en base a tres roles principales:

1. **Administrador**: Posee privilegios globales. Puede ver el panel general, la lista de todos los clientes de todos los entrenadores, modificar perfiles corporativos e información genérica.
2. **Entrenador**: Su visión es departamentalizada. El sistema lo enruta a su agenda y (en principio de diseño) solo debería manipular a sus clientes asignados.
3. **Cliente**: Su visión es personal. Solo puede acceder a su propio detalle de mediciones, gráficas e imágenes, y agendar horas exclusivamente con su entrenador.

## 3. Mecanismos de Seguridad Implementados
El proyecto aplica la seguridad en varias capas complementarias:

- **Asignación Automática de Accesos (Signals)**: Se implementó un signal `post_save` en el modelo `Profile` que se activa en tiempo de creación del perfil. Este signal asocia de manera automática las rutas estándar correspondientes al rol del usuario (evitando errores manuales de registro):
  - **Entrenadores**: Obtienen acceso a `/clients/`, `/agenda/trainer/`, `/trainer/schedule/` (disponibilidad), etc.
  - **Clientes**: Obtienen acceso a `/agenda/client/`, `/agenda/session/` (cancelaciones), etc.
  - **Admins**: Acceso completo a todas las rutas.
- **Filtro de Clientes Asignados (`get_visible_clients`)**: En `core/views.py`, se implementó el filtro `get_visible_clients`. Todas las vistas de clientes (listados, activos, archivados, detalles, edición, fotos y mediciones) utilizan esta función. Si un Entrenador intenta manipular o ver información de un cliente asignado a otro entrenador (incluso escribiendo directamente el ID en la URL), el sistema responderá con un error HTTP 404 (Not Found).
- **Middleware Dinámico (`DynamicAccessMiddleware`)**: En `settings.py` existe un middleware personalizado. Este guardián intercepta cada petición web, verifica en la base de datos de permisos (`Access`) si el perfil del usuario tiene habilitada la ruta solicitada (`Route`), y bloquea el paso con un error HTTP 403 (Forbidden) si no posee los permisos.

## 4. Asignaciones e Interfaz Contextuales (Campos Implícitos)
- Para evitar que un Entrenador deba seleccionarse a sí mismo en los formularios de creación o edición de clientes (y para evitar que elija por error a otro entrenador), el formulario `ClientForm` (`core/forms.py`) **elimina dinámicamente** el campo `entrenador_asignado` cuando detecta que el usuario en sesión es un Entrenador.
- La vista de creación (`ClientCreateView`) asocia de manera implícita al Entrenador en sesión al momento de guardar los datos.
- Para usuarios con el rol **Admin** o **Superusuario**, el campo `entrenador_asignado` permanece visible y editable, permitiéndoles reasignar o definir el entrenador correspondiente libremente.
