import json
from flask import abort, jsonify, send_file
from flask_restx import fields
from models.base_model import base_model

class Application(base_model):
    def __init__(self,driver):
        super().__init__("toepassing", driver=driver)
        self.model_data['toepassing'] = fields.String(required=True)
        self.model_data['productID'] = fields.String(required=True)
        self.model_data['ID'] = fields.String(required=True)
        
    def getApplicationWithProduct(self):
        query = f"MATCH ({self.label}:{self.label})<-[ht:HEEFT_TOEPASSING]-(product) RETURN {self.label}.{self.label}, product.naam, product.beschrijving, {self.label}.productID, {self.label}.ID "
        with self.driver.session() as session:
            result = session.run(query)
            if result: 
                extracted_data = [{'toepassing': item['toepassing.toepassing'], 'productnaam': item['product.naam'], 'beschrijving': item['product.beschrijving'], 'productID': item['toepassing.productID'], 'ID': item['toepassing.ID']} for item in result.data()]

                return extracted_data
            else: 
                return abort(404, "Something went wrong")
    
    def getDistinctApplications(self):
        query = f"MATCH (p:toepassing)<-[t:HEEFT_TOEPASSING]-() WITH p.toepassing as n, COUNT(t) AS count RETURN n ORDER BY count DESC"
        with self.driver.session() as session:
            result = session.run(query)
            if result: 
                data = self.extract(result)
                return data
            else: 
                return abort(404, "Something went wrong")
    
class Client(base_model):
    def __init__(self, driver):
        super().__init__("client", driver=driver)
        self.model_data['ID'] = fields.String(required=False)
        self.model_data['probleem'] = fields.String(required=True)
        
    def getDistinctProblems(self):
        query = f"MATCH(n:client) WITH n.probleem as n RETURN DISTINCT n"
        with self.driver.session() as session:
            result = session.run(query)
            if result:
                data = self.extract(result)
                return data
            else: 
                return abort(404, "Something went wrong")
    
    def getClientsOfHCProf(self, zorgprofID):
        query = f"MATCH (zorgprofessional:zorgprofessional)-[:VERZORGD_CLIENT]->(cliënt:client) WHERE zorgprofessional.ID = '{zorgprofID}' RETURN cliënt as n"
        with self.driver.session() as session:
            result = session.run(query)
            if result:
                data = self.extract(result)
                return data
            else: 
                return abort(404, "Something went wrong")
            
    def setClientHealthcareProfRelationship(self, clientID, zorgprofID):
        query = f"MATCH (c:client) WHERE c.ID = '{clientID}' MATCH (z:zorgprofessional) WHERE z.ID = '{zorgprofID}' CREATE (c)<-[:VERZORGD_CLIENT]-(z)"
        with self.driver.session() as session:
            result = session.run(query)
            if result:
                return json.dumps({"message": "Relationship created successfully."})
            else: 
                return abort(404, "Something went wrong")
            
    def getLatestClient(self):
        with self.driver.session() as session:
            result = session.run(f"MATCH (n:{self.label}) RETURN n ORDER BY n.ID DESC LIMIT 1")
            if result:
                data = self.extract(result)
                return data
            else:
                return abort(404, "Something went wrong")
    
        
class HealthcareProfessional(base_model):
    def __init__(self, driver):
        super().__init__("zorgprofessional", driver=driver)
        self.model_data['naam'] = fields.String(required=True)
        self.model_data['organisatieID'] = fields.String(required=True)
        self.model_data['email'] = fields.String(required=True)
        self.model_data['rol'] = fields.String(required=True)
        self.model_data['ID'] = fields.String(required=True)
        
class Organisation(base_model):
    def __init__(self, driver):
        super().__init__("organisatie",driver=driver)
        self.model_data['ID'] = fields.String(required=True)
        self.model_data['naam'] = fields.String(required=True)
        
class Product(base_model):
    def __init__(self, driver):
        super().__init__("product", driver=driver)
        self.model_data['beschrijving'] = fields.String()
        self.model_data['ID'] = fields.String()
        self.model_data['leverancierID'] = fields.String()
        self.model_data['link'] = fields.String()
        self.model_data['naam'] = fields.String(required=True, description='Naam van het product')
        self.model_data['prijs'] = fields.Float()
        self.model_data['imageBase64'] = fields.String()
    
    def getNewestProducts(self):
        with self.driver.session() as session:
            result = session.run(f"MATCH (n:product)RETURN n ORDER BY id(n) DESC LIMIT 6")
            if result:
                data = self.extract(result)
                return data
            else:
                return abort(404, "Something went wrong")
    
    def getRecommendationProducts(self, zorgprofID, probleem ):
        query = f"""
        MATCH (zorgprofessional:zorgprofessional)
        WHERE zorgprofessional.ID = '{zorgprofID}'
        WITH zorgprofessional
        MATCH (andereZorgprofessional:zorgprofessional)-[:VERZORGD_CLIENT]->(andereCliënt:client)
        WHERE andereCliënt.probleem = '{probleem}'
        WITH zorgprofessional, andereCliënt
        MATCH (andereCliënt)<-[VERZORGD_CLIENT]-(andereZorgprofessional)-[K:KRIJGT_AANBEVELING]->(product:product)
        WHERE NOT (zorgprofessional)-[:KRIJGT_AANBEVELING]->(product) AND K.clientID = andereCliënt.ID
        WITH product AS n
        RETURN DISTINCT n
        """
        with self.driver.session() as session:
            result = session.run(query)
            if result:
                data = self.extract(result)
                return data
            else:
                return abort(404, "Something went wrong")
            
    def getProductsOneClient(self, clientID):
        query = f"MATCH (n:product)<-[k:KRIJGT_AANBEVELING]-(a:zorgprofessional)-[z:VERZORGD_CLIENT]->(c:client) WHERE c.ID = '{clientID}' AND k.clientID = '{clientID}' RETURN DISTINCT n"
        with self.driver.session() as session:
            result = session.run(query)
            if result:
                data = self.extract(result)
                return data
            else:
                return abort(404, "Something went wrong")
            
    def setRecommendedRelationship(self, zorgprofID, productID):
        query = f"MATCH (z:zorgprofessional) WHERE z.ID = '{zorgprofID}' MATCH (p:product) WHERE p.ID = '{productID}' CREATE (p)<-[:KRIJGT_AANBEVELING]-(z)"
        
        with self.driver.session() as session:
            result = session.run(query)
            if result:
                data = self.extract(result)
                return data
            else:
                return abort(404, "Something went wrong")
        
class Review(base_model):
    def __init__(self, driver):
        super().__init__("review", driver=driver)
        self.model_data['datum'] = fields.Date(required=True)
        self.model_data['score'] = fields.String(required=True)
        self.model_data['beschrijving'] = fields.String(required=True)
        self.model_data['productID'] = fields.String(required=True)
        self.model_data['ID'] = fields.String(required=True)
        self.model_data['zorgprofessionalID'] = fields.String(required=True)
        
class Supplier(base_model):
    def __init__(self, driver):
        super().__init__("leverancier", driver=driver)
        self.model_data['ID'] = fields.String(required=True)
        self.model_data['naam'] = fields.String(required=True)
        
class Relationship(base_model):
    def __init__(self, driver):
        super().__init__("relatie", driver)
        self.model_data['start_id'] = fields.String()
        self.model_data['end_id'] = fields.String()
        self.model_data['relationship_name'] = fields.String()
        
    def setRelationship( self, start_node, start_id, end_node, end_id, relationship_name):
        with self.driver.session() as session:
            result = session.run(f"MATCH (start:{start_node} {{{start_node}ID: $start_id }}), (end:{end_node} {{{end_node}ID: $end_id }}) CREATE (start)-[:{relationship_name}]->(end) RETURN start, end", start_id=str(start_id), start_node=start_node, end_id=str(end_id), end_node=end_node)
            if result:
                return jsonify({"message": "Relationship created successfully."})
            else:
                return jsonify({"message": "Could not create relationship"})
            
    def deleteRelationship(self, start_node, start_id, end_node, end_id, relationship_name):
        with self.driver.session() as session:
            # checkedValue = self.StringToIntCheck(value)
            result = session.run(f"MATCH (start:{start_node} {{{start_node}ID: $start_id }})-[r:{relationship_name}]->(end:{end_node} {{{end_node}ID: $end_id }}) DELETE r", start_id=str(start_id), start_node=start_node, end_id=str(end_id), end_node=end_node)
            if result:
                return jsonify({"message": "Resource deleted successfully."}) 
            else:
                return abort(404, "Could not delete")
            
class Recommendation(base_model):
    def __init__(self, driver):
        super().__init__("aanbeveling", driver=driver)
        self.model_data['ID'] = fields.String(required=True)
        self.model_data['aanbeveling'] = fields.String(required=True)
        
    def getRecommendationsByProduct(self, productID):
        # Query to retrieve recommendations by product ID
        query = f"MATCH (p:product)-[:AANBEVELEN]-(r:aanbeveling) WHERE p.ID = '{productID}' RETURN r"
        with self.driver.session() as session:
            result = session.run(query)
            if result:
                data = self.extract(result)
                return data
            else:
                return abort(404, "Something went wrong")

    def setRecommendation(self, zorgprofessionalID, productID,clientID):
        # Query to create a recommendation relationship between a product and a recommendation
        query = f"MATCH (p:product) WHERE p.ID = '{productID}' MATCH (z:zorgprofessional) WHERE z.ID = '{zorgprofessionalID}' CREATE (p)<-[:KRIJGT_AANBEVELING {{aanbevelingsID: randomUUID(), zorgprofessionalID: '{zorgprofessionalID}', productID: '{productID}', clientID: '{clientID}'}}]-(z)"
        with self.driver.session() as session:
            result = session.run(query)
            if result:
                return "Relationship created successfully"
            else:
                return abort(404, "Something went wrong")
            
    