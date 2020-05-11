from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from core.database.base import Base

from database.models.basecolumn import BaseColumn

class Match(Base, BaseColumn):
    __tablename__ = 'matches'

    id = Column(Integer, primary_key=True)
    isNotified = Column(Boolean, default=False)

    batchId = Column(String(100), ForeignKey('batches.id'), default=0)
    runId = Column(Integer, ForeignKey('runs.id'))
    subscriptionId = Column(Integer, ForeignKey('subscriptions.id'))
    apartmentId = Column(String(255), ForeignKey('apartments.id'))

    __table_args__ = (
        UniqueConstraint('subscriptionId', 'apartmentId', name='idx_unique_match'),
        {
        'mysql_row_format': 'DYNAMIC'
        }
    )