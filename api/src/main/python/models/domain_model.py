from flask import abort, jsonify
from flask_restx import fields
from models.base_model import base_model
from loguru import logger

class ApplicationModel(base_model):
    def __init__(self, driver):
        super().__init__("toepassing", driver=driver)
        self.model_data['toepassing'] = fields.String(required=True)
        self.model_data['productID'] = fields.String(required=True)
        self.model_data['ID'] = fields.String(required=True)

    @staticmethod
    def get_str_of_dict(application_dict: dict) -> str:
        return f"Application(Toepassing: '{application_dict['toepassing'] if 'toepassing' in application_dict else None}', ProductID: '{application_dict['productID'] if 'productID' in application_dict else None}', ID: '{application_dict['ID'] if 'ID' in application_dict else None}')"
        
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

class ClientModel(base_model):
    def __init__(self, driver):
        super().__init__("client", driver=driver)
        self.model_data['ID'] = fields.String(required=False)
        self.model_data['probleem'] = fields.String(required=True)

    @staticmethod
    def get_str_of_dict(client_dict: dict) -> str:
        return f"Client(ID: '{client_dict['ID'] if 'ID' in client_dict else None}', Probleem: '{client_dict['probleem'] if 'probleem' in client_dict else None}')"
        
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

class HealthcareProfessionalModel(base_model):
    def __init__(self, driver):
        super().__init__("zorgprofessional", driver=driver)
        self.model_data['ID'] = fields.String(required=True)
        self.model_data['naam'] = fields.String(required=True)

    @staticmethod
    def get_str_of_dict(healthcareprofessional_dict: dict) -> str:
        return f"HealthcareProfessional(ID: '{healthcareprofessional_dict['ID'] if 'ID' in healthcareprofessional_dict else None}', Naam: '{healthcareprofessional_dict['naam'] if 'naam' in healthcareprofessional_dict else None}')"
        
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

class OrganisationModel(base_model):
    def __init__(self, driver):
        super().__init__("organisatie", driver=driver)
        self.model_data['ID'] = fields.String(required=True)
        self.model_data['naam'] = fields.String(required=True)

    @staticmethod
    def get_str_of_dict(organisation_dict: dict) -> str:
        return f"Organisation(ID: '{organisation_dict['ID'] if 'ID' in organisation_dict else None}', Naam: '{organisation_dict['naam'] if 'naam' in organisation_dict else None}')"
        
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

class ProductModel(base_model):
    def __init__(self, driver):
        super().__init__("product", driver=driver)
        self.model_data['beschrijving'] = fields.String()
        self.model_data['ID'] = fields.String()
        self.model_data['leverancierID'] = fields.String()
        self.model_data['link'] = fields.String()
        self.model_data['naam'] = fields.String(required=True, description='Naam van het product')
        self.model_data['prijs'] = fields.Float()
        self.model_data['imageBase64'] = fields.String()

    @staticmethod
    def get_str_of_dict(product_dict: dict) -> str:
        return f"Product(ID: '{product_dict['ID'] if 'ID' in product_dict else None}', Naam: '{product_dict['naam'] if 'naam' in product_dict else None}', Prijs: '{product_dict['prijs'] if 'prijs' in product_dict else None}', Beschrijving: '{product_dict['beschrijving'] if 'beschrijving' in product_dict else None}', LeverancierID: '{product_dict['leverancierID'] if 'leverancierID' in product_dict else None}', Link: '{product_dict['link'] if 'link' in product_dict else None}', ImageBase64: '{product_dict['imageBase64'][:5] if 'imageBase64' in product_dict else None}')"
    
    def getNewestProducts(self):
        logger.trace("Attempting to retrieve the newest products")
        with self.driver.session() as session:
            result = session.run(f"MATCH (n:product)RETURN n ORDER BY id(n) DESC LIMIT 6")
            if result:
                data = self.extract(result)
                logger_data = [ProductModel.get_str_of_dict(p) for p in data]
                logger.trace("Successfully retrieved the newest products: '{newest_products}'", newest_products=logger_data)
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
        WITH product AS n
        RETURN DISTINCT n
        """
        # This part of the algorithm is being excluded due to new data not having enough relations
        # WHERE NOT (zorgprofessional)-[:KRIJGT_AANBEVELING]->(product) AND K.clientID = andereCliënt.ID
        
        
        with self.driver.session() as session:
            result = session.run(query)
            if result:
                data = self.extract(result)
                logger_data = [ProductModel.get_str_of_dict(p) for p in data]
                logger.trace("Successfully retrieved the recommendation products '{recommendation_products}'", recommendation_products=logger_data)
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
                logger_data = [ProductModel.get_str_of_dict(p) for p in data]
                logger.trace("Successfully retrieved products for client '{client}': '{products}'", client=clientID, products=logger_data)
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
            
class RecommendationModel(base_model):
    def __init__(self, driver):
        super().__init__("aanbeveling", driver=driver)
        self.model_data['ID'] = fields.String(required=True)
        self.model_data['aanbeveling'] = fields.String(required=True)

    @staticmethod
    def get_str_of_dict(recommendation_dict: dict) -> str:
        return f"Recommendation(ID: '{recommendation_dict['ID'] if 'ID' in recommendation_dict else None}', Aanbeveling: '{recommendation_dict['aanbeveling'] if 'aanbeveling' in recommendation_dict else None}')"
        
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
            
class ReviewModel(base_model):
    def __init__(self, driver):
        super().__init__("review", driver=driver)
        self.model_data['datum'] = fields.Date(required=True)
        self.model_data['score'] = fields.String(required=True)
        self.model_data['beschrijving'] = fields.String(required=True)
        self.model_data['productID'] = fields.String(required=True)
        self.model_data['ID'] = fields.String(required=True)
        self.model_data['zorgprofessionalID'] = fields.String(required=True)

    @staticmethod
    def get_str_of_dict(review_dict: dict) -> str:
            return f"Review(ID: '{review_dict['ID'] if 'ID' in review_dict else None}', Datum: '{review_dict['datum'] if 'datum' in review_dict else None}', Score: '{review_dict['score'] if 'score' in review_dict else None}', Beschrijving: '{review_dict['beschrijving'] if 'beschrijving' in review_dict else None}', ProductID: '{review_dict['productID'] if 'productID' in review_dict else None}', ZorgprofessionalID: '{review_dict['zorgprofessionalID'] if 'zorgprofessionalID' in review_dict else None}')"
        
class SupplierModel(base_model):
    def __init__(self, driver):
        super().__init__("leverancier", driver=driver)
        self.model_data['ID'] = fields.String(required=True)
        self.model_data['naam'] = fields.String(required=True)

    @staticmethod
    def get_str_of_dict(supplier_dict: dict) -> str:
        return f"Supplier(ID: '{supplier_dict['ID'] if 'ID' in supplier_dict else None}', Naam: '{supplier_dict['naam'] if 'naam' in supplier_dict else None}')"
        
class RelationshipModel(base_model):
    def __init__(self, driver):
        super().__init__("relatie", driver)
        self.model_data['start_id'] = fields.String()
        self.model_data['end_id'] = fields.String()
        self.model_data['relationship_name'] = fields.String()

    @staticmethod
    def get_str_of_dict(relationship_dict: dict) -> str:
        return f"Relationship(Name: '{relationship_dict['relationship_name'] if 'relationship_name' in relationship_dict else None}', StartID: '{relationship_dict['start_id'] if 'start_id' in relationship_dict else None}', EndID: '{relationship_dict['end_id'] if 'end_id' in relationship_dict else None}')"
        
    def setRelationship( self, start_node, start_id, end_node, end_id, relationship_name):
        logger.trace("Attempting to set relationship '{relationship_name}' between startNode '{start_node}' with ID '{start_id}' and endNode '{end_node}' with ID '{end_id}'", relationship_name=relationship_name, start_node=start_node, start_id=start_id, end_node=end_node, end_id=end_id)
        with self.driver.session() as session:
            result = session.run(f"MATCH (start:{start_node} {{{start_node}ID: $start_id }}), (end:{end_node} {{{end_node}ID: $end_id }}) CREATE (start)-[:{relationship_name}]->(end) RETURN start, end", start_id=str(start_id), start_node=start_node, end_id=str(end_id), end_node=end_node)
            if result:
                logger.trace("Successfully set the relationship")
                return jsonify({"message": "Relationship created successfully."})
            else:
                logger.error("Failed to create the relationship")
                return jsonify({"message": "Could not create relationship"})
            
    def deleteRelationship(self, start_node, start_id, end_node, end_id, relationship_name):
        logger.trace("Attempting to delete relationship '{relationship_name}' between startNode '{start_node}' with ID '{start_id}' and endNode '{end_node}' with ID '{end_id}'", relationship_name=relationship_name, start_node=start_node, start_id=start_id, end_node=end_node, end_id=end_id)
        with self.driver.session() as session:
            result = session.run(f"MATCH (start:{start_node} {{{start_node}ID: $start_id }})-[r:{relationship_name}]->(end:{end_node} {{{end_node}ID: $end_id }}) DELETE r", start_id=str(start_id), start_node=start_node, end_id=str(end_id), end_node=end_node)
            if result:
                logger.trace("Successfully deleted the relationship")
                return jsonify({"message": "Resource deleted successfully."}) 
            else:
                logger.error("Failed to delete the relationship")
                return abort(404, "Could not delete")