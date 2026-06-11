from fastapi import FastAPI
from app.database.connection import engine, Base
from app.routes.user_routes import router as user_router

# ─── Crear tablas al iniciar (si no existen) ──────────────────────────────────
Base.metadata.create_all(bind=engine)

# ─── Metadatos OpenAPI / Swagger ──────────────────────────────────────────────
tags_metadata = [
    {
        "name": "Users",
        "description": (
            "Operaciones CRUD sobre el recurso **usuarios**. "
            "Incluye creación, consulta, actualización completa/parcial y eliminación. "
            "Los datos se persisten en una base de datos SQLite mediante SQLAlchemy."
        ),
    },
]

app = FastAPI(
    title="device_systems API",
    description=(
        "API REST para la gestión de usuarios del sistema **device_systems**.\n\n"
        "## Funcionalidades\n"
        "- CRUD completo de usuarios con persistencia en SQLite\n"
        "- Filtrado por rol y estado activo\n"
        "- Ordenamiento por campo\n"
        "- Validación de datos con Pydantic v2\n"
        "- Manejo profesional de errores HTTP\n"
        "- Dependency Injection con `Depends()`\n"
        "- Modelos SQLAlchemy con constraints\n\n"
        "## Roles permitidos\n"
        "`admin`, `user`, `support`"
    ),
    version="3.0.0",
    contact={
        "name": "Kevin Andrés Zapata Murillo",
        "email": "kevin.zapata@sena.edu.co",
    },
    license_info={
        "name": "SENA - Ficha 3114227",
    },
    openapi_tags=tags_metadata,
)

# ─── Routers ──────────────────────────────────────────────────────────────────
app.include_router(user_router)


# ─── Root ─────────────────────────────────────────────────────────────────────
@app.get("/", tags=["Root"], summary="Bienvenida")
def root():
    return {
        "message": "Bienvenido a device_systems API v3.0.0",
        "descripcion": "API con persistencia SQLAlchemy + SQLite",
        "docs": "/docs",
        "redoc": "/redoc",
    }
