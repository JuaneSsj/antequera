# Resumen del Proyecto: Sistema de Gestión de Gimnasio

Este documento sirve como punto de entrada para comprender la arquitectura, estructura y flujos principales del proyecto.

## 🎯 Objetivo General
Es una aplicación web construida con **Django** orientada a la gestión de un gimnasio o servicio de entrenamiento personal. Permite administrar clientes, entrenadores, registrar medidas corporales, agendar sesiones de entrenamiento y manejar perfiles con control de acceso basado en roles.

## 📂 Archivos de Documentación Detallada
Para mantener este resumen conciso, la información detallada se ha dividido en los siguientes documentos. Haz clic en los enlaces para leer más:

1. **[Estructura y Relaciones de Base de Datos](./02_estructura_base_datos.md)**: Detalla los modelos de datos, cómo se relacionan los Usuarios, Clientes, Entrenadores y sus Medidas.
2. **[Flujos de Usuario y Vistas](./03_flujos_y_vistas.md)**: Explica cómo navega un usuario por la aplicación, los flujos de creación/edición y la agenda.
3. **[Roles y Seguridad](./04_roles_seguridad.md)**: Describe cómo funciona el sistema de autenticación, middleware de acceso y diferenciación entre Administradores, Entrenadores y Clientes.

## 🛠️ Stack Tecnológico
- **Backend:** Python con Django (Versión 5.x/6.x)
- **Base de Datos:** PostgreSQL (Configurada vía variables de entorno)
- **Frontend:** Django Templates (HTML/CSS/JS) con un diseño dinámico.
- **Despliegue/Entorno:** Gestión de variables de entorno mediante `python-dotenv`.

## 📁 Estructura Principal del Código
- `gym_project/`: Carpeta de configuración principal de Django (`settings.py`, `urls.py`).
- `core/`: La aplicación Django principal que contiene toda la lógica de negocio (`models.py`, `views.py`, `urls.py`, `forms.py`, `middleware.py`).
