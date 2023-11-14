from flask import abort
from flask_restx import fields
from models.base_model import base_model
from loguru import logger

class Application(base_model):
    def __init__(self, driver):
        super().__init__("toepassing", driver=driver)
        self.model_data['toepassing'] = fields.String(required=True)
        self.model_data['productID'] = fields.String(required=True)
        self.model_data['ID'] = fields.String(required=True)
        
    def getApplicationWithProduct(self):
        logger.trace("Attempting to retrieve applications with associated products")
        # Query to retrieve applications with associated products
        query = f"MATCH ({self.label}:{self.label})<-[ht:HEEFT_TOEPASSING]-(product) RETURN {self.label}.{self.label}, product.naam, product.beschrijving, {self.label}.productID, {self.label}.ID"
        with self.driver.session() as session:
            result = session.run(query)
            if result:
                extracted_data = [{'toepassing': item['toepassing.toepassing'], 'productnaam': item['product.naam'], 'beschrijving': item['product.beschrijving'], 'productID': item['toepassing.productID'], 'ID': item['toepassing.ID']} for item in result.data()]
                logger.trace("Successfully retrieved applications with associated products: '{extracted_data}'", extracted_data=extracted_data)
                return extracted_data
            else:
                logger.error("Can't retrieve applications with associated products")
                return abort(404, "Something went wrong")
    
    def getDistinctApplications(self):
        logger.trace("Attempting to retrieve all distinct applications")
        # Query to retrieve distinct applications
        query = f"MATCH (p:toepassing)<-[t:HEEFT_TOEPASSING]-() WITH p.toepassing as n, COUNT(t) AS count RETURN n ORDER BY count DESC"
        with self.driver.session() as session:
            result = session.run(query)
            if result:
                data = self.extract(result)
                logger.trace("Successfully retrieved distinct applications: '{distinct_applications}'", distinct_applications=data)
                return data
            else:
                logger.error("Failed to retrieve all distinct applications")
                return abort(404, "Something went wrong")

class Client(base_model):
    def __init__(self, driver):
        super().__init__("client", driver=driver)
        self.model_data['ID'] = fields.String(required=False)
        self.model_data['probleem'] = fields.String(required=True)
        
    def getDistinctProblems(self):
        logger.trace("Attempting to retrieve distinct client problems")
        # Query to retrieve distinct client problems
        query = f"MATCH(n:client) WITH n.probleem as n RETURN DISTINCT n"
        with self.driver.session() as session:
            result = session.run(query)
            if result:
                data = self.extract(result)
                logger.trace("Successfully retrieved distinct client problems '{distinct_client_problems}'", distinct_client_problems=data)
                return data
            else:
                logger.error("Failed to retrieve distinct client problems")
                return abort(404, "Something went wrong")
    
    def getClientsOfHCProf(self, zorgprofID):
        logger.trace("Attempting to retrieve clients for HealthcareProfessional '{healthcareProfessional}'", healthcareProfessional=zorgprofID)
        # Query to retrieve clients of a specific healthcare professional
        query = f"MATCH (zorgprofessional:zorgprofessional)-[:VERZORGD_CLIENT]->(cliënt:client) WHERE zorgprofessional.ID = '{zorgprofID}' RETURN cliënt as n"
        with self.driver.session() as session:
            result = session.run(query)
            if result:
                data = self.extract(result)
                logger.trace("Successfully retrieved clients for HealthcareProfessional '{healthcareProfessional}': '{clients}'", healthcareProfessional=zorgprofID, clients=data)
                return data
            else:
                logger.error("Failed to retireve clients for HealthcareProfessional '{healthcareProfessional}'", healthcareProfessional=zorgprofID)
                return abort(404, "Something went wrong")
            
    def setClientHealthcareProfRelationship(self, clientID, zorgprofID):
        logger.trace("Attempting to create relationship for client '{client}' and HealthcareProfessional '{healthcareProfessional}'", client=clientID, healthcareProfessional=zorgprofID)
        # Query to create a relationship between a client and a healthcare professional
        query = f"MATCH (c:client) WHERE c.ID = '{clientID}' MATCH (z:zorgprofessional) WHERE z.ID = '{zorgprofID}' CREATE (c)<-[:VERZORGD_CLIENT]-(z)"
        with self.driver.session() as session:
            result = session.run(query)
            if result:
                logger.trace("Successfully created relationship for client '{client}' and HealthcareProfessional '{healthcareProfessional}'", client=clientID, healthcareProfessional=zorgprofID)
                return "Relationship created successfully"
            else:
                logger.error("Failed to create relationship for client '{client}' and HealthcareProfessional '{healthcareProfessional}'", client=clientID, healthcareProfessional=zorgprofID)
                return abort(404, "Something went wrong")

class HealthcareProfessional(base_model):
    def __init__(self, driver):
        super().__init__("zorgprofessional", driver=driver)
        self.model_data['ID'] = fields.String(required=True)
        self.model_data['naam'] = fields.String(required=True)
        
    def getHealthcareProfessionalByID(self, zorgprofID):
        logger.trace("Attempting to retrieve HealthcareProfessional '{healthcareProfessional}'", healthcareProfessional=zorgprofID)
        # Query to retrieve a healthcare professional by ID
        query = f"MATCH (zorgprofessional:zorgprofessional) WHERE zorgprofessional.ID = '{zorgprofID}' RETURN zorgprofessional"
        with self.driver.session() as session:
            result = session.run(query)
            if result:
                data = self.extract(result)
                logger.trace("Successfully retrieved HealthcareProfessional '{healthcareProfessional}': '{result}'", healthcareProfessional=zorgprofID, result=data)
                return data
            else:
                logger.error("Failed to retrieve HealthcareProfessional '{healthcareProfessional}'", healthcareProfessional=zorgprofID)
                return abort(404, "Something went wrong")
            
    def getDistinctHealthcareProfessionals(self):
        logger.trace("Attempting to retrieve all distinct HealthcareProfessionals")
        # Query to retrieve distinct healthcare professionals
        query = "MATCH(n:zorgprofessional) RETURN n"
        with self.driver.session() as session:
            result = session.run(query)
            if result:
                data = self.extract(result)
                logger.trace("Successfully retrieved all distinct HealthcareProfessionals: '{result}'", result=data)
                return data
            else:
                logger.error("Failed to retrieve all distinct HealthcareProfessionals")
                return abort(404, "Something went wrong")

class Organisation(base_model):
    def __init__(self, driver):
        super().__init__("organisatie", driver=driver)
        self.model_data['ID'] = fields.String(required=True)
        self.model_data['naam'] = fields.String(required=True)
        
    def getDistinctOrganisations(self):
        logger.trace("Attempting to retrieve all distinct organizations")
        # Query to retrieve distinct organizations
        query = "MATCH(n:organisatie) RETURN n"
        with self.driver.session() as session:
            result = session.run(query)
            if result:
                data = self.extract(result)
                logger.trace("Successfully retrieved all distinct organizations: '{distinct_organizations}'", distinct_organizations=data)
                return data
            else:
                logger.error("Failed to retrieve all distinct organizations")
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
        logger.trace("Attempting to retrieve the newest products")
        with self.driver.session() as session:
            result = session.run(f"MATCH (n:product)RETURN n ORDER BY id(n) DESC LIMIT 6")
            if result:
                data = self.extract(result)
                logger.trace("Successfully retrieved the newest products: '{newest_products}'", newest_products=data)
                return data
            else:
                logger.error("Failed to retrieve the newest products")
                return abort(404, "Something went wrong")
    
    def getRecommendationProducts(self, zorgprofID, probleem ):
        logger.trace("Attempting to retrieve the recommendation products for HealthcareProfessional '{healthcare_professional}' and problem '{problem}'", healthcare_professional=zorgprofID, problem=probleem)
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
                logger.trace("Successfully retrieved the recommendation products '{recommendation_products}'", recommendation_products=data)
                return data
            else:
                logger.error("Failed to retrieve the recommendation products for HealthcareProfessional '{healthcare_professional}' and problem '{problem}'", healthcare_professional=zorgprofID, problem=probleem)
                return abort(404, "Something went wrong")
            
    def getProductsOneClient(self, clientID):
        logger.trace("Attempting to retrieve products for client '{client}'", client=clientID)
        query = f"MATCH (n:product)<-[k:KRIJGT_AANBEVELING]-(a:zorgprofessional)-[z:VERZORGD_CLIENT]->(c:client) WHERE c.ID = '{clientID}' AND k.clientID = '{clientID}' RETURN DISTINCT n"
        with self.driver.session() as session:
            result = session.run(query)
            if result:
                data = self.extract(result)
                logger.trace("Successfully retrieved products for client '{client}': '{products}'", client=clientID, products=data)
                return data
            else:
                logger.error("Failed to retrieve products for client '{client}'", client=clientID)
                return abort(404, "Something went wrong")

            
    def setRecommendedRelationship(self, zorgprofID, productID):
        logger.trace("Attempting to create recommended relationship for HealthcareProfessional '{healthcare_professional}' and product '{product}'", healthcare_professional=zorgprofID, product=productID)
        query = f"MATCH (z:zorgprofessional) WHERE z.ID = '{zorgprofID}' MATCH (p:product) WHERE p.ID = '{productID}' CREATE (p)<-[:KRIJGT_AANBEVELING]-(z)"
        with self.driver.session() as session:
            result = session.run(query)
            if result:
                logger.trace("Successfully created recommended relationship for HealthcareProfessional '{healthcare_professional}' and product '{product}'", healthcare_professional=zorgprofID, product=productID)
                return "Relationship created successfully"
            else:
                logger.error("Failed to create recommended relationship for HealthcareProfessional '{healthcare_professional}' and product '{product}'", healthcare_professional=zorgprofID, product=productID)
                return abort(404, "Something went wrong")
        
    def getDistinctProducts(self):
        logger.trace("Attempting to retrieve all distinct products")
        # Query to retrieve distinct products
        query = "MATCH(n:product) RETURN n"
        with self.driver.session() as session:
            result = session.run(query)
            if result:
                data = self.extract(result)
                logger.trace("Successfully retrieved all distinct products: '{distinct_products}'", distinct_products=data)
                return data
            else:
                logger.error("Failed to retrieve all distinct products")
                return abort(404, "Something went wrong")
        
    def getRecommendationsByProduct(self, productID):
        logger.trace("Attempting to retrieve recommendations for product '{product}'", product=productID)
        # Query to retrieve recommendations by product ID
        query = f"MATCH (p:product)-[:AANBEVELEN]-(r:aanbeveling) WHERE p.ID = '{productID}' RETURN r"
        with self.driver.session() as session:
            result = session.run(query)
            if result:
                data = self.extract(result)
                logger.trace("Successfully retrieved recommendations for product '{product}': '{recommendations}'", product=productID, recommendations=data)
                return data
            else:
                logger.error("Failed to retrieve recommendations for product '{product}'", product=productID)
                return abort(404, "Something went wrong")

    def setRecommendation(self, productID, recommendationID):
        logger.trace("Attempting to create recommendation relationship between product '{product}' and recommendation '{recommendation}'", product=productID, recommendation=recommendationID)
        # Query to create a recommendation relationship between a product and a recommendation
        query = f"MATCH (p:product) WHERE p.ID = '{productID}' MATCH (r:aanbeveling) WHERE r.ID = '{recommendationID}' CREATE (p)-[:AANBEVELEN]->(r)"
        with self.driver.session() as session:
            result = session.run(query)
            if result:
                logger.trace("Successfully created recommendation relationship between product '{product}' and recommendation '{recommendation}'", product=productID, recommendation=recommendationID)
                return "Relationship created successfully"
            else:
                logger.error("Failed to create recommendation relationship between product '{product}' and recommendation '{recommendation}'", product=productID, recommendation=recommendationID)
                return abort(404, "Could not delete")
            
class Recommendation(base_model):
    def __init__(self, driver):
        super().__init__("aanbeveling", driver=driver)
        self.model_data['ID'] = fields.String(required=True)
        self.model_data['aanbeveling'] = fields.String(required=True)
        
    def getRecommendationsByProduct(self, productID):
        logger.trace("Attempting to retrieve recommendations for product '{product}'", product=productID)
        # Query to retrieve recommendations by product ID
        query = f"MATCH (p:product)-[:AANBEVELEN]-(r:aanbeveling) WHERE p.ID = '{productID}' RETURN r"
        with self.driver.session() as session:
            result = session.run(query)
            if result:
                data = self.extract(result)
                logger.trace("Successfully retrieved recommendations for product '{product}': '{recommendations}'", product=productID, recommendations=data)
                return data
            else:
                logger.error("Failed to retrieve recommendations for product '{product}'", product=productID)
                return abort(404, "Something went wrong")

    def setRecommendation(self, zorgprofessionalID, productID,clientID):
        logger.trace("Attempting to create recommendation relationship for HealthcareProfessional '{healthcare_professional}', product '{product}' and client '{client}'", healthcare_professional=zorgprofessionalID, product=productID, client=clientID)
        # Query to create a recommendation relationship between a product and a recommendation
        query = f"MATCH (p:product) WHERE p.ID = '{productID}' MATCH (z:zorgprofessional) WHERE z.ID = '{zorgprofessionalID}' CREATE (p)<-[:KRIJGT_AANBEVELING {{aanbevelingsID: randomUUID(), zorgprofessionalID: '{zorgprofessionalID}', productID: '{productID}', clientID: '{clientID}'}}]-(z)"
        with self.driver.session() as session:
            result = session.run(query)
            if result:
                logger.trace("Successfully created recommendation relationship for HealthcareProfessional '{healthcare_professional}', product '{product}' and client '{client}'", healthcare_professional=zorgprofessionalID, product=productID, client=clientID)
                return "Relationship created successfully"
            else:
                logger.error("Failed to create recommendation relationship for HealthcareProfessional '{healthcare_professional}', product '{product}' and client '{client}'", healthcare_professional=zorgprofessionalID, product=productID, client=clientID)
                return abort(404, "Something went wrong")
            
    
