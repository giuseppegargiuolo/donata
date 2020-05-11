from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from core.database.base import Base

from database.models.basecolumn import BaseColumn

class City(Base, BaseColumn):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))

    publishers = relationship('Publisher', backref='city')
    subscriptions = relationship('Subscription', backref='cities')

    __table_args__ = {
        'mysql_row_format': 'DYNAMIC'
    }