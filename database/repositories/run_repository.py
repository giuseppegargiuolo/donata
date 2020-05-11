from core.database.repository import Repository
from database.models.run import Run

class RunRepository(Repository):

    def last(self):
        return self.session.query(Run).order_by(Run.id.desc()).first()

    def getCurrent(self):
        return self.session.query(Run).filter(Run.finishedAt == None).order_by(Run.startedAt.desc()).first()