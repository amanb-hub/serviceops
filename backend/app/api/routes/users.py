from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import require_roles
from app.core.security import hash_password
from app.db.session import get_db
from app.models.role import RoleName
from app.models.user import User
from app.schemas.common import ApiResponse
from app.schemas.user import UserCreate, UserOut

router = APIRouter(prefix="/users", tags=["users"])

ADMIN_ROLES = (RoleName.SUPER_ADMIN, RoleName.OPERATIONS_MANAGER)


@router.get("", response_model=ApiResponse[list[UserOut]])
def list_users(
    db: Session = Depends(get_db), current_user: User = Depends(require_roles(*ADMIN_ROLES))
) -> ApiResponse[list[UserOut]]:
    users = db.query(User).order_by(User.name).all()
    return ApiResponse(success=True, data=[UserOut.model_validate(u) for u in users])


@router.post("", response_model=ApiResponse[UserOut], status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(*ADMIN_ROLES)),
) -> ApiResponse[UserOut]:
    user = User(
        name=payload.name,
        email=payload.email.lower(),
        phone=payload.phone,
        password_hash=hash_password(payload.password),
        role_id=payload.role_id,
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="A user with this email already exists"
        )
    db.refresh(user)
    return ApiResponse(success=True, data=UserOut.model_validate(user), message="User created")
