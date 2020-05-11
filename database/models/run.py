import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from core.database.base import Base

from database.models.basecolumn import BaseColumn

class Run(Base, BaseColumn):
    __tablename__ = 'runs'

    id = Column(Integer, primary_key=True)
    startedAt = Column(DateTime)
    finishedAt = Column(DateTime, nullable=True)
    
    apartments = relationship('Apartment', backref='runs')
    matches = relationship('Match', backref='runs')

    __table_args__ = {
        'mysql_row_format': 'DYNAMIC'
    }