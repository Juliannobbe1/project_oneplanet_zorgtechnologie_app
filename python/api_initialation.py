from flask_restx import Namespace
from models.domain_model import Application, Client, HealthcareProfessional, Organisation, Product, Recommendation, Review, Supplier

class NamespaceFactory:
    def __init__(self, driver, api):
        self.driver = driver
        self.api = api
        self.models = {
            'aanbeveling': Recommendation,
            'toepassing': Application,
            'product': Product,
            'client': Client,
            'zorgprofessional': HealthcareProfessional,
            'organisatie': Organisation,
            'review': Review,
            'leverancier': Supplier
        }
        self.namespaces = {}
        self.object_names = {}
        
    def create_model(self, model_cls):
        return model_cls(self.driver)

    def create_namespace(self, name, description=None, decorators=None):
        return Namespace(name, description=description, decorators=decorators)

    def initialize_factory(self):
        models = {}
        for name, model_cls in self.models.items():
            model_instance = self.create_model(model_cls)
            models[name] = self.api.model(name, model_instance.model())
            self.namespaces[name] = self.create_namespace(name, description=f'{name.capitalize()} operations')
            self.object_names[name] = model_cls.__name__

        for name, namespace in self.namespaces.items():
            self.api.add_namespace(namespace)
        #     namespace.models[name] = models[name]  # Register model with namespace

        return models, self.namespaces, self.object_names

    