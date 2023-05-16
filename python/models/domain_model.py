from flask_restx import fields

from models.base_model import base_model

class Application(base_model):
    def __init__(self,driver):
        super().__init__("toepassing", driver=driver)
        self.model_data['toepassing'] = fields.String(required=True)
        self.model_data['productID'] = fields.Integer(required=True)
        self.model_data['toepassingID'] = fields.Integer(required=True)
    
class Client(base_model):
    def __init__(self, driver):
        super().__init__("client", driver=driver)
        self.model_data['clientID'] = fields.Integer(required=True)
        self.model_data['probleem'] = fields.String(required=True)
        
class HealthcareProfessional(base_model):
    def __init__(self, driver):
        super().__init__("zorgprofesional", driver=driver)
        
class organisation_model(base_model):
    def __init__(self, driver):
        super().__init__("organisatie",driver=driver)
        
class Product(base_model):
    def __init__(self, driver):
        super().__init__("product", driver=driver)
        self.model_data['beschrijving'] = fields.String()
        self.model_data['categorie'] = fields.String()
        self.model_data['productID'] = fields.Integer()
        self.model_data['leverancierID'] = fields.Integer()
        self.model_data['link'] = fields.String()
        self.model_data['productNaam'] = fields.String(required=True, description='Naam van het product')
        self.model_data['prijs'] = fields.Float()
        
        
class Recommendation(base_model):
    def __init__(self, driver):
        super().__init__("aanbeveling", driver=driver)
        self.model_data['aanbeveling'] = fields.String(required=True)
        self.model_data['productID'] = fields.Integer(required=True)
        self.model_data['aanbevelingID'] = fields.Integer(required=True)
        self.model_data['zorgprofessionalID'] = fields.Integer(required=True) 
        self.model_data['datum'] = fields.String()  
        
class review_model(base_model):
    def __init__(self, driver):
        super().__init__("review", driver=driver)
        
class supplier_model(base_model):
    def __init__(self, driver):
        super().__init__("leverancier", driver=driver)