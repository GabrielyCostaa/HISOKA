from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session as Session_type

from app.database import get_session
from app.models import User
from app.schemas import Token
from app.security import create_token, match_password_hash

router = APIRouter(prefix='/auth', tags=['auth'])
Session = Annotated[Session_type, Depends(get_session)]
OAuthForm = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post('/token', response_model=Token)
def get_token(data: OAuthForm, session: Session):
    user = session.scalar(select(User).where(User.username == data.username))

    if not user or not match_password_hash(data.password, user.password):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Usuário ou Senha inválidos')
    token = create_token({'sub': user.username})
    return {'access_token': token, 'token_type': 'bearer', 'user_id': user.id}
