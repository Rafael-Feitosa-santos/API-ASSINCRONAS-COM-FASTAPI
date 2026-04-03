from fastapi import APIRouter

from dio_blog.src.schemas.auth import LoginIn
from dio_blog.src.security import sign_jwt
from dio_blog.src.views.auth import LoginOut

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginOut)
async def login(data: LoginIn):
    return sign_jwt(user_id=data.user_id)
