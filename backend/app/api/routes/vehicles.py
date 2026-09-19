import csv
import io
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_roles
from app.db.session import get_db
from app.models.client import Client
from app.models.role import RoleName
from app.models.user import User
from app.models.vehicle import Vehicle
from app.schemas.common import ApiResponse
from app.schemas.vehicle import (
    VehicleCreate,
    VehicleImportResult,
    VehicleOut,
    VehicleUpdate,
)

router = APIRouter(prefix="/vehicles", tags=["vehicles"])

ADMIN_ROLES = (RoleName.SUPER_ADMIN, RoleName.OPERATIONS_MANAGER)


@router.get("", response_model=ApiResponse[list[VehicleOut]])
def list_vehicles(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    client_id: uuid.UUID | None = None,
    city_id: uuid.UUID | None = None,
    search: str | None = Query(default=None, description="Match against registration number"),
    limit: int = Query(default=100, le=500),
    offset: int = Query(default=0, ge=0),
) -> ApiResponse[list[VehicleOut]]:
    q = db.query(Vehicle)
    if client_id:
        q = q.filter(Vehicle.client_id == client_id)
    if city_id:
        q = q.filter(Vehicle.city_id == city_id)
    if search:
        q = q.filter(Vehicle.registration_number.ilike(f"%{search}%"))
    vehicles = q.order_by(Vehicle.registration_number).offset(offset).limit(limit).all()
    return ApiResponse(success=True, data=[VehicleOut.model_validate(v) for v in vehicles])


@router.post("", response_model=ApiResponse[VehicleOut], status_code=status.HTTP_201_CREATED)
def create_vehicle(
    payload: VehicleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(*ADMIN_ROLES)),
) -> ApiResponse[VehicleOut]:
    vehicle = Vehicle(**payload.model_dump())
    db.add(vehicle)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A vehicle with this registration number already exists",
        )
    db.refresh(vehicle)
    return ApiResponse(success=True, data=VehicleOut.model_validate(vehicle), message="Vehicle created")


@router.patch("/{vehicle_id}", response_model=ApiResponse[VehicleOut])
def update_vehicle(
    vehicle_id: uuid.UUID,
    payload: VehicleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(*ADMIN_ROLES)),
) -> ApiResponse[VehicleOut]:
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(vehicle, field, value)
    db.commit()
    db.refresh(vehicle)
    return ApiResponse(success=True, data=VehicleOut.model_validate(vehicle), message="Vehicle updated")


@router.post("/import", response_model=ApiResponse[VehicleImportResult])
async def import_vehicles(
    file: UploadFile,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(*ADMIN_ROLES)),
) -> ApiResponse[VehicleImportResult]:
    """
    Bulk-load vehicles from a CSV for initial fleet onboarding.
    Expected columns (header row, case-insensitive):
      registration_number (required), client_code, city_name, make, model, vehicle_type, status
    client_code / city_name are matched against existing Clients/Cities by code/name;
    unmatched values are left null on the row rather than failing the whole import.
    """
    raw = await file.read()
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File must be UTF-8 encoded CSV")

    reader = csv.DictReader(io.StringIO(text))
    if reader.fieldnames is None:
        raise HTTPException(status_code=400, detail="CSV appears to be empty")
    headers = {h.strip().lower(): h for h in reader.fieldnames}
    if "registration_number" not in headers:
        raise HTTPException(
            status_code=400, detail="CSV must include a 'registration_number' column"
        )

    clients_by_code = {c.code: c for c in db.query(Client).all()}
    from app.models.city import City

    cities_by_name = {c.name.lower(): c for c in db.query(City).all()}
    existing_regs = {v.registration_number for v in db.query(Vehicle.registration_number).all()}

    created, skipped, errors = 0, 0, []
    for i, row in enumerate(reader, start=2):  # start=2: row 1 is the header
        reg = (row.get(headers["registration_number"]) or "").strip().upper()
        if not reg:
            errors.append(f"Row {i}: missing registration_number, skipped")
            continue
        if reg in existing_regs:
            skipped += 1
            continue

        client_code = (row.get(headers.get("client_code", "")) or "").strip().upper()
        city_name = (row.get(headers.get("city_name", "")) or "").strip()
        client = clients_by_code.get(client_code) if client_code else None
        city = cities_by_name.get(city_name.lower()) if city_name else None

        vehicle = Vehicle(
            registration_number=reg,
            client_id=client.id if client else None,
            city_id=city.id if city else None,
            make=(row.get(headers.get("make", "")) or "").strip() or None,
            model=(row.get(headers.get("model", "")) or "").strip() or None,
            vehicle_type=(row.get(headers.get("vehicle_type", "")) or "").strip() or None,
            status=(row.get(headers.get("status", "")) or "ACTIVE").strip().upper() or "ACTIVE",
        )
        db.add(vehicle)
        existing_regs.add(reg)
        created += 1

    db.commit()
    return ApiResponse(
        success=True,
        data=VehicleImportResult(created=created, skipped_duplicates=skipped, errors=errors),
        message=f"Imported {created} vehicle(s), skipped {skipped} duplicate(s)",
    )
