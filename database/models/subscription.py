from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from core.database.base import Base

from database.models.basecolumn import BaseColumn

class Subscription(Base, BaseColumn):
    __tablename__ = 'subscriptions'

    id = Column(Integer, primary_key=True)
    isActive = Column(Boolean, default=True)

    labelId = Column(Integer, ForeignKey('labels.id'))
    cityId = Column(Integer, ForeignKey('cities.id'))
    restrictionId = Column(Integer, ForeignKey('restrictions.id'), nullable=True)
    userId = Column(Integer, ForeignKey('users.id'), nullable=True)
    
    matches = relationship('Match', backref='subscription')

    __table_args__ = {
        'mysql_row_format': 'DYNAMIC'
    }