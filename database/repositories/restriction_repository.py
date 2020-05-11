from core.database.repository import Repository
from database.models.restriction import Restriction

class RestrictionRepository(Repository):

    def last(self):
        return self.session.query(Restriction).order_by(Restriction.id.desc()).first()

    def get(self, id):
        return self.query(Restriction).filter(Restriction.id == id).first()