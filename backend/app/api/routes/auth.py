from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.security import create_access_token
from app.db.session import get_db
from app.models.user import User
from app.schemas.common import ApiResponse
from app.schemas.user import LoginRequest, TokenResponse, UserOut
from app.services.auth_service import authenticate_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=ApiResponse[TokenResponse])
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> ApiResponse[TokenResponse]:
    user = authenticate_user(db, payload.email, payload.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token(subject=str(user.id), extra_claims={"role": user.role.name})
    return ApiResponse(
        success=True,
        data=TokenResponse(access_token=token, user=UserOut.model_validate(user)),
        message="Login successful",
    )


@router.get("/me", response_model=ApiResponse[UserOut])
def get_me(current_user: User = Depends(get_current_user)) -> ApiResponse[UserOut]:
    return ApiResponse(success=True, data=UserOut.model_validate(current_user), message="Success")
