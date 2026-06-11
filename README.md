# device_systems API — EV09

**GA1-220501096-01-AA1-EV09 · FastAPI con SQLAlchemy**  
Aprendiz: Kevin Andrés Zapata Murillo · Ficha 3114227 · SENA Medellín  
Instructor: Carlos Navia

---

## Tabla de contenido

1. [Descripción del proyecto](#descripción-del-proyecto)
2. [Tecnologías utilizadas](#tecnologías-utilizadas)
3. [Estructura del proyecto](#estructura-del-proyecto)
4. [Instalación y ejecución](#instalación-y-ejecución)
5. [Base de datos generada](#base-de-datos-generada)
6. [Documentación Swagger UI](#documentación-swagger-ui)
7. [Prueba de cada endpoint](#prueba-de-cada-endpoint)
8. [Errores controlados](#errores-controlados)
9. [Diferencia entre modelo SQLAlchemy y schema Pydantic](#diferencia-entre-modelo-sqlalchemy-y-schema-pydantic)
10. [Reflexión final](#reflexión-final)

---

## Descripción del proyecto

`device_systems` es una API REST construida con **FastAPI** que gestiona usuarios de un sistema de dispositivos. En esta versión EV09 se migró el almacenamiento de memoria RAM a una **base de datos relacional SQLite** usando **SQLAlchemy** como ORM, cumpliendo con persistencia real de datos.

### Cambios respecto a EV08

| Aspecto | EV08 | EV09 |
|---------|------|------|
| Almacenamiento | Listas y diccionarios en memoria | Base de datos SQLite |
| ORM | No aplica | SQLAlchemy 2.x |
| Modelo de datos | `UserInDB` (Pydantic) | `User` (SQLAlchemy) |
| Persistencia | Se pierde al reiniciar | Persiste en `device_systems.db` |
| Directorio `data/` | `users_db.py` con datos en memoria | Eliminado — reemplazado por `database/` |
| Filtros | En memoria con list comprehension | Queries SQL con `.filter()` |
| Ordenamiento | No disponible | ORDER BY con campo configurable |

---

## Tecnologías utilizadas

- Python 3.12
- FastAPI 0.100+
- Uvicorn
- SQLAlchemy 2.0
- Pydantic v2 + email-validator
- SQLite

---

## Estructura del proyecto

```
device_systems/
│── app/
│   │── __init__.py
│   │── main.py                          ← Configuración FastAPI + arranque de tablas
│   │
│   │── database/
│   │   └── connection.py                ← engine, SessionLocal, Base
│   │
│   │── models/
│   │   └── user_model.py                ← Modelo SQLAlchemy User (tabla users)
│   │
│   │── schemas/
│   │   └── user_schema.py               ← UserCreate, UserUpdate, UserPatch, UserResponse
│   │
│   │── routes/
│   │   └── user_routes.py               ← Endpoints GET/POST/PUT/PATCH/DELETE
│   │
│   │── services/
│   │   └── user_service.py              ← Lógica de negocio + operaciones CRUD
│   │
│   └── dependencies/
│       └── database_dependency.py       ← get_db() con Depends()
│
│── requirements.txt
│── README.md
└── device_systems.db                    ← Base de datos SQLite (generada automáticamente)
```

**Captura de la estructura en terminal:**

```
$ find device_systems/app -name "*.py" | sort
device_systems/app/__init__.py
device_systems/app/database/__init__.py
device_systems/app/database/connection.py
device_systems/app/dependencies/__init__.py
device_systems/app/dependencies/database_dependency.py
device_systems/app/main.py
device_systems/app/models/__init__.py
device_systems/app/models/user_model.py
device_systems/app/routes/__init__.py
device_systems/app/routes/user_routes.py
device_systems/app/schemas/__init__.py
device_systems/app/schemas/user_schema.py
device_systems/app/services/__init__.py
device_systems/app/services/user_service.py
```

---

## Instalación y ejecución

```bash
# 1. Clonar el repositorio
git clone https://github.com/kevinzapata/device_systems.git
cd device_systems

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate        # Linux / Mac
venv\Scripts\activate           # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Iniciar el servidor
uvicorn app.main:app --reload

# La API estará disponible en:
#   http://localhost:8000
#   http://localhost:8000/docs  ← Swagger UI
#   http://localhost:8000/redoc ← ReDoc
```

> La base de datos `device_systems.db` se crea automáticamente al iniciar la aplicación mediante `Base.metadata.create_all(bind=engine)`.

---

## Base de datos generada

Al iniciar la API, SQLAlchemy crea automáticamente el archivo `device_systems.db` con la tabla `users`.

**Estructura de la tabla `users`:**

```sql
CREATE TABLE users (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       VARCHAR(100) NOT NULL,
    email      VARCHAR(255) NOT NULL UNIQUE,
    role       VARCHAR(50)  NOT NULL,
    is_active  BOOLEAN      NOT NULL DEFAULT 1,
    created_at DATETIME     NOT NULL
);

CREATE UNIQUE INDEX ix_users_email ON users (email);
CREATE INDEX ix_users_id ON users (id);
```

**Verificación con sqlite3:**

```bash
$ sqlite3 device_systems.db ".schema users"
CREATE TABLE users (
    id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,
    is_active BOOLEAN NOT NULL,
    created_at DATETIME NOT NULL,
    PRIMARY KEY (id)
);

$ sqlite3 device_systems.db "SELECT * FROM users;"
1|Kevin Zapata|kevin@devicesystems.com|admin|1|2026-06-11 00:44:29.842912
2|Carolina Zuluaga|carolina@devicesystems.com|user|1|2026-06-11 00:44:29.850532
3|Luis Méndez|luis@devicesystems.com|support|0|2026-06-11 00:44:29.855568
4|Kelin Montoya|kelin@devicesystems.com|user|1|2026-06-11 00:44:29.867102
```

---

## Documentación Swagger UI

La documentación interactiva está disponible en `http://localhost:8000/docs`.

FastAPI genera automáticamente la especificación OpenAPI 3.0 con:
- Todos los endpoints del recurso `/users`
- Schemas de entrada y salida
- Códigos de estado HTTP
- Posibilidad de probar cada endpoint desde el navegador

**Endpoints documentados:**

```
GET    /users/           Listar todos los usuarios (con filtros y ordenamiento)
GET    /users/{user_id}  Obtener usuario por ID
POST   /users/           Crear nuevo usuario
PUT    /users/{user_id}  Actualizar usuario completo
PATCH  /users/{user_id}  Actualizar usuario parcialmente
DELETE /users/{user_id}  Eliminar usuario
```

> **Nota:** Las capturas de pantalla de Swagger UI se encuentran en la carpeta `/screenshots` del repositorio o se pueden generar localmente ejecutando el servidor y visitando `/docs`.

---

## Prueba de cada endpoint

### 1. GET `/users/` — Listar usuarios

**Request:**
```
GET http://localhost:8000/users/
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Kevin Zapata",
    "email": "kevin@devicesystems.com",
    "role": "admin",
    "is_active": true,
    "created_at": "2026-06-11T00:44:29.842912"
  },
  {
    "id": 2,
    "name": "Carolina Z. Actualizada",
    "email": "carolina.updated@devicesystems.com",
    "role": "support",
    "is_active": true,
    "created_at": "2026-06-11T00:44:29.850532"
  },
  {
    "id": 3,
    "name": "Luis Méndez",
    "email": "luis@devicesystems.com",
    "role": "support",
    "is_active": true,
    "created_at": "2026-06-11T00:44:29.855668"
  }
]
```

---

### 2. GET `/users/{user_id}` — Obtener usuario por ID

**Request:**
```
GET http://localhost:8000/users/1
```

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "Kevin Zapata",
  "email": "kevin@devicesystems.com",
  "role": "admin",
  "is_active": true,
  "created_at": "2026-06-11T00:44:29.842912"
}
```

---

### 3. POST `/users/` — Crear usuario válido

**Request:**
```json
POST http://localhost:8000/users/
Content-Type: application/json

{
  "name": "Gustavo Bolaños",
  "email": "gustavo@sena.edu.co",
  "role": "admin",
  "is_active": true
}
```

**Response (201 Created):**
```json
{
  "id": 5,
  "name": "Gustavo Bolaños",
  "email": "gustavo@sena.edu.co",
  "role": "admin",
  "is_active": true,
  "created_at": "2026-06-11T00:50:01.891865"
}
```

---

### 4. PUT `/users/{user_id}` — Actualizar completo

**Request:**
```json
PUT http://localhost:8000/users/2
Content-Type: application/json

{
  "name": "Carolina Z. Actualizada",
  "email": "carolina.updated@devicesystems.com",
  "role": "support",
  "is_active": true
}
```

**Response (200 OK):**
```json
{
  "id": 2,
  "name": "Carolina Z. Actualizada",
  "email": "carolina.updated@devicesystems.com",
  "role": "support",
  "is_active": true,
  "created_at": "2026-06-11T00:44:29.850532"
}
```

---

### 5. PATCH `/users/{user_id}` — Actualizar parcialmente

**Request:**
```json
PATCH http://localhost:8000/users/3
Content-Type: application/json

{
  "is_active": true
}
```

**Response (200 OK):**
```json
{
  "id": 3,
  "name": "Luis Méndez",
  "email": "luis@devicesystems.com",
  "role": "support",
  "is_active": true,
  "created_at": "2026-06-11T00:44:29.855668"
}
```

---

### 6. DELETE `/users/{user_id}` — Eliminar usuario

**Request:**
```
DELETE http://localhost:8000/users/4
```

**Response: `204 No Content`** (sin cuerpo)

---

### 7. GET `/users/?role=admin` — Filtrar por rol

**Request:**
```
GET http://localhost:8000/users/?role=admin
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Kevin Zapata",
    "email": "kevin@devicesystems.com",
    "role": "admin",
    "is_active": true,
    "created_at": "2026-06-11T00:44:29.842912"
  },
  {
    "id": 4,
    "name": "Gustavo Bolaños",
    "email": "gustavo@sena.edu.co",
    "role": "admin",
    "is_active": true,
    "created_at": "2026-06-11T00:50:01.891865"
  }
]
```

---

### 8. GET `/users/?is_active=true` — Filtrar usuarios activos

**Request:**
```
GET http://localhost:8000/users/?is_active=true
```

**Response (200 OK):**
```json
[
  {"id": 1, "name": "Kevin Zapata", "role": "admin", "is_active": true, ...},
  {"id": 2, "name": "Carolina Z. Actualizada", "role": "support", "is_active": true, ...},
  {"id": 3, "name": "Luis Méndez", "role": "support", "is_active": true, ...},
  {"id": 4, "name": "Gustavo Bolaños", "role": "admin", "is_active": true, ...}
]
```

---

### 9. GET `/users/?order_by=name` — Ordenar por nombre

**Request:**
```
GET http://localhost:8000/users/?order_by=name
```

**Response (200 OK) — ordenado alfabéticamente:**
```json
[
  {"id": 2, "name": "Carolina Z. Actualizada", ...},
  {"id": 4, "name": "Gustavo Bolaños", ...},
  {"id": 1, "name": "Kevin Zapata", ...},
  {"id": 3, "name": "Luis Méndez", ...}
]
```

---

### 10. GET `/users/99` — Verificar usuario eliminado / no existente

**Request:**
```
GET http://localhost:8000/users/99
```

**Response (404 Not Found):**
```json
{
  "detail": "Usuario con id 99 no encontrado"
}
```

---

## Errores controlados

### Email duplicado — 400 Bad Request

**Request:**
```json
POST http://localhost:8000/users/
{
  "name": "Copia Kevin",
  "email": "kevin@devicesystems.com",
  "role": "user"
}
```

**Response:**
```json
{
  "detail": "El correo 'kevin@devicesystems.com' ya está registrado"
}
```

---

### Rol no permitido — 422 Unprocessable Entity

**Request:**
```json
POST http://localhost:8000/users/
{
  "name": "Test User",
  "email": "test@test.com",
  "role": "moderator"
}
```

**Response:**
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "role"],
      "msg": "Value error, Rol 'moderator' no permitido. Roles válidos: ['admin', 'support', 'user']",
      "input": "moderator",
      "ctx": {"error": {}}
    }
  ]
}
```

---

### Usuario no encontrado — 404 Not Found

```json
{ "detail": "Usuario con id 99 no encontrado" }
```

---

### Tabla de códigos HTTP

| Caso | Código |
|------|--------|
| Usuario creado | 201 Created |
| Consulta correcta | 200 OK |
| Actualización correcta | 200 OK |
| Eliminación correcta | 204 No Content |
| Usuario no encontrado | 404 Not Found |
| Email duplicado | 400 Bad Request |
| Rol inválido / datos inválidos | 422 Unprocessable Entity |

---

## Diferencia entre modelo SQLAlchemy y schema Pydantic

Esta es una de las distincciones más importantes de esta actividad:

### Modelo SQLAlchemy (`app/models/user_model.py`)

```python
class User(Base):
    __tablename__ = "users"
    id         = Column(Integer, primary_key=True)
    name       = Column(String(100), nullable=False)
    email      = Column(String(255), unique=True, nullable=False)
    role       = Column(String(50), nullable=False)
    is_active  = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
```

**Propósito:** Representa la **tabla en la base de datos**. Define cómo se almacenan los datos (columnas, tipos, constraints). SQLAlchemy lo usa para generar SQL y para mapear filas de la DB a objetos Python.

---

### Schemas Pydantic (`app/schemas/user_schema.py`)

```python
class UserCreate(BaseModel):
    name:      str      = Field(..., min_length=3)
    email:     EmailStr
    role:      str
    is_active: bool     = True

class UserResponse(BaseModel):
    id:         int
    name:       str
    email:      str
    role:       str
    is_active:  bool
    created_at: datetime
    model_config = {"from_attributes": True}
```

**Propósito:** Controlan lo que entra y sale de la API. `UserCreate` valida que el JSON que envía el cliente sea correcto. `UserResponse` define qué campos se devuelven al cliente (puede excluir campos sensibles).

---

### Resumen comparativo

| Aspecto | Modelo SQLAlchemy | Schema Pydantic |
|---------|-------------------|-----------------|
| ¿Qué representa? | Tabla en la base de datos | Datos que entran/salen de la API |
| Hereda de | `Base` (declarative_base) | `BaseModel` |
| Define | Columnas, constraints, índices | Campos, validaciones, tipos |
| Usado en | `services/`, sesión de DB | `routes/`, request/response |
| Genera | SQL CREATE TABLE | Validación + serialización JSON |
| Conoce la DB | Sí | No |

> **Conclusión:** ambos representan al mismo "usuario", pero desde perspectivas distintas. El modelo SQLAlchemy es el contrato con la base de datos; el schema Pydantic es el contrato con el cliente HTTP.

---

## Reflexión final

En la versión anterior (EV08), cada vez que se reiniciaba el servidor todos los usuarios creados desaparecían. Eso hace que una API sea inútil en producción real, porque los datos no sobreviven ni siquiera un simple reinicio.

Con SQLAlchemy y SQLite aprendí que la persistencia no es solo "guardar en un archivo": implica un sistema completo de transacciones, constraints de integridad (como `UNIQUE` en email), consultas eficientes con índices, y la separación clara entre el modelo de datos (lo que vive en la DB) y el schema de API (lo que el cliente ve).

También entendí por qué FastAPI separa estos dos conceptos: el modelo SQLAlchemy puede tener campos internos (como contraseñas hasheadas, tokens, fechas de modificación) que nunca deberían exponerse al cliente. El schema `UserResponse` actúa como filtro: decide qué datos son públicos y cuáles no.

Este patrón —modelo + schema + servicio + ruta— es exactamente cómo funcionan aplicaciones reales como las que estamos construyendo en FinMind, y entenderlo a este nivel da una base sólida para cualquier backend profesional.

---
