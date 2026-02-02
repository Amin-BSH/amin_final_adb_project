import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.database import get_session

SessionDep = Annotated[Session, Depends(get_session)]

load_dotenv()
pwd_context = CryptContext(schemes=os.getenv("CRYPTO_CONTEXT_SCHEMA"))


class Hasher:
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)
