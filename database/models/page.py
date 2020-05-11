from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from core.database.base import Base

from database.models.basecolumn import BaseColumn

class Page(Base, BaseColumn):
    __tablename__ = 'pages'

    id = Column(String(255), primary_key=True, autoincrement=False)
    number = Column(Integer)
    url = Column(String(255))

    publisherId = Column(Integer, ForeignKey('publishers.id'))

    apartments = relationship('Apartment', backref='pages')

    __table_args__ = {
        'mysql_row_format': 'DYNAMIC'
    }