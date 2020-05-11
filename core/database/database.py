import pymysql
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker

from core.config import Config

from core.database.base import Base

class Database:
    def __init__(self):
        database = Config().get('database')
        self.engine = create_engine('mysql+pymysql://' + database['username'] + ':' + database['password'] + '@' + database['host'] + ':' + database['port'] + '/' + database['name'], pool_size=0)

        Session = sessionmaker(bind=self.engine, expire_on_commit=False)
        self.session = Session()
        self.session.expunge_all()

    def connect(self):
        self.connection = self.engine.connect()

    def disconnect(self):
        self.connection.close()
        self.session.bind.dispose()
        self.engine.dispose()

    def commit(self):
        try:
            self.session.commit()
        except Exception as e:
            print(str(e))
            self.session.rollback()

    def rollback(self):
        self.session.rollback()

    def migrate(self):
        Base.metadata.create_all(bind=self.engine)