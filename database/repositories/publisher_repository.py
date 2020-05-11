from core.database.repository import Repository
from database.models.publisher import Publisher

class PublisherRepository(Repository):

    def all(self):
        return self.session.query(Publisher).all()

    def last(self):
        return self.session.query(Publisher).order_by(Publisher.id.desc()).first()

    def get(self, id):
        return self.session.query(Publisher).filter(Publisher.id == id).first()    