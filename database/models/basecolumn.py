from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func

class BaseColumn:
    createdAt = Column(DateTime, server_default=func.now())
    updatedAt = Column(DateTime, server_default=func.now(), onupdate=func.current_timestamp())