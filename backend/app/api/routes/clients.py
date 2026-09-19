from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_roles
from app.db.session import get_db
from app.models.client import Client
from app.models.client_user import ClientUser
from app.models.role import RoleName
from app.models.user import User
from app.schemas.client import ClientCreate, ClientOut
from app.schemas.common import ApiResponse

router = APIRouter(prefix="/clients", tags=["clients"])

# Roles allowed to see every client
GLOBAL_CLIENT_ACCESS_ROLES = {
    RoleName.SUPER_ADMIN,
    RoleName.OPERATIONS_MANAGER,
    RoleName.CITY_MANAGER,
    RoleName.SERVICE_COORDINATOR,
    RoleName.FINANCE_ADMIN,
}


@router.get("", response_model=ApiResponse[list[ClientOut]])
def list_clients(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> ApiResponse[list[ClientOut]]:
    """
    Multi-tenant enforcement happens here, not in the frontend:
    a CLIENT_USER only ever sees the client(s) they are linked to.
    """
    if current_user.role.name in GLOBAL_CLIENT_ACCESS_ROLES:
        clients = db.query(Client).order_by(Client.name).all()
    else:
        clients = (
            db.query(Client)
            .join(ClientUser, ClientUser.client_id == Client.id)
            .filter(ClientUser.user_id == current_user.id)
            .order_by(Client.name)
            .all()
        )

    return ApiResponse(success=True, data=[ClientOut.model_validate(c) for c in clients])


@router.post("", response_model=ApiResponse[ClientOut], status_code=status.HTTP_201_CREATED)
def create_client(
    payload: ClientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(RoleName.SUPER_ADMIN, RoleName.OPERATIONS_MANAGER)
    ),
) -> ApiResponse[ClientOut]:
    client = Client(
        name=payload.name,
        code=payload.code.upper(),
        contact_name=payload.contact_name,
        contact_email=payload.contact_email,
        contact_phone=payload.contact_phone,
    )
    db.add(client)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="A client with this code already exists"
        )
    db.refresh(client)
    return ApiResponse(success=True, data=ClientOut.model_validate(client), message="Client created")
