from flask import abort, jsonify
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
        super().__init__("zorgprofessional", driver=driver)
        self.model_data['zorgprofessionalNaam'] = fields.String(required=True)
        self.model_data['organisatieID'] = fields.Integer(required=True)
        self.model_data['email'] = fields.String(required=True)
        self.model_data['rol'] = fields.String(required=True)
        self.model_data['zorgprofessionalID'] = fields.Integer(required=True)
        
class Organisation(base_model):
    def __init__(self, driver):
        super().__init__("organisatie",driver=driver)
        self.model_data['organisatieID'] = fields.Integer(required=True)
        self.model_data['organisatieNaam'] = fields.String(required=True)
        
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
    
    def getNewestProducts(self):
        with self.driver.session() as session:
            result = session.run(f"MATCH (n:{self.label}) RETURN n ORDER BY n.productID DESC LIMIT 5")
            if result:
                data = self.extract(result)
                return data
            else:
                return abort(404, "Something went wrong")
        
        
class Recommendation(base_model):
    def __init__(self, driver):
        super().__init__("aanbeveling", driver=driver)
        self.model_data['aanbeveling'] = fields.String(required=True)
        self.model_data['productID'] = fields.Integer(required=True)
        self.model_data['aanbevelingID'] = fields.Integer(required=True)
        self.model_data['zorgprofessionalID'] = fields.Integer(required=True) 
        self.model_data['datum'] = fields.String()  
        
class Review(base_model):
    def __init__(self, driver):
        super().__init__("review", driver=driver)
        self.model_data['datum'] = fields.Date(required=True)
        self.model_data['score'] = fields.String(required=True)
        self.model_data['beschrijving'] = fields.String(required=True)
        self.model_data['productID'] = fields.String(required=True)
        self.model_data['reviewID'] = fields.String(required=True)
        self.model_data['zorgprofessionalID'] = fields.String(required=True)
        
class Supplier(base_model):
    def __init__(self, driver):
        super().__init__("leverancier", driver=driver)
        self.model_data['leverancierID'] = fields.Integer(required=True)
        self.model_data['leverancierNaam'] = fields.String(required=True)
        
class Relationship(base_model):
    def __init__(self, driver):
        super().__init__("relatie", driver)
        self.model_data['start_id'] = fields.Integer()
        self.model_data['end_id'] = fields.Integer()
        self.model_data['relationship_name'] = fields.String()
        
    def setRelationship( self, start_node, start_id, end_node, end_id, relationship_name):
        with self.driver.session() as session:
            result = session.run(f"MATCH (start:{start_node} {{{start_node}ID: $start_id }}), (end:{end_node} {{{end_node}ID: $end_id }}) CREATE (start)-[:{relationship_name}]->(end) RETURN start, end", start_id=start_id, start_node=start_node, end_id=end_id, end_node=end_node)
            if result:
                return jsonify({"message": "Relationship created successfully."})
            else:
                return jsonify({"message": "Could not create relationship"})
            
    def deleteRelationship(self, start_node, start_id, end_node, end_id, relationship_name):
        with self.driver.session() as session:
            # checkedValue = self.StringToIntCheck(value)
            result = session.run(f"MATCH (start:{start_node} {{{start_node}ID: $start_id }})-[r:{relationship_name}]->(end:{end_node} {{{end_node}ID: $end_id }}) DELETE r", start_id=start_id, start_node=start_node, end_id=end_id, end_node=end_node)
            if result:
                return jsonify({"message": "Resource deleted successfully."}) 
            else:
                return abort(404, "Could not delete")