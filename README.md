# diagnostico_rx_ia

Aplicación para apoyar el diagnóstico de imágenes RX con ayuda de IA.

**Instalación rápida (al clonar el repositorio)**

Sigue estos pasos después de clonar el repositorio para preparar el entorno de desarrollo (instrucciones para Windows PowerShell):

```powershell
# Clonar el repositorio (reemplaza la URL por la tuya si procede)
git clone <REPO_URL>
cd diagnostico_rx_ia

# Crear y activar un virtualenv (PowerShell)
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.\.venv\Scripts\Activate.ps1

# Actualizar pip e instalar dependencias
python -m pip install --upgrade pip
pip install -r requirements.txt

# Aplicar migraciones y crear superusuario
python manage.py migrate
python manage.py createsuperuser

# Ejecutar servidor de desarrollo
python manage.py runserver
```

**Instalar Django (opcional / manual)**

Si por alguna razón necesitas instalar Django manualmente en el entorno virtual (por ejemplo para usar una versión concreta), ejecuta:

```powershell
# Instalar la versión recomendada (ej: Django 5.2.x)
pip install "Django==5.2.*"


Biblioteca para imágenes:
- Este proyecto requiere `Pillow` (ya incluido en `requirements.txt` como `pillow==10.1.0`). Si necesitas instalarla manualmente dentro del virtualenv:

```powershell
pip install pillow
```

- Si planeas procesar imágenes con OpenCV (opcional), instala:

```powershell
pip install opencv-python
```

Si quieres que añada instrucciones para entornos Unix/macOS o Docker, dímelo y las agrego.



# Verificar la versión instalada
python -m django --version
```

También puedes instalar todas las dependencias desde `requirements.txt` (recomendado si existe):

```powershell
pip install -r requirements.txt
```

Notas breves:
- Requiere Python 3.13 (o la versión indicada en `requirements.txt`).
- Por defecto el proyecto usa SQLite (`db.sqlite3`) para desarrollo.
- El correo electrónico en desarrollo está configurado para consola; configura el `EMAIL_BACKEND` y credenciales SMTP en `diagnostico_ia_project/settings.py` para envío real.
- La verificación 2FA en frontend tiene un bypass temporal; la implementación backend completa de 2FA está pendiente (ver `users/` para plantillas y vistas existentes).

