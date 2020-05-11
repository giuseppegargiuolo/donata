from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from core.database.base import Base

from database.models.basecolumn import BaseColumn

class Label(Base, BaseColumn):
    __tablename__ = 'labels'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    publishers = relationship('Publisher', backref='label')
    subscriptions = relationship('Subscription', backref='label')

    __table_args__ = {
        'mysql_row_format': 'DYNAMIC'
    }