import time
from typing import Annotated
from uuid import uuid4

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer

SECRET = "my-secret"
ALGORITHM = "HS256"


def sign_jwt(user_id: int) -> dict:
    now = int(time.time())

    payload = {
        "iss": "curso-fastapi.com.br",
        "sub": str(user_id),  # ✅ corrigido (string)
        "aud": "curso-fastapi",
        "exp": now + (60 * 30),  # 30 min
        "iat": now,
        "nbf": now,
        "jti": uuid4().hex,
    }

    token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)

    return {"access_token": token}


async def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(
            token,
            SECRET,
            audience="curso-fastapi",
            issuer="curso-fastapi.com.br",  # ✅ valida issuer
            algorithms=[ALGORITHM],
        )
        return decoded_token

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado",
        )

    except jwt.InvalidTokenError as e:
        print("ERRO JWT:", e)  # ajuda debug
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
        )


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request) -> dict:
        authorization = request.headers.get("Authorization")

        if not authorization:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Header Authorization ausente",
            )

        scheme, _, token = authorization.partition(" ")

        if scheme != "Bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Formato inválido. Use: Bearer <token>",
            )

        return await decode_jwt(token)


async def get_current_user(
        token: Annotated[dict, Depends(JWTBearer())]
) -> dict:
    return {"user_id": int(token["sub"])}


def login_required(
        current_user: Annotated[dict, Depends(get_current_user)]
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado",
        )
    return current_user
