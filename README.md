# API de La Cosecha

API para apoyar la operación de **La Cosecha**, una tienda en Zipaquirá: permite organizar el inventario de productos y registrar ventas.

## Tecnologías y componentes

- **FastAPI** para exponer la API y su documentación interactiva.
- **SQLAlchemy** para crear las tablas y trabajar con la base de datos configurada en `DATABASE_URL`.
- **OAuth2 Bearer** para autenticar a las personas usuarias.
- **CORS** configurable mediante `CORS_ORIGINS`.
- **Excel `.xlsx`** para importar inventario de productos.

La documentación interactiva de FastAPI está disponible en `/docs` cuando la aplicación está en ejecución.

## Endpoints

Las rutas protegidas requieren iniciar sesión y enviar el token Bearer, salvo `POST /auth/login` y `GET /`.

| Método | Ruta | Qué hace | Quién puede usarla |
|---|---|---|---|
| `GET` | `/` | Comprueba que la API está en línea. | Cualquier persona |
| `POST` | `/auth/login` | Inicia sesión con correo y contraseña; devuelve un token de acceso. | Cualquier persona con cuenta |
| `GET` | `/auth/yo` | Devuelve la información de la cuenta autenticada. | Cualquier persona autenticada |
| `GET` | `/usuarios/` | Lista las cuentas. | Administradora |
| `POST` | `/usuarios/` | Crea una cuenta. | Administradora |
| `PATCH` | `/usuarios/{usuario_id}/estado` | Cambia el estado activo de una cuenta. | Administradora |
| `GET` | `/categorias/` | Lista las categorías. | Cualquier persona autenticada |
| `GET` | `/categorias/{categoria_id}` | Consulta una categoría. | Cualquier persona autenticada |
| `POST` | `/categorias/` | Crea una categoría. | Administradora |
| `PUT` | `/categorias/{categoria_id}` | Actualiza una categoría. | Administradora |
| `DELETE` | `/categorias/{categoria_id}` | Elimina una categoría si no tiene productos asociados. | Administradora |
| `GET` | `/productos/` | Lista productos del inventario. | Cualquier persona autenticada |
| `GET` | `/productos/{producto_id}` | Consulta un producto. | Cualquier persona autenticada |
| `POST` | `/productos/` | Crea un producto. | Administradora |
| `POST` | `/productos/importar` | Importa inventario desde un `.xlsx` con las columnas `nombre`, `precio`, `stock` y `categoria` en la primera fila. La operación valida el archivo antes de guardar. | Administradora |
| `PUT` | `/productos/{producto_id}` | Actualiza un producto. | Administradora |
| `DELETE` | `/productos/{producto_id}` | Elimina un producto si todavía no tiene ventas. | Administradora |
| `POST` | `/ventas/` | Registra una venta; el vendedor se obtiene de la sesión y el backend calcula totales y subtotales. Si una línea falla, no guarda la venta ni descuenta stock. | Cualquier persona autenticada |
| `GET` | `/ventas/` | Consulta las ventas de un día. Acepta el parámetro opcional `fecha` con formato `AAAA-MM-DD`; si se omite, consulta el día actual. | Administradora (todas las ventas); vendedora (solo las propias) |

## Instalación y ejecución en Windows

Abre PowerShell en la carpeta del proyecto y crea y activa un entorno virtual:

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
```

Instala las dependencias del proyecto:

```powershell
python -m pip install -r requirements.txt
```

Crea un archivo `.env` en la raíz del proyecto usando `.env.example` como referencia y completa sus valores. Luego inicia la API:

```powershell
uvicorn app.main:app --reload
```

Abre `http://127.0.0.1:8000/docs` para explorar y probar los endpoints.

## Variables de entorno

Configura estas variables en `.env` para desarrollo. En producción, configúralas como variables de entorno del servicio y no subas credenciales reales al repositorio.

| Variable | Uso |
|---|---|
| `DATABASE_URL` | URL de conexión a la base de datos. El ejemplo usa el puerto `5432`. |
| `SECRET_KEY` | Clave para firmar los tokens. Usa una clave aleatoria y privada; no conserves el texto de ejemplo en producción. |
| `ADMIN_NOMBRE` | Nombre de la administradora inicial. |
| `ADMIN_CORREO` | Correo de la administradora inicial. |
| `ADMIN_CONTRASENA` | Contraseña inicial de la administradora. Cámbiala por una segura. |
| `CORS_ORIGINS` | Lista JSON de orígenes permitidos para solicitudes CORS. El ejemplo incluye direcciones locales en el puerto `5500`. |
| `ECHO_SQL` | Controla la opción de registro SQL indicada en el ejemplo (`false`). |

Al iniciar la aplicación, se crean las tablas y se prepara la cuenta administradora inicial.

## Producción: Render y Neon

1. Crea una base de datos PostgreSQL en Neon y copia su cadena de conexión.
2. Despliega este repositorio en Render como un servicio web de Python.
3. En las variables de entorno del servicio Render, configura `DATABASE_URL` con la conexión de Neon y define también `SECRET_KEY`, `ADMIN_NOMBRE`, `ADMIN_CORREO`, `ADMIN_CONTRASENA`, `CORS_ORIGINS` y `ECHO_SQL`.
4. Usa `uvicorn app.main:app --host 0.0.0.0 --port $PORT` como comando de inicio del servicio.
5. Reemplaza los orígenes locales de `CORS_ORIGINS` por los orígenes de producción que deban acceder a la API. Mantén las claves y contraseñas fuera del repositorio.

