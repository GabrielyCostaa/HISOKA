from http import HTTPStatus
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as Session_type

from app.database import get_session
from app.models import Exam, SensorReading, User
from app.schemas import (
    SensorReadingBulkCreateSchema,
    SensorReadingBulkResponseSchema,
    SensorReadingCreateSchema,
    SensorReadingSchema,
)
from app.security import session_user

router = APIRouter(
    prefix='/reading',
    responses={404: {'description': 'Not found'}},
)

Session = Annotated[Session_type, Depends(get_session)]
SessionUser = Annotated[User, Depends(session_user)]


@router.post('/exams/{exam_id}', status_code=HTTPStatus.CREATED, response_model=SensorReadingSchema)
def create_reading(
    exam_id: int,
    reading_data: SensorReadingCreateSchema,
    session: Session,
    user: SessionUser,
):
    """
    Create a SensorReading linked to a specific Exam.
    """

    # Ensure the exam exists
    exam = session.get(Exam, exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail='Exam not found')

    # Create reading and link to the exam
    reading = SensorReading(
        sensor_id=reading_data.sensor_id,
        value=reading_data.value,
        timestamp=reading_data.timestamp,
        exam_id=exam.id,
        exam=exam,
    )

    session.add(reading)
    session.commit()
    session.refresh(reading)
    return reading


@router.get('/exams/{exam_id}', status_code=HTTPStatus.OK, response_model=List[SensorReadingSchema])
def get_readings(
    exam_id: int,
    session: Session,
    user: SessionUser,
):
    """
    Retrieve all SensorReadings for a specific Exam.
    """

    exam = session.get(Exam, exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail='Exam not found')

    return exam.readings  # relationship provides all readings


@router.post('/exams/{exam_id}/bulk', status_code=HTTPStatus.CREATED, response_model=List[SensorReadingBulkResponseSchema])
def create_bulk_readings(
    exam_id: int,
    bulk_data: List[SensorReadingBulkCreateSchema],
    session: Session,
    user: SessionUser,
):
    exam = session.get(Exam, exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail='Exam not found')

    response_data = []

    for sensor in bulk_data:
        timestamps = sensor.timestamps
        if len(timestamps) != len(sensor.readings):
            raise HTTPException(
                status_code=400, detail=f'timestamps and readings length mismatch for sensor {sensor.sensor_id}'
            )

        readings_objs = [
            SensorReading(sensor_id=sensor.sensor_id, value=value, timestamp=ts, exam=exam, exam_id=exam.id)
            for value, ts in zip(sensor.readings, timestamps)
        ]

        session.add_all(readings_objs)

        response_data.append(
            SensorReadingBulkResponseSchema(sensor_id=sensor.sensor_id, readings=sensor.readings, timestamps=timestamps)
        )

    session.commit()

    return response_data


@router.get('/exams/{exam_id}/bulk', status_code=HTTPStatus.OK, response_model=List[SensorReadingBulkResponseSchema])
def get_bulk_readings(
    exam_id: int,
    session: Session,
    user: SessionUser,
):
    exam = session.get(Exam, exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail='Exam not found')

    # group readings by sensor_id
    grouped = {}
    for reading in exam.readings:
        grouped.setdefault(reading.sensor_id, {'readings': [], 'timestamps': []})
        grouped[reading.sensor_id]['readings'].append(reading.value)
        grouped[reading.sensor_id]['timestamps'].append(reading.timestamp)

    return [
        SensorReadingBulkResponseSchema(sensor_id=sensor_id, readings=data['readings'], timestamps=data['timestamps'])
        for sensor_id, data in grouped.items()
    ]
