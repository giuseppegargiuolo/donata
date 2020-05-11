from datetime import datetime

from database.models.run import Run
from core.services.service import Service

class RunService(Service):

    def connect(self):
        self.run = Run()
        self.run.startedAt = datetime.now()

        self.run = self.db.runs.save(self.run)        
        self.db.commit()

    def close(self):
        self.run.finishedAt = datetime.now()
        
        self.db.runs.save(self.run)
        self.db.commit()

    def getCurrent(self):
        return self.db.runs.getCurrent()