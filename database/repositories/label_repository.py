from core.database.repository import Repository
from database.models.label import Label

from sqlalchemy import func

class LabelRepository(Repository):

    def all(self):
        return self.session.query(Label).all()

    def get(self, name):
        return self.session.query(Label).filter(func.upper(Label.name) == name.upper()).first()