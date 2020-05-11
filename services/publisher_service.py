from core.services.service import Service

class PublisherService(Service):

    def get(self, id):
        return self.db.publishers.get(id)