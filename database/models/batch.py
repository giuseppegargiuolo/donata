from sqlalchemy import Column, Boolean, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from core.database.base import Base

from database.models.basecolumn import BaseColumn

class Batch(Base, BaseColumn):
    __tablename__ = 'batches'

    id = Column(String(255), primary_key=True, autoincrement=False)
    isLocked = Column(Boolean, default=False)
    isProcessed = Column(Boolean, default=False)

    matches = relationship('Match', backref='batch')

    __table_args__ = {
        'mysql_row_format': 'DYNAMIC'
    }