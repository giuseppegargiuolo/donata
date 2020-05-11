from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from core.database.base import Base

from database.models.basecolumn import BaseColumn

class Group(Base, BaseColumn):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    adminId = Column(Integer, ForeignKey('users.id'), nullable=True)

    __table_args__ = {
        'mysql_row_format': 'DYNAMIC'
    }