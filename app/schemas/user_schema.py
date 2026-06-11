from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime

# ─── Roles permitidos ─────────────────────────────────────────────────────────
ALLOWED_ROLES = {"admin", "user", "support"}


# ─── Schemas de entrada ───────────────────────────────────────────────────────

class UserCreate(BaseModel):
    """Schema para crear un usuario — usado en POST /users."""
    name: str = Field(..., min_length=3, max_length=100, examples=["Kevin Zapata"])
    email: EmailStr = Field(..., examples=["kevin@devicesystems.com"])
    role: str = Field(..., examples=["admin"])
    is_active: bool = Field(default=True)

    @field_validator("role")
    @classmethod
    def validate_role(cls, value: str) -> str:
        if value not in ALLOWED_ROLES:
            raise ValueError(f"Rol '{value}' no permitido. Roles válidos: {sorted(ALLOWED_ROLES)}")
        return value

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("El nombre no puede estar vacío o ser solo espacios")
        return value.strip()


class UserUpdate(BaseModel):
    """Schema para actualización completa — usado en PUT /users/{id}."""
    name: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    role: str
    is_active: bool

    @field_validator("role")
    @classmethod
    def validate_role(cls, value: str) -> str:
        if value not in ALLOWED_ROLES:
            raise ValueError(f"Rol '{value}' no permitido. Roles válidos: {sorted(ALLOWED_ROLES)}")
        return value


class UserPatch(BaseModel):
    """Schema para actualización parcial — usado en PATCH /users/{id}."""
    name: Optional[str] = Field(default=None, min_length=3, max_length=100)
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None

    @field_validator("role")
    @classmethod
    def validate_role(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and value not in ALLOWED_ROLES:
            raise ValueError(f"Rol '{value}' no permitido. Roles válidos: {sorted(ALLOWED_ROLES)}")
        return value


# ─── Schema de respuesta ──────────────────────────────────────────────────────

class UserResponse(BaseModel):
    """Schema de respuesta pública — lo que devuelve la API al cliente."""
    id: int
    name: str
    email: str
    role: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
