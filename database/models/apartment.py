from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from core.database.base import Base

from database.models.basecolumn import BaseColumn

class Apartment(Base, BaseColumn):
    __tablename__ = 'apartments'

    id = Column(String(255), primary_key=True, autoincrement=False)
    refNo = Column(String(100))
    title = Column(String(255))
    subtitle = Column(String(255))
    description = Column(Text())
    rooms = Column(Integer)
    price = Column(Integer)
    surface = Column(Integer)
    url = Column(String(255))
    pageId = Column(String(255), ForeignKey('pages.id'))
    runId = Column(Integer, ForeignKey('runs.id'))

    apartment = relationship('Match', backref='apartment')

    __table_args__ = {
        'mysql_row_format': 'DYNAMIC'
    }