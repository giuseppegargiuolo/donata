import traceback
from datetime import datetime
import importlib

from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import desc
from sqlalchemy.inspection import inspect

class Repository:
    
    def __init__(self, db, session):
        self.db = db
        self.session = session

    def all(self):
        return self.session.all()

    def query(self, query):
        return self.session.query(query)

    def save(self, entity):
        try:
            record = self.session.query(type(entity)).filter(type(entity).id == entity.id).first()
            if record is None:        
                self.session.add(entity)
            else:
                self.update(entity)
        except:
            pass

        # self.session.flush()
        return entity

    def update(self, entity):
        self.session.query(type(entity)).filter_by(id = entity.id).with_for_update().update({ column: getattr(entity, column) for column in type(entity).__table__.columns.keys() })
    
    def close(self):        
        self.session.close()
        self.db.dispose()

    def getPrimaryKey(self, entity):
        return [key.name for key in inspect(type(entity)).primary_key]

    def bulkInsert(self, values):
        self.session.bulk_save_objects(values)