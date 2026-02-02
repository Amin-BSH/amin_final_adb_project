import os
import time

import jwt
from dotenv import load_dotenv
from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")


def token_response(token: str) -> dict:
    return {"access token": token}


def sign_jwt(identifier: str):
    payload = {
        "user-identifier": identifier,
        "expires": time.time() + 6000,
    }
    token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
    return token_response(token)


def decode_jwt(token: str):
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, JWT_ALGORITHM)
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:  # noqa: E722
        return {}


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(
            auto_error=auto_error,
        )

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme..!"
                )
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail="Invalid or expired token..!"
                )

            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code..!")

    def verify_jwt(self, jwttoken: str) -> bool:
        is_token_valid = False
        try:
            payload = decode_jwt(jwttoken)
        except:
            payload = None

        if payload:
            is_token_valid = True

        return is_token_valid
