from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, ExpiredSignatureError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select

from app.database import get_session
from app.models import User
from app.settings import Settings

settings = Settings()
pwd_context = PasswordHash.recommended()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')

credentials_exception = HTTPException(
    status_code=HTTPStatus.UNAUTHORIZED,
    detail='Could not validate credentials',
    headers={'WWW-Authenticate': 'Bearer'},
)


def create_token(data):
    payload = data.copy()
    expire_date = datetime.now(tz=ZoneInfo('UTC')) + timedelta(minutes=settings.TOKEN_LIFE_MINUTES)

    payload.update({'exp': expire_date})

    token = encode(payload, settings.TOKEN_ASSINATURE_KEY, algorithm=settings.TOKEN_ALGORITHM)

    return token


def get_password_hash(password: str):
    return pwd_context.hash(password)


def match_password_hash(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


def session_user(session=Depends(get_session), token=Depends(oauth2_scheme)):
    try:
        payload = decode(token, settings.TOKEN_ASSINATURE_KEY, algorithms=[settings.TOKEN_ALGORITHM])
        subject = payload.get('sub')
        if not subject:
            raise credentials_exception
    except (DecodeError, ExpiredSignatureError):
        raise credentials_exception

    user = session.scalar(select(User).where(User.username == subject))

    if not user:
        raise credentials_exception

    return user
