# db/crud.py
from sqlalchemy.orm import Session
from . import models
from datetime import datetime

def get_user(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, email: str, password_hash: str, name: str = None):
    db_user = models.User(email=email, name=name, password_hash=password_hash)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_emission_record(db: Session, user_id: int, category: str, quantity: float, emission: float, scope: str = None, **kwargs):
    record = models.EmissionRecord(
        user_id=user_id,
        category=category,
        quantity=quantity,
        emission=emission,
        scope=scope,
        reporting_period_start=kwargs.get("reporting_period_start"),
        reporting_period_end=kwargs.get("reporting_period_end"),
        location=kwargs.get("location"),
        data_source=kwargs.get("data_source"),
        is_verified=kwargs.get("is_verified", "false")
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_user_emissions(db: Session, user_id: int):
    return db.query(models.EmissionRecord).filter(models.EmissionRecord.user_id == user_id).order_by(models.EmissionRecord.timestamp.desc()).all()
