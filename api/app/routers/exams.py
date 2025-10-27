from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session as Session_type

from app.database import get_session
from app.models import Exam, User
from app.schemas import ExamCreateSchema, ExamSchema
from app.security import session_user

router = APIRouter(
    prefix='/exams',
    responses={404: {'description': 'Not found'}},
)


Session = Annotated[Session_type, Depends(get_session)]
SessionUser = Annotated[User, Depends(session_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=ExamSchema)
def create_exam(exam_data: ExamCreateSchema, session: Session, current_user: SessionUser):
    db_exam = Exam(
        comment=exam_data.comment,
        user=current_user,  # pass user object, SQLAlchemy will handle user_id
        user_id=current_user.id,
    )

    session.add(db_exam)
    session.commit()
    session.refresh(db_exam)

    return db_exam


@router.get('/{exam_id}', response_model=ExamSchema)
def read_exam(exam_id: int, session: Session, user: SessionUser):
    db_exam = session.get(Exam, exam_id)

    if not db_exam:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Exam not found',
        )

    return db_exam


@router.get('/', response_model=list[ExamSchema])
def read_exams(
    session: Session,
    user: SessionUser,
    skip: int = 0,
    limit: int = 100,
):
    exams = session.scalars(select(Exam).where(Exam.user_id == user.id).offset(skip).limit(limit)).all()
    return exams

@router.delete('/{exam_id}', status_code=HTTPStatus.NO_CONTENT)
def delete_exam(exam_id: int, session: Session, user: SessionUser):
    db_exam = session.get(Exam, exam_id)

    if not db_exam:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Exam not found',
        )

    session.delete(db_exam)
    session.commit()
    return None