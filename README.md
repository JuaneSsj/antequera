# Training Home

Aplicación web para la gestión de clientes y entrenamientos personalizados.

## 🚀 Instalación y Configuración

Sigue estos pasos para clonar y ejecutar el proyecto en tu entorno local.

### 1. Clonar el Repositorio

```bash
git clone git@github.com:JuaneSsj/antequera.git
cd antequera
```

### 2. Crear Entorno Virtual

Es recomendable usar un entorno virtual para aislar las dependencias del proyecto.

**Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

Instala las librerías necesarias listadas en `requirements.txt`.

```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto (basado en el archivo de ejemplo si existe, o con las siguientes variables):

```ini
DEBUG=True
SECRET_KEY=tu_clave_secreta_segura
DB_NAME=nombre_base_datos
DB_USER=usuario_base_datos
DB_PASSWORD=contraseña_base_datos
DB_HOST=localhost
DB_PORT=5432
```
*Asegúrate de tener PostgreSQL instalado y configurado.*

### 5. Migraciones de Base de Datos

Aplica las migraciones para crear la estructura de la base de datos.

```bash
python manage.py migrate
```

### 6. Crear un Superusuario (Opcional)

Para acceder al panel de administración de Django:

```bash
python manage.py createsuperuser
```

### 7. Cargar las rutas y permisos iniciales

Ejecuta el script de seed para registrar las rutas y permisos que usa el middleware del proyecto.

```bash
python seed_routes.py
```

> Si ya creaste el superusuario, el script intentará vincularlo a un perfil de Admin para otorgarle acceso completo.

### 8. Ejecutar el Servidor

Inicia el servidor de desarrollo.

```bash
python manage.py runserver
```

Abre tu navegador en [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## 📋 Características Principales

- **Dashboard:** Vista general del entrenador y accesos rápidos.
- **Gestión de Clientes:** Registro, listado y detalles de clientes.
- **Seguimiento:** Registro de medidas y progreso.
- **Perfil de Entrenador:** Personalización de información pública (Bio, Redes, Contacto).
- **Branding:** Personalización de la identidad de la marca ("Training Home").

## 🛠️ Tecnologías

- Python / Django 5+
- PostgreSQL
- HTML / CSS / JavaScript
