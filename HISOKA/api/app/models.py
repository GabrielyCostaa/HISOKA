from datetime import datetime
from typing import List, Optional

from sqlalchemy import Float, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str]
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())

    # 1:N -> User has many Exams
    exams: Mapped[List['Exam']] = relationship(
        'Exam',
        back_populates='user',
        cascade='all, delete-orphan',
        default_factory=list,  # safe default
    )


@table_registry.mapped_as_dataclass
class Exam:
    __tablename__ = 'exams'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())

    # Foreign key to User
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey('users.id'), nullable=True)
    user: Mapped[Optional['User']] = relationship(
        'User',
        back_populates='exams',
    )

    # 1:N -> Exam has many SensorReadings
    readings: Mapped[List['SensorReading']] = relationship(
        'SensorReading',
        back_populates='exam',
        cascade='all, delete-orphan',
        default_factory=list,  # safe default
        passive_deletes=True,
    )


@table_registry.mapped_as_dataclass
class SensorReading:
    __tablename__ = 'sensor_readings'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    sensor_id: Mapped[str] = mapped_column(String, nullable=False)
    timestamp: Mapped[float] = mapped_column(Float, nullable=False)
    value: Mapped[float] = mapped_column(Float, nullable=False)

    # Foreign key to Exam
    exam_id: Mapped[int] = mapped_column(ForeignKey('exams.id', ondelete='CASCADE'), nullable=False)
    exam: Mapped['Exam'] = relationship('Exam', back_populates='readings')
