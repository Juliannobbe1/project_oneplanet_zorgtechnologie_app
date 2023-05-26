from flask_restx import Namespace
from models.domain_model import Application, Client, HealthcareProfessional, Organisation, Product, Recommendation, Review, Supplier, Relationship

class NamespaceFactory:
    def __init__(self, driver, api):
        self.driver = driver
        self.api = api
        self.models = {
            'aanbeveling': Recommendation(driver),
            'toepassing': Application(driver),
            'product': Product(driver),
            'client': Client(driver),
            'zorgprofessional': HealthcareProfessional(driver),
            'organisatie': Organisation(driver),
            'review': Review(driver),
            'leverancier': Supplier(driver),
            'relatie': Relationship(driver)
        }
        self.namespaces = {}
        self.object_names = {}

    def create_namespace(self, name, description=None, decorators=None):
        return Namespace(name, description=description, decorators=decorators)

    def initialize_factory(self):
        models = {}

        for name, model_instance in self.models.items():
            model = self.api.model(name, model_instance.model())
            models[name] = model
            self.namespaces[name] = self.create_namespace(name, description=f'{name.capitalize()} operations')
            self.object_names[name] = model_instance.__class__.__name__

        for name, namespace in self.namespaces.items():
            self.api.add_namespace(namespace)
            namespace.models = models  # Set models dictionary as namespace attribute

        return models, self.namespaces, self.object_names
