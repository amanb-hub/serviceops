import uuid

from pydantic import BaseModel, Field


class ClientOut(BaseModel):
    id: uuid.UUID
    name: str
    code: str
    contact_name: str | None = None
    contact_email: str | None = None
    contact_phone: str | None = None
    status: str

    class Config:
        from_attributes = True


class ClientCreate(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    code: str = Field(min_length=1, max_length=32)
    contact_name: str | None = None
    contact_email: str | None = None
    contact_phone: str | None = None


class CityOut(BaseModel):
    id: uuid.UUID
    name: str
    state: str | None = None
    country: str
    status: str

    class Config:
        from_attributes = True
