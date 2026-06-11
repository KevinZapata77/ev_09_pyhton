from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Optional
from app.schemas.user_schema import UserCreate, UserUpdate, UserPatch, UserResponse
from app.services import user_service
from app.dependencies.database_dependency import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "/",
    response_model=list[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar todos los usuarios",
    description=(
        "Retorna la lista de usuarios registrados en la base de datos. "
        "Se puede filtrar por **rol** o **estado activo** y ordenar por campo."
    ),
)
def list_users(
    role: Optional[str] = Query(
        default=None,
        description="Filtrar por rol: admin, user, support",
    ),
    is_active: Optional[bool] = Query(
        default=None,
        description="Filtrar por estado: true = activos, false = inactivos",
    ),
    order_by: str = Query(
        default="id",
        description="Ordenar por: id, name, created_at (prefijo '-' para descendente)",
    ),
    db: Session = Depends(get_db),
):
    return user_service.get_all_users(db, role=role, is_active=is_active, order_by=order_by)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener usuario por ID",
    description="Retorna los datos completos de un usuario específico por su ID.",
)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return user_service.get_user_by_id(db, user_id)


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo usuario",
    description=(
        "Crea un nuevo usuario en la base de datos. "
        "El **email** debe ser único. El **rol** debe ser uno de: admin, user, support. "
        "El **nombre** requiere mínimo 3 caracteres."
    ),
)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, data)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar usuario completo (PUT)",
    description="Reemplaza **todos** los campos del usuario. Se requieren todos los campos.",
)
def update_user(user_id: int, data: UserUpdate, db: Session = Depends(get_db)):
    return user_service.update_user(db, user_id, data)


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar usuario parcialmente (PATCH)",
    description="Modifica solo los campos enviados en el body. Se debe enviar al menos uno.",
)
def partial_update_user(user_id: int, data: UserPatch, db: Session = Depends(get_db)):
    return user_service.partial_update_user(db, user_id, data)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar usuario",
    description="Elimina permanentemente un usuario de la base de datos. Retorna 204 sin cuerpo.",
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_service.delete_user(db, user_id)
