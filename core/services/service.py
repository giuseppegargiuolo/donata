import os
from core.log import Log
from core.config import Config
from database.database import ApartmentsDatabase

from core.utils import Utils

class Service:
    def __init__(self, database=None):
        self.utils = Utils()
        self.config = Config()
        self.log = Log.getInstance()
        
        if database is None:
            self.db = ApartmentsDatabase()
        else:
            self.db = database