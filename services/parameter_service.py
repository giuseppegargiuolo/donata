from core.services.service import Service

class ParameterService(Service):

    def get(self, name, default=None):
        parameter = self.db.parameters.get(name)
        if parameter.value is None:
            return default
        else:
            return parameter.value