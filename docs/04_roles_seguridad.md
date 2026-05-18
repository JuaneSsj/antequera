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
El proyecto aplica la seguridad en dos capas:

- **Lógica en las Vistas (Python)**: Vistas como `HomeView` y `TrainerDetailView` verifican explícitamente el rol del usuario (haciendo `.lower()` al nombre del rol) para decidir qué datos mandar al template (`context`) o hacia qué URL redirigir al visitante para que no vea páginas que no le corresponden.
- **Middleware Dinámico (`DynamicAccessMiddleware`)**: En `settings.py` existe un middleware de creación propia. Este componente es un guardián que se ejecuta en cada petición web. Intercepta la URL que el usuario quiere visitar, verifica en la base de datos de permisos (`Access`) si el `Profile` del usuario tiene habilitada esa ruta (`Route`), y bloquea el paso si se intenta violar un acceso.

## 4. Asignaciones Contextuales
Para evitar que un entrenador se asigne a sí mismo clientes de otros entrenadores por error, la lógica de los formularios (ej. `ClientCreateView`) inserta automáticamente la relación Entrenador-Cliente basándose en quién está logueado haciendo la solicitud web, inyectando seguridad directa a la capa de creación de datos.
