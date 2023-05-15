from flask_restx import fields

from models.base_model import base_model

class application_model(base_model):
    def __init__(self,driver):
        super().__init__("toepassing", driver=driver)

class client_model(base_model):
    def __init__(self, driver):
        super().__init__("client", driver=driver)
        
class healthcare_professional_model(base_model):
    def __init__(self, driver):
        super().__init__("zorgprofesional", driver=driver)
        
class organisation_model(base_model):
    def __init__(self, driver):
        super().__init__("organisatie",driver=driver)
        
class Product(base_model):
    def __init__(self, driver):
        super().__init__("product", driver=driver)
    
    def Model(self):
        ProductModel = {'beschrijving': fields.String(),
         'categorie': fields.String(),
         'productID': fields.Integer(),
         'leverancierID': fields.Integer(),
         'link': fields.String(),
         'productNaam': fields.String(required=True, description='Naam van het product'),
         'prijs': fields.Float()}
        return ProductModel
        
        
class recommendation_model(base_model):
    def __init__(self, driver):
        super().__init__("aanbeveling", driver=driver)        
        
class review_model(base_model):
    def __init__(self, driver):
        super().__init__("review", driver=driver)
        
class supplier_model(base_model):
    def __init__(self, driver):
        super().__init__("leverancier", driver=driver)