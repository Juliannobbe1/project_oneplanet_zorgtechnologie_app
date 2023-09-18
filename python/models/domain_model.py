import json
from flask import abort
from flask_restx import fields
from models.base_model import base_model

class Application(base_model):
    def __init__(self, driver):
        super().__init__("toepassing", driver=driver)
        self.model_data['toepassing'] = fields.String(required=True)
        self.model_data['productID'] = fields.String(required=True)
        self.model_data['ID'] = fields.String(required=True)
        
    def getApplicationWithProduct(self):
        # Query to retrieve applications with associated products
        query = f"MATCH ({self.label}:{self.label})<-[ht:HEEFT_TOEPASSING]-(product) RETURN {self.label}.{self.label}, product.naam, product.beschrijving, {self.label}.productID, {self.label}.ID"
        with self.driver.session() as session:
            result = session.run(query)
            if result:
                extracted_data = [{'toepassing': item['toepassing.toepassing'], 'productnaam': item['product.naam'], 'beschrijving': item['product.beschrijving'], 'productID': item['toepassing.productID'], 'ID': item['toepassing.ID']} for item in result.data()]
                return extracted_data
            else:
                return abort(404, "Something went wrong")
    
    def getDistinctApplications(self):
        # Query to retrieve distinct applications
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
        # Query to retrieve distinct client problems
        query = f"MATCH(n:client) WITH n.probleem as n RETURN DISTINCT n"
        with self.driver.session() as session:
            result = session.run(query)
            if result:
                data = self.extract(result)
                return data
            else:
                return abort(404, "Something went wrong")
    
    def getClientsOfHCProf(self, zorgprofID):
        # Query to retrieve clients of a specific healthcare professional
        query = f"MATCH (zorgprofessional:zorgprofessional)-[:VERZORGD_CLIENT]->(cliënt:client) WHERE zorgprofessional.ID = '{zorgprofID}' RETURN cliënt as n"
        with self.driver.session() as session:
            result = session.run(query)
            if result:
                data = self.extract(result)
                return data
            else:
                return abort(404, "Something went wrong")
            
    def setClientHealthcareProfRelationship(self, clientID, zorgprofID):
        # Query to create a relationship between a client and a healthcare professional
        query = f"MATCH (c:client) WHERE c.ID = '{clientID}' MATCH (z:zorgprofessional) WHERE z.ID = '{zorgprofID}' CREATE (c)<-[:VERZORGD_CLIENT]-(z)"
        with self.driver.session() as session:
            result = session.run(query)
            if result:
                return "Relationship created successfully"
            else:
                return abort(404, "Something went wrong")

class HealthcareProfessional(base_model):
    def __init__(self, driver):
        super().__init__("zorgprofessional", driver=driver)
        self.model_data['ID'] = fields.String(required=True)
        self.model_data['naam'] = fields.String(required=True)
        
    def getHealthcareProfessionalByID(self, zorgprofID):
        # Query to retrieve a healthcare professional by ID
        query = f"MATCH (zorgprofessional:zorgprofessional) WHERE zorgprofessional.ID = '{zorgprofID}' RETURN zorgprofessional"
        with self.driver.session() as session:
            result = session.run(query)
            if result:
                data = self.extract(result)
                return data
            else:
                return abort(404, "Something went wrong")
            
    def getDistinctHealthcareProfessionals(self):
        # Query to retrieve distinct healthcare professionals
        query = "MATCH(n:zorgprofessional) RETURN n"
        with self.driver.session() as session:
            result = session.run(query)
            if result:
                data = self.extract(result)
                return data
            else:
                return abort(404, "Something went wrong")

class Organisation(base_model):
    def __init__(self, driver):
        super().__init__("organisatie", driver=driver)
        self.model_data['ID'] = fields.String(required=True)
        self.model_data['naam'] = fields.String(required=True)
        
    def getDistinctOrganisations(self):
        # Query to retrieve distinct organizations
        query = "MATCH(n:organisatie) RETURN n"
        with self.driver.session() as session:
            result = session.run(query)
            if result:
                data = self.extract(result)
                return data
            else:
                return abort(404, "Something went wrong")

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
        
    def getDistinctProducts(self):
        # Query to retrieve distinct products
        query = "MATCH(n:product) RETURN n"
        with self.driver.session() as session:
            result = session.run(query)
            if result:
                data = self.extract(result)
                return data
            else:
                return abort(404, "Something went wrong")
        
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

    def setRecommendation(self, productID, recommendationID):
        # Query to create a recommendation relationship between a product and a recommendation
        query = f"MATCH (p:product) WHERE p.ID = '{productID}' MATCH (r:aanbeveling) WHERE r.ID = '{recommendationID}' CREATE (p)-[:AANBEVELEN]->(r)"
        with self.driver.session() as session:
            result = session.run(query)
            if result:
                return "Relationship created successfully"
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
            
    
