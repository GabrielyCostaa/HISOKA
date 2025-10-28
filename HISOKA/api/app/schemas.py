from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class Message(BaseModel):
    message: str


class Token(BaseModel):
    access_token: str
    token_type: str  # Bearer? default.
    user_id: int


class ExamCreateSchema(BaseModel):
    comment: Optional[str] = None


class ExamSchema(BaseModel):
    id: int
    comment: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True


# Input schema for creating a reading
class SensorReadingCreateSchema(BaseModel):
    sensor_id: str
    value: float
    timestamp: Optional[float] = None  # optional, defaults to now


# Output schema for returning a reading
class SensorReadingSchema(BaseModel):
    id: int
    sensor_id: str
    value: float
    timestamp: float

    class Config:
        orm_mode = True


class SensorReadingBulkCreateSchema(BaseModel):
    sensor_id: str
    readings: List[float]
    timestamps: Optional[List[float]] = None  # optional, defaults to now for missing


class SensorReadingBulkResponseSchema(BaseModel):
    sensor_id: str
    readings: List[float]
    timestamps: List[float]
