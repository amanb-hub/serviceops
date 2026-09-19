from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.city import City
from app.models.user import User
from app.schemas.client import CityOut
from app.schemas.common import ApiResponse

router = APIRouter(prefix="/cities", tags=["cities"])


@router.get("", response_model=ApiResponse[list[CityOut]])
def list_cities(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> ApiResponse[list[CityOut]]:
    cities = db.query(City).order_by(City.name).all()
    return ApiResponse(success=True, data=[CityOut.model_validate(c) for c in cities])
