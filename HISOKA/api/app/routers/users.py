from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session as Session_type

from app.database import get_session
from app.models import User
from app.schemas import Message, UserList, UserPublic, UserSchema
from app.security import get_password_hash, session_user

router = APIRouter(
    prefix='/users',
    responses={404: {'description': 'Not found'}},
)

Session = Annotated[Session_type, Depends(get_session)]
SessionUser = Annotated[User, Depends(session_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session):
    db_user = session.scalar(select(User).where((User.username == user.username) | (User.email == user.email)))

    if db_user:
        if db_user.username == user.username or db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username or Email already exists',
            )

    db_user = User(username=user.username, password=get_password_hash(user.password), email=user.email)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.get('/', response_model=UserList)
def read_users(
    session: Session,
    skip: int = 0,
    limit: int = 100,
):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {'users': users}


@router.get('/profile', response_model=UserPublic)
def read_user_profile(session_user: SessionUser):
    return session_user


@router.put('/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema, session: Session, session_user: SessionUser):
    try:
        session_user.username = user.username
        session_user.password = get_password_hash(user.password)
        session_user.email = user.email
        session.commit()
        session.refresh(session_user)

        return session_user

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or Email already exists',
        )


@router.delete('/{user_id}', response_model=Message)
def delete_user(user_id: int, session: Session, session_user: SessionUser):
    session.delete(session_user)
    session.commit()

    return {'message': 'User deleted'}
