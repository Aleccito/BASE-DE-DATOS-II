# TALLER2 Backend — Sistema de Gestión de Expedientes Vehiculares

## Análisis del diagrama original

### Entidades identificadas

| Entidad       | PK              | Descripción                                  |
|---------------|-----------------|-----------------------------------------------|
| ASEGURADORAS  | id_aseguradora  | Compañías aseguradoras                        |
| USUARIO       | id_usuario      | Personas dueñas de vehículos / partes en un caso |
| JUZGADOS      | id_juzgado      | Juzgados donde se tramitan los expedientes    |
| MARCAS        | id_marca        | Marcas de vehículos                           |
| MODELOS       | id_modelo       | Modelos de vehículos                          |
| VEHICULOS     | id_vehiculo     | Vehículos registrados                         |
| EXPEDIENTES   | id_expediente   | Casos/expedientes legales asociados a un vehículo |

### Relaciones (1 : N)

- `ASEGURADORAS` → `USUARIO` (un usuario puede tener una aseguradora)
- `ASEGURADORAS` → `EXPEDIENTES`
- `USUARIO` → `VEHICULOS`
- `USUARIO` → `EXPEDIENTES`
- `JUZGADOS` → `EXPEDIENTES`
- `VEHICULOS` → `EXPEDIENTES`
- `MODELOS` → `VEHICULOS`
- `MARCAS` → `VEHICULOS`


## Arquitectura del proyecto

```
taller2_backend/
├── app.py                  # Punto de entrada (factory create_app)
├── config.py                # Configuración vía variables de entorno
├── extensions.py             # Instancias de SQLAlchemy, JWT, Migrate, CORS
├── requirements.txt
├── .env.example
├── database/
│   └── schema.sql            # Script SQL completo (DDL) para MySQL
├── models/                   # Modelos SQLAlchemy (1 archivo por entidad)
├── routes/                   # Blueprints (definición de endpoints)
├── controllers/              # Traducción request/response, códigos HTTP
├── services/                 # Lógica de negocio, validaciones, acceso a datos
└── utils/
    ├── responses.py          # Formato estándar de respuestas JSON
    ├── validators.py         # Validaciones reutilizables + ValidationError
    └── decorators.py         # @roles_required, etc.
```

Flujo de una petición: `routes` → `controllers` (parseo request / respuesta HTTP) →
`services` (reglas de negocio, validación, ORM) → `models` (SQLAlchemy).

## Requisitos previos

- Python 3.10+
- MySQL 8+
- pip / virtualenv

## Instalación

```bash
# 1. Clonar / descomprimir el proyecto y entrar en la carpeta
cd taller2_backend

# 2. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate        # En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con las credenciales reales de tu MySQL
```

## Configuración de la base de datos

### Opción A: usar el script SQL directamente

```bash
mysql -u root -p < database/schema.sql
```

Esto crea la base `taller2_db`, todas las tablas, llaves foráneas, índices y restricciones
(`CHECK`, `UNIQUE`).

### Opción B: usar Flask-Migrate (Alembic)

```bash
# Asegúrate de que DB_NAME en .env ya exista vacía en MySQL (CREATE DATABASE taller2_db;)
flask db init
flask db migrate -m "Esquema inicial"
flask db upgrade
```

## Ejecutar el servidor

```bash
python app.py
# o
flask run
```

Por defecto corre en `http://localhost:5000`. Verifica que esté activo:

```bash
curl http://localhost:5000/api/health
```

## Autenticación (JWT)

1. **Registro**: `POST /api/auth/register` (público) crea un usuario con contraseña hasheada
   (`werkzeug.security`).
2. **Login**: `POST /api/auth/login` retorna `access_token` y `refresh_token`.
3. Todas las rutas de `usuarios`, `vehiculos` y `expedientes` requieren el header:
   `Authorization: Bearer <access_token>`.
4. **Refresh**: `POST /api/auth/refresh` con el `refresh_token` genera un nuevo `access_token`.

Los endpoints de `aseguradoras`, `juzgados`, `marcas` y `modelos` (catálogos) están abiertos
para lectura/escritura en esta versión; puedes protegerlos igual con `@jwt_required()` o
`@roles_required("admin")` (ya incluido en `utils/decorators.py`) si tu caso de uso lo requiere.

## Formato de respuesta estándar

```json
{
  "success": true,
  "message": "Descripción de la operación",
  "data": { }
}
```

En caso de error:

```json
{
  "success": false,
  "message": "Descripción del error",
  "errors": ["detalle 1", "detalle 2"]
}
```

## Endpoints disponibles

### Autenticación (`/api/auth`)

| Método | Endpoint             | Descripción                    | Auth |
|--------|-----------------------|---------------------------------|------|
| POST   | /api/auth/register    | Registrar nuevo usuario         | No   |
| POST   | /api/auth/login       | Iniciar sesión (retorna JWT)    | No   |
| POST   | /api/auth/refresh     | Renovar access_token            | Refresh token |

### Usuarios (`/api/usuarios`)

| Método | Endpoint              | Descripción             | Auth |
|--------|------------------------|--------------------------|------|
| GET    | /api/usuarios          | Listar usuarios          | Sí   |
| GET    | /api/usuarios/me       | Perfil del usuario autenticado | Sí |
| GET    | /api/usuarios/<id>     | Obtener usuario por id   | Sí   |
| POST   | /api/usuarios          | Crear usuario (= register) | No |
| PUT    | /api/usuarios/<id>     | Actualizar usuario       | Sí   |
| DELETE | /api/usuarios/<id>     | Eliminar usuario         | Sí   |

### Aseguradoras, Juzgados, Marcas, Modelos

CRUD estándar bajo `/api/aseguradoras`, `/api/juzgados`, `/api/marcas`, `/api/modelos`:
`GET /`, `GET /<id>`, `POST /`, `PUT /<id>`, `DELETE /<id>`.

### Vehículos (`/api/vehiculos`) — requiere JWT

| Método | Endpoint             | Body de ejemplo |
|--------|------------------------|------------------|
| POST   | /api/vehiculos         | `{"id_usuario":1,"id_modelo":1,"id_marca":1,"matricula":"ABC-123","chasis":"XYZ123456","anio":2022,"tipo":"sedan","color":"rojo"}` |
| PUT    | /api/vehiculos/<id>    | Cualquier subconjunto de los campos anteriores |
| GET    | /api/vehiculos         | Lista todos |
| GET    | /api/vehiculos/<id>    | Detalle |
| DELETE | /api/vehiculos/<id>    | Elimina si no tiene expedientes asociados |

### Expedientes (`/api/expedientes`) — requiere JWT

| Método | Endpoint               | Body de ejemplo |
|--------|-------------------------|------------------|
| POST   | /api/expedientes        | `{"id_aseguradora":1,"id_juzgado":1,"id_usuario":1,"id_vehiculo":1,"fecha":"2026-01-01","estado":"abierto"}` |
| PUT    | /api/expedientes/<id>   | Cualquier subconjunto de los campos anteriores |
| GET    | /api/expedientes        | Lista todos |
| GET    | /api/expedientes/<id>   | Detalle |
| DELETE | /api/expedientes/<id>   | Elimina el expediente |

`estado` acepta: `abierto`, `en_proceso`, `cerrado`, `archivado`.

## Validaciones implementadas

- Campos obligatorios y tipos de dato (string, int, fecha, email).
- Duplicados: `correo`, `identificacion`, `matricula`, `chasis`, nombres de catálogos.
- Existencia de llaves foráneas antes de crear/actualizar (`id_usuario`, `id_aseguradora`, etc.).
- Restricción de borrado: no se permite eliminar un registro padre si tiene hijos asociados
  (por ejemplo, no se puede borrar una marca con vehículos registrados).
- Longitudes de campos (`VARCHAR`) y rangos (`anio` entre 1900 y 2100).
- Contraseñas: mínimo 8 caracteres, almacenadas con hash (`werkzeug.security`), nunca en texto plano.

## Ejemplo de flujo completo con `curl`

```bash
# Registro
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Juan","apellido":"Perez","identificacion":"001-123456","correo":"juan@test.com","password":"password123"}'

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"correo":"juan@test.com","password":"password123"}'

# Usar el access_token retornado
curl http://localhost:5000/api/vehiculos \
  -H "Authorization: Bearer <access_token>"
```

## Notas de despliegue

- Para producción, usar `gunicorn app:app` (incluido en `requirements.txt`) detrás de un
  proxy como Nginx, y establecer `FLASK_ENV=production` en `.env`.
- Cambiar `SECRET_KEY` y `JWT_SECRET_KEY` por valores aleatorios y seguros (mínimo 32 bytes).
- Nunca subir el archivo `.env` real al control de versiones (ya está en `.gitignore`).
