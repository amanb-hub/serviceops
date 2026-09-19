import uuid

from pydantic import BaseModel, Field


class VehicleOut(BaseModel):
    id: uuid.UUID
    registration_number: str
    client_id: uuid.UUID | None = None
    city_id: uuid.UUID | None = None
    make: str | None = None
    model: str | None = None
    vehicle_type: str | None = None
    status: str

    class Config:
        from_attributes = True


class VehicleCreate(BaseModel):
    registration_number: str = Field(min_length=1, max_length=32)
    client_id: uuid.UUID | None = None
    city_id: uuid.UUID | None = None
    make: str | None = None
    model: str | None = None
    vehicle_type: str | None = None
    status: str = "ACTIVE"


class VehicleUpdate(BaseModel):
    client_id: uuid.UUID | None = None
    city_id: uuid.UUID | None = None
    make: str | None = None
    model: str | None = None
    vehicle_type: str | None = None
    status: str | None = None


class VehicleImportResult(BaseModel):
    created: int
    skipped_duplicates: int
    errors: list[str]
