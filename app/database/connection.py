from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ─── URL de la base de datos SQLite ───────────────────────────────────────────
DATABASE_URL = "sqlite:///./device_systems.db"

# ─── Engine ───────────────────────────────────────────────────────────────────
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Solo necesario para SQLite
)

# ─── Sesión ───────────────────────────────────────────────────────────────────
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# ─── Base declarativa ─────────────────────────────────────────────────────────
Base = declarative_base()
