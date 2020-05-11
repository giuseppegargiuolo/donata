from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey

from core.database.base import Base

class ModelBase(Base):
    # createdAt = Column(DateTime)
    updatedAt = Column(DateTime)