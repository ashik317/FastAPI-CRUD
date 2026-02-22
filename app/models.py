from sqlalchemy import Column, Integer, String, Text, Numeric, DateTime
from app.database import Base
from datetime import datetime

class CourseModel(Base):
    __tablename__ = "Courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    duration = Column(Numeric, nullable=False)
    instructor = Column(String(255), nullable=False)
    website = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(255), nullable=True)
    updated_by = Column(String(255), nullable=True)
    status = Column(String(50), default="active")


class UserModel(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)