from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from fastapi import HTTPException, status
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserUpdate, UserPatch


# ─── Helpers internos ─────────────────────────────────────────────────────────

def _get_or_404(db: Session, user_id: int) -> User:
    """Obtiene un usuario por ID o lanza 404."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con id {user_id} no encontrado",
        )
    return user


def _check_email_unique(db: Session, email: str, exclude_id: int | None = None) -> None:
    """Verifica que el email no esté registrado (opcionalmente excluye un ID)."""
    query = db.query(User).filter(User.email == email)
    if exclude_id is not None:
        query = query.filter(User.id != exclude_id)
    if query.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El correo '{email}' ya está registrado",
        )


# ─── CRUD ─────────────────────────────────────────────────────────────────────

def get_all_users(
    db: Session,
    role: str | None = None,
    is_active: bool | None = None,
    order_by: str = "id",
) -> list[User]:
    """
    Lista usuarios con filtros opcionales y ordenamiento.

    Parámetros:
        role      – filtra por rol exacto
        is_active – filtra por estado activo/inactivo
        order_by  – 'id', 'name', 'created_at' (prefijo '-' para DESC)
    """
    query = db.query(User)

    if role is not None:
        query = query.filter(User.role == role)
    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    # Ordenamiento
    ORDER_MAP = {
        "id": User.id,
        "name": User.name,
        "created_at": User.created_at,
        "-id": desc(User.id),
        "-name": desc(User.name),
        "-created_at": desc(User.created_at),
    }
    order_col = ORDER_MAP.get(order_by, User.id)
    query = query.order_by(order_col)

    return query.all()


def get_user_by_id(db: Session, user_id: int) -> User:
    """Retorna un usuario por ID o lanza 404."""
    return _get_or_404(db, user_id)


def get_user_by_email(db: Session, email: str) -> User:
    """Busca un usuario por email o lanza 404."""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con email '{email}' no encontrado",
        )
    return user


def create_user(db: Session, data: UserCreate) -> User:
    """Crea un nuevo usuario en la base de datos."""
    _check_email_unique(db, data.email)

    new_user = User(
        name=data.name,
        email=data.email,
        role=data.role,
        is_active=data.is_active,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def update_user(db: Session, user_id: int, data: UserUpdate) -> User:
    """Reemplaza completamente un usuario (PUT)."""
    user = _get_or_404(db, user_id)
    _check_email_unique(db, data.email, exclude_id=user_id)

    user.name = data.name
    user.email = data.email
    user.role = data.role
    user.is_active = data.is_active

    db.commit()
    db.refresh(user)
    return user


def partial_update_user(db: Session, user_id: int, data: UserPatch) -> User:
    """Actualiza solo los campos enviados (PATCH)."""
    user = _get_or_404(db, user_id)

    fields = data.model_dump(exclude_none=True)
    if not fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe enviar al menos un campo para actualizar",
        )

    if "email" in fields:
        _check_email_unique(db, fields["email"], exclude_id=user_id)

    for field, value in fields.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int) -> None:
    """Elimina un usuario de la base de datos."""
    user = _get_or_404(db, user_id)
    db.delete(user)
    db.commit()
