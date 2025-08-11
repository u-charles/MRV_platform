# db/models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    emissions = relationship("EmissionRecord", back_populates="user", cascade="all, delete-orphan")

class EmissionRecord(Base):
    __tablename__ = "emission_records"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category = Column(String(100), nullable=False)
    quantity = Column(Float, nullable=False)
    emission = Column(Float, nullable=False)  # kg CO2e
    scope = Column(String(20), nullable=True)
    reporting_period_start = Column(DateTime, nullable=True)
    reporting_period_end = Column(DateTime, nullable=True)
    location = Column(String(255), nullable=True)
    data_source = Column(String(255), nullable=True)
    is_verified = Column(String(10), default="false")
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="emissions")
