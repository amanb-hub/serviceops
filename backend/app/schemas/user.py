import uuid

from pydantic import BaseModel, Field

# NOTE: plain `str` is used for email fields rather than pydantic's EmailStr.
# EmailStr's underlying email-validator library rejects reserved/special-use
# TLDs such as ".local" (used for local development accounts, e.g.
# admin@serviceops.local), which would break login for seeded dev users.


class RoleOut(BaseModel):
    id: uuid.UUID
    name: str

    class Config:
        from_attributes = True


class UserOut(BaseModel):
    id: uuid.UUID
    name: str
    email: str
    phone: str | None = None
    is_active: bool
    role: RoleOut

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    email: str
    phone: str | None = None
    password: str = Field(min_length=8, max_length=128)
    role_id: uuid.UUID


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut
