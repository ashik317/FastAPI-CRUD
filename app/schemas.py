# app/schemas.py
from enum import Enum
from typing import Optional
from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime


class CourseStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"


class CourseCreate(BaseModel):
    name: str
    description: str | None = None
    duration: Decimal
    instructor: str
    website: str | None = None
    created_by: str | None = None
    updated_by: str | None = None
    status: CourseStatus = CourseStatus.ACTIVE

    model_config = {"use_enum_values": True}


class CousereResponse(BaseModel):
    name: str
    description: str | None = None
    duration: Decimal
    instructor: str
    website: str | None = None
    created_by: str | None = None
    updated_by: str | None = None
    status: CourseStatus = CourseStatus.ACTIVE
    id: int
    cretor_id: int

    class Config:
        orm_mode = True


class CourseUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    duration: Optional[Decimal] = None
    instructor: Optional[str] = None
    website: Optional[str] = None
    updated_by: Optional[str] = None
    status: Optional[CourseStatus] = None

    model_config = {"use_enum_values": True}


class UserRegistration(BaseModel):
    username: str
    email: str
    password: str

    model_config = {"use_enum_values": True}


class UserList(BaseModel):
    id: int
    username: Optional[str] = None
    email: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"use_enum_values": True, "from_attributes": True}


class LoginRequest(BaseModel):
    email: str
    password: str

    model_config = {"use_enum_values": True}


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    message: str


class VerifyTokenResponse(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None
