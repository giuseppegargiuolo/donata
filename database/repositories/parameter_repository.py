from core.database.repository import Repository
from database.models.parameter import Parameter

class ParameterRepository(Repository):

    def get(self, name):
        return self.session.query(Parameter).filter(Parameter.name == name).first()