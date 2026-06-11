from typing import Generator
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Dependencia de FastAPI que proporciona una sesión de base de datos.

    Abre una sesión al inicio de cada request y la cierra automáticamente
    al finalizar, incluso si ocurre una excepción.

    Uso en endpoints:
        db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
