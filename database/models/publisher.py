from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from core.database.base import Base

from database.models.basecolumn import BaseColumn

class Publisher(Base, BaseColumn):
    __tablename__ = 'publishers'

    id = Column(Integer, primary_key=True)
    url = Column(String(255))    
    isActive = Column(Boolean, default=True)

    labelId = Column(Integer, ForeignKey('labels.id'))
    cityId = Column(Integer, ForeignKey('cities.id'))

    pages = relationship('Page', backref='publishers')
    
    __table_args__ = {
        'mysql_row_format': 'DYNAMIC'
    }