import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from core.database.base import Base

from database.models.basecolumn import BaseColumn

class Parameter(Base, BaseColumn):
    __tablename__ = 'parameters'

    id = Column(Integer, primary_key=True)        
    name = Column(String(100))
    value = Column(String(100))

    __table_args__ = {
        'mysql_row_format': 'DYNAMIC'
    }