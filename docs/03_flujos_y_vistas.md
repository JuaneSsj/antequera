# Flujos de Usuario y Vistas

La aplicación utiliza fuertemente el patrón de Vistas Basadas en Clases (Class-Based Views) de Django en `core/views.py` para manejar el flujo de las pantallas.

## 1. Flujo de Inicio (`HomeView`)
Es el punto de entrada principal (`/`) una vez que el usuario inicia sesión. Analiza el rol del usuario para redirigirlo de forma inteligente:
- **Admin / Superuser**: Visualiza un dashboard resumen con los últimos clientes creados y el entrenador principal.
- **Entrenador**: Es redirigido automáticamente a su agenda diaria (`trainer_agenda`).
- **Cliente**: Es redirigido al panel de detalle de su perfil (`client_detail`) para ver sus avances, o a la vista para reservar sesión (`client_booking`) si no tiene asignación.

## 2. Flujo de Gestión de Clientes
- **Listados (`ClientListView`, `ClientArchiveListView`)**: Vistas separadas para ver clientes activos y clientes archivados, con un motor de búsqueda integrado. Permite alternar el estado con un botón (`client_archive_toggle`).
- **Panel Detalle (`ClientDetailView`)**: Funciona como el expediente médico/deportivo del cliente. Carga y muestra los datos generales, todo el historial de medidas (extrayendo visualmente la medición inicial y la última) y su galería de imágenes.
- **Creación/Edición**: Al crear un cliente, si el usuario que lo crea es un Entrenador, el sistema asigna automáticamente a ese entrenador como el encargado del nuevo cliente.

## 3. Flujo de Mediciones y Progreso
- **Crear Medida (`MeasurementCreateView`)**: Accesible desde el detalle del cliente. El controlador inyecta el `client_id` automáticamente en el formulario.
- **Galería (`ClientImageCreateView`)**: Permite subir fotos de evolución con fechas y notas asociadas.

## 4. Flujo de Agenda y Reservas
Existen dos vistas complementarias para la gestión del tiempo:
- **Vista del Cliente (`ClientBookingView`)**: El cliente escoge un día. El sistema calcula los horarios disponibles (de 8:00 a 20:00) cruzando esta información con las sesiones ya agendadas de su Entrenador. Al elegir una hora, se crea la sesión en estado "Pendiente".
- **Vista del Entrenador (`TrainerAgendaView`)**: Muestra al entrenador un listado ordenado cronológicamente de todas las sesiones que tiene programadas.
