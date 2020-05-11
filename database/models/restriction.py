from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from core.database.base import Base

from database.models.basecolumn import BaseColumn

class Restriction(Base, BaseColumn):
    __tablename__ = 'restrictions'

    id = Column(Integer, primary_key=True)
    minRooms = Column(Integer)
    maxRooms = Column(Integer)
    minSurface = Column(Integer)
    maxSurface = Column(Integer)
    minPrice = Column(Integer)
    maxPrice = Column(Integer)
    
    subscriptions = relationship('Subscription', backref='restrictions')

    __table_args__ = {
        'mysql_row_format': 'DYNAMIC'
    }