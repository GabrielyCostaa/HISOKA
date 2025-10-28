import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from app.database import get_session
from app.main import app
from app.models import Exam, SensorReading, User, table_registry
from app.security import get_password_hash


@pytest.fixture
def client(session):
    def get_test_session():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_test_session
        yield client

    app.dependency_overrides.clear()


@pytest.fixture(scope='session')
def engine():
    with PostgresContainer('postgres:16', driver='psycopg2') as postgres:
        _engine = create_engine(postgres.get_connection_url())
        with _engine.begin():
            yield _engine


@pytest.fixture
def session(engine):
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def user(session):
    pwd = 'password_test'
    user = User('test_user', get_password_hash(pwd), 'mail@mail.com')
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = pwd

    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.username, 'password': user.clean_password},
    )
    return response.json()['access_token']


@pytest.fixture
def exam(session, user):
    exam = Exam(
        comment='Test exam',
        user_id=user.id,
        user=user,
    )
    session.add(exam)
    session.commit()
    session.refresh(exam)
    return exam


@pytest.fixture
def reading(session, exam):
    reading = SensorReading(
        sensor_id='sensor_1',
        value=42.0,
        timestamp=1625079600.0,
        exam_id=exam.id,
        exam=exam,
    )
    session.add(reading)
    session.commit()
    session.refresh(reading)
    return reading


@pytest.fixture
def bulk_readings(session, exam):
    readings = []
    for i in range(5):
        reading = SensorReading(
            sensor_id=f'sensor_{i}',
            value=40.0 + i,
            timestamp=1625079600.0 + i * 60,
            exam_id=exam.id,
            exam=exam,
        )
        readings.append(reading)
        session.add(reading)

    session.commit()
    for reading in readings:
        session.refresh(reading)
    return readings
