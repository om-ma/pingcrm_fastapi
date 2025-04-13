from datetime import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func

class TimestampMixin:
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
