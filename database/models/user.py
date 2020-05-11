from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from core.database.base import Base

from database.models.basecolumn import BaseColumn

class User(Base, BaseColumn):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    surname = Column(String(50))
    isActive = Column(Boolean, default=True)
    email = Column(String(100), nullable=True)
    telegram = Column(String(255), nullable=True)
    username = Column(String(100), nullable=True)
    password = Column(String(100), nullable=True)
    
    groupId = Column(Integer, ForeignKey('groups.id'))

    subscriptions = relationship('Subscription', backref='user')

    __table_args__ = {
        'mysql_row_format': 'DYNAMIC'
    }