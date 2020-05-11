from core.services.service import Service

class LabelService(Service):

    def all(self):
        return self.db.labels.all()