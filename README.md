# Secret Scanner

Su misión es escanear archivos locales o repositorios Git en busca de secretos, claves y contraseñas expuestas.
## Requisitos Previos

-   Python 3.8 o superior.
-   Instancia de PostgreSQL activa.
-   Git instalado en el sistema.

## Instalación

1.  **Clonar el proyecto:**
    ```bash
    git clone <tu-repositorio>
    cd password
    ```

2.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configurar variables de entorno:**
    Crea un archivo `.env` en la raíz con tus credenciales:
    ```text
    DB_NAME=tu_base_de_datos
    DB_USER=tu_usuario
    DB_PASS=tu_password
    DB_HOST=localhost
    DB_PORT=5432
    ```

4.  **Inicializar la Base de Datos:**
    ```bash
    python3 setup_db.py
    ```

## Uso

El programa acepta tanto rutas de carpetas locales como URLs de Git.

### Escaneo de carpeta local:
```bash
python3 -m main ./mi_codigo_fuente# password
