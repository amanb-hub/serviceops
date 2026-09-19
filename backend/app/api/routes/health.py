from fastapi import APIRouter

from app.schemas.common import ApiResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=ApiResponse[dict])
def health_check() -> ApiResponse[dict]:
    return ApiResponse(success=True, data={"status": "healthy"}, message="ServiceOps API is running")
