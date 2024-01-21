import sys
from uuid import uuid4
from flask import Flask, abort, jsonify
from flask_restx import Api, Resource
from database.connect_database import Database
from models.domain_model import *
from api_initialation import NamespaceFactory
from loguru import logger
import flask_monitoringdashboard as dashboard

# Create Flask application
app = Flask(__name__)
logger.trace("Initialized Flask app")

dashboard.config.init_from(file='flask_monitoring_dashboard.cfg')
logger.trace("Initialized dashboard from configuration file")
dashboard.bind(app)
logger.trace("Successfully bound dashboard to Flask")

# Create API
api = Api(app)
logger.trace("Initialized Flask API")

# Connect to the database
driver = Database.connectDatabase()
logger.trace("Successfully connected to the database")

# Initialize the NamespaceFactory with the database driver and API
factory = NamespaceFactory(driver=driver, api=api)

# Initialize models, namespaces, and object names using the factory
models, namespaces, object_names = factory.initialize_factory()

# Access the names of the created objects
org = eval(object_names['organisatie'])(driver) # nosec
product = eval(object_names['product'])(driver) # nosec
recommendation = eval(object_names['aanbeveling'])(driver) # nosec
application = eval(object_names['toepassing'])(driver) # nosec
client = eval(object_names['client'])(driver) # nosec
healthprof = eval(object_names['zorgprofessional'])(driver) # nosec
review = eval(object_names['review'])(driver) # nosec
supplier = eval(object_names['leverancier'])(driver) # nosec
relationship = eval(object_names['relatie'])(driver) # nosec

# Access the models for each object
recommendationModel = models['aanbeveling']
applicationModel = models['toepassing']
productModel = models['product']
clientModel = models['client']
healthProfModel = models['zorgprofessional']
orgModel = models['organisatie']
reviewModel = models['review']
supplierModel = models['leverancier']
relationshipModel = models['relatie']

# Access the namespaces for each object
recommendation_ns = namespaces['aanbeveling']
application_ns = namespaces['toepassing']
product_ns = namespaces['product']
client_ns = namespaces['client']
healthprof_ns = namespaces['zorgprofessional']
organisation_ns = namespaces['organisatie']
review_ns = namespaces['review']
supplier_ns = namespaces['leverancier']
relationship_ns = namespaces['relatie']

# Define the routes for the RecommendationResource
@recommendation_ns.route('/<string:zorgprofessionalID>/<string:productID>/<string:clientID>')
class RecommendationResource(Resource):
    @api.marshal_with(recommendationModel)     
    def put(self, zorgprofessionalID, productID, clientID):
        """
        This method handles the PUT request to update a recommendation.
        It takes the payload as input and updates the recommendation with the provided data.
        It returns the updated recommendation.
        """
        requestId = uuid4()
        logger.info("requestID: '{requestId}'\nSetting recommendation for 'zorgProfessionalID': '{zorgprofessionalID}' 'productID': '{productID}' 'clientID': '{clientID}'", requestId=requestId, zorgprofessionalID=zorgprofessionalID, productID=productID, clientID=clientID)
        recommendation.setRecommendation(zorgprofessionalID, productID, clientID)
        logger.info("requestID: '{requestId}'\nSuccessfully set recommendation for 'zorgProfessionalID': '{zorgprofessionalID}' 'productID': '{productID}' 'clientID': '{clientID}'", requestId=requestId, zorgprofessionalID=zorgprofessionalID, productID=productID, clientID=clientID)

# Define the routes for the OrganisationResource
@organisation_ns.route('/')
class OrganisationResource(Resource):
    @api.doc(responses={200: 'Success'}, description='Get method description')
    @api.marshal_with(orgModel)
    def get(self):
        """
        This method handles the GET request to retrieve all organisations.
        It returns a list of organisations.
        """
        requestId = uuid4()
        logger.info("requestID: '{requestId}'\nReceived request to retrieve all organisations", requestId=requestId)
        response = org.get_all()
        logger_response = [OrganisationModel.get_str_of_dict(o) for o in response]
        logger.info("requestID: '{requestId}'\nSuccessfully retrieved all organisations '{organisations}'", requestId=requestId, organisations=logger_response)
        return response

    def post(self, data):
        """
        This method handles the POST request to create a new organisation.
        It takes in data as input and creates a new organisation based on the provided data.
        If the data is None, it returns an error response indicating that information is missing.
        Otherwise, it creates the organisation and returns a success message.
        """
        requestId = uuid4()
        logger.info("requestID: '{requestId}'\nReceived request to create organisation with data '{data}'", requestId=requestId, data=data)
        if data is None:
            logger.error("requestID: '{requestId}'\nCannot create organisation, information is missing", requestId=requestId)
            return abort(404, "Cannot create, information is missing")
        else:
            org.create(data)
            logger.info("requestID: '{requestId}'\nOrganisation created successfully with data '{data}'", requestId=requestId, data=data)
            return jsonify({"message": "Organisation created successfully."})


@organisation_ns.route('/<string:property>/<value>')
class OrganisationPropertyResource(Resource):
    @api.marshal_with(orgModel)
    def get(self, property, value):
        """
        This method handles the GET request to retrieve organisations based on a specific property and its value.
        It takes in the property and value as input and returns a list of organisations matching the criteria.
        """
        requestId = uuid4()
        logger.info("requestID: '{requestId}'\nReceived request to retrieve organisation with property '{property}' matching value '{value}'", requestId=requestId, property=property, value=value)
        response = org.get(property, value)
        logger.info("requestID: '{requestId}'\nSucessfully retrieved organisation '{organisation}'", requestId=requestId, organisation=response)
        return response

    def delete(self, property, value):
        """
        This method handles the DELETE request to delete organisations based on a specific property and its value.
        It takes in the property and value as input and deletes the organisations matching the criteria.
        If either the property or value is None, it returns an error response indicating that information is missing.
        Otherwise, it deletes the organisations and returns a success message.
        """
        requestId = uuid4()
        logger.info("requestID: '{requestId}'\nReceived request to delete organisation with property '{property}' matching value '{value}'", requestId=requestId, property=property, value=value)
        if property and value is None:
            logger.error("requestID: '{requestId}'\nCannot delete organisation, information is missing", requestId=requestId)
            return abort(404, "Cannot delete, information is missing")
        else:
            org.delete(property, value)
            logger.info("requestID: '{requestId}'\nOrganisation deleted successfully", requestId=requestId)
            return jsonify({"message": "Organisation deleted successfully."})


@review_ns.route('/')
class ReviewResource(Resource):
    @api.marshal_with(reviewModel)
    def get(self):
        """
        This method handles the GET request to retrieve all reviews.
        It returns a list of reviews.
        """
        requestId = uuid4()
        logger.info("requestID: '{requestId}'\nReceived request to retrieve all reviews", requestId=requestId)
        response = review.get_all()
        logger_response = [ReviewModel.get_str_of_dict(r) for r in response]
        logger.info("requestID: '{requestId}'\nSuccessfully retrieved all reviews '{reviews}'", requestId=requestId, reviews=logger_response)
        return response

    def post(self, data):
        """
        This method handles the POST request to create a new review.
        It takes in data as input and creates a new review based on the provided data.
        If the data is None, it returns an error response indicating that information is missing.
        Otherwise, it creates the review and returns a success message.
        """
        requestId = uuid4()
        logger.info("requestID: '{requestId}'\nReceived request to create a new review with data '{data}'", requestId=requestId, data=data)
        if data is None:
            logger.error("requestID: '{requestId}'\nCannot create review, information is missing")
            return abort(404, "Cannot create, information is missing")
        else:
            review.create(data)
            logger.info("requestID: '{requestId}'\nReview created successfully")
            return jsonify({"message": "Review created successfully."})


@review_ns.route('/<string:property>/<value>')
class ReviewPropertyResource(Resource):
    def get(self, property, value):
        """
        This method handles the GET request to retrieve reviews based on a specific property and its value.
        It takes in the property and value as input and returns a list of reviews matching the criteria.
        """
        requestId = uuid4()
        logger.info("requestID: '{requestId}'\nReceived request to retrieve review with property '{property}' containing '{value}'", requestId=requestId, property=property, value=value)
        response = review.get(property, value)
        logger.info("requestID: '{requestId}'\nSuccessfully retrieved review '{review}'", requestId=requestId, review=response)
        return response

    def delete(self, property, value):
        """
        This method handles the DELETE request to delete reviews based on a specific property and its value.
        It takes in the property and value as input and deletes the reviews matching the criteria.
        If either the property or value is None, it returns an error response indicating that information is missing.
        Otherwise, it deletes the reviews and returns a success message.
        """
        requestId = uuid4()
        logger.info("requestID: '{requestId}'\nReceived request to delete review with property '{property}' containing '{value}'", requestId=requestId, property=property, value=value)
        if property or value is None:
            logger.error("requestID: '{requestId}'\nCannot delete review, information is missing")
            return abort(404, "Cannot delete, information is missing")
        else:
            review.delete(property, value)
            logger.info("requestID: '{requestId}'\nReview deleted successfully")
            return jsonify({"message": "Review deleted successfully."})

@supplier_ns.route('/')
class SupplierResource(Resource):
    @api.marshal_with(supplierModel)
    def get(self):
        """
        This method handles the GET request to retrieve all suppliers.
        It returns a list of suppliers.
        """
        requestId = uuid4()
        logger.info("requestID: '{requestId}'\nReceived request to retrieve all suppliers", requestId=requestId)
        response = supplier.get_all()
        logger_response = [SupplierModel.get_str_of_dict(s) for s in response]
        logger.info("requestID: '{requestId}'\nSuccessfully retrieved sll suppliers '{suppliers}'", requestId=requestId, suppliers=logger_response)
        return response

    def post(self, data):
        """
        This method handles the POST request to create a new supplier.
        It takes in data as input and creates a new supplier based on the provided data.
        If the data is None, it returns an error response indicating that information is missing.
        Otherwise, it creates the supplier and returns a success message.
        """
        requestId = uuid4()
        logger.info("requestID: '{requestId}'\nReceived request to create a new supplier with data '{data}'", requestId=requestId, data=data)
        if data is None:
            logger.error("requestID: '{requestId}'\nCannot create supplier, information is missing", requestId=requestId)
            return abort(404, "Cannot create, information is missing")
        else:
            supplier.create(data)
            logger.info("requestID: '{requestId}'\nSuccessfully created supplier", requestId=requestId)
            return jsonify({"message": "Supplier created successfully."})


@supplier_ns.route('/<string:property>/<value>')
class SupplierPropertyResource(Resource):
    def get(self, property, value):
        """
        This method handles the GET request to retrieve suppliers based on a specific property and its value.
        It takes in the property and value as input and returns a list of suppliers matching the criteria.
        """
        requestId = uuid4()
        logger.info("requestID: '{requestId}'\nReceived request to retrieve all suppliers", requestId=requestId)
        response = supplier.get(property, value)
        logger.info("requestID: '{requestId}'\nSuccessfully retrieved all reviews '{reviews}'", requestId=requestId, reviews=response)
        return response

    def delete(self, property, value):
        """
        This method handles the DELETE request to delete suppliers based on a specific property and its value.
        It takes in the property and value as input and deletes the suppliers matching the criteria.
        If either the property or value is None, it returns an error response indicating that information is missing.
        Otherwise, it deletes the suppliers and returns a success message.
        """
        requestId = uuid4()
        logger.info("requestID: '{requestId}'\nReceived request to delete supplier with property '{property}' containing '{value}'", requestId=requestId, property=property, value=value)
        if property or value is None:
            logger.error("requestID: '{requestId}'\nCannot delete supplier, information is missing", requestId=requestId)
            return abort(404, "Cannot delete, information is missing")
        else:
            supplier.delete(property, value)
            logger.info("requestID: '{requestId}'\nSuccessfully deleted supplier", requestId=requestId)
            return jsonify({"message": "Supplier deleted successfully."})


@healthprof_ns.route('/')
class HealthProfessionalResource(Resource):
    @api.marshal_with(healthProfModel)
    def get(self):
        """
        This method handles the GET request to retrieve all health professionals.
        It returns a list of health professionals.
        """
        requestId = uuid4()
        logger.info("requestID: '{requestId}'\nReceived request to retrieve all HealthProfessionals", requestId=requestId)
        response = healthprof.get_all()
        logger_response = [HealthcareProfessionalModel.get_str_of_dict(h) for h in response]
        logger.info("requestID: '{requestId}'\nSuccessfully retrieved all HealthProfessionals '{healthProfessionals}'", requestId=requestId, healthProfessionals=logger_response)
        return response

    def post(self, data):
        """
        This method handles the POST request to create a new health professional.
        It takes in data as input and creates a new health professional based on the provided data.
        If the data is None, it returns an error response indicating that information is missing.
        Otherwise, it creates the health professional and returns a success message.
        """
        requestId = uuid4()
        logger.info("requestID: '{requestId}'\nReceived request to create a new HealthProfessional with data '{data}'", requestId=requestId, data=data)
        if data is None:
            logger.error("requestID: '{requestId}'\nCannot create HealthProfessional, information is missing", requestId=requestId)
            return abort(404, "Cannot create, information is missing")
        else:
            healthprof.create(data)
            logger.info("requestID: '{requestId}'\nSucessfully created HealthProfessional", requestId=requestId)
            return jsonify({"message": "Health professional created successfully."})


@healthprof_ns.route('/<string:property>/<value>')
class HealthProfessionalPropertyResource(Resource):
    def get(self, property, value):
        """
        This method handles the GET request to retrieve health professionals based on a specific property and its value.
        It takes in the property and value as input and returns a list of health professionals matching the criteria.
        """
        requestId = uuid4()
        logger.info("requestID: '{requestId}'\nReceived request to retrieve HealthProfessional with property '{property}' containing '{value}'", requestId=requestId, property=property, value=value)
        response = healthprof.get(property, value)
        logger.info("requestID: '{requestId}'\nSucessfully retrieved HealthProfessional", requestId=requestId)
        return response

    def delete(self, property, value):
        """
        This method handles the DELETE request to delete health professionals based on a specific property and its value.
        It takes in the property and value as input and deletes the health professionals matching the criteria.
        If either the property or value is None, it returns an error response indicating that information is missing.
        Otherwise, it deletes the health professionals and returns a success message.
        """
        requestId = uuid4()
        logger.info("requestID: '{requestId}'\nReceived request to delete HealthProfessional with property '{property}' containing '{value}'", requestId=requestId, property=property, value=value)
        if property or value is None:
            logger.error("requestID: '{requestId}'\nCannot delete HealthProfessional, information is missing", requestId=requestId)
            return abort(404, "Cannot delete, information is missing")
        else:
            healthprof.delete(property, value)
            logger.info("requestID: '{requestId}'\nSucessfully deleted HealthProfessional", requestId=requestId)
            return jsonify({"message": "Health professional deleted successfully."})



@client_ns.route('/')
class ClientList(Resource):
    @api.marshal_with(clientModel)
    def get(self):
        """
        This method handles the GET request to retrieve all clients.
        It returns a list of clients.
        """
        requestId = uuid4()
        logger.info("requestID: '{requestId}'\nReceived request to retrieve all clients", requestId=requestId)
        response = client.get_all()
        logger_response = [ClientModel.get_str_of_dict(c) for c in response]
        logger.info("requestID: '{requestId}'\nSucessfully retrieved all clients '{clients}'", requestId=requestId, clients=logger_response)
        return response

    @api.expect(clientModel)
    @api.doc(description="Create a client with ID and problem")
    def post(self):
        """
        This method handles the POST request to create a new client.
        It takes the payload as input and creates a new client based on the provided data.
        If the payload is None, it returns an error response indicating that information is missing.
        Otherwise, it creates the client and returns a success message.
        """
        requestId = uuid4()
        payload = api.payload
        logger.info("requestID: '{requestId}'\nReceived request to create a new client with data '{data}'", requestId=requestId, data=payload)
        if payload is None:
            logger.error("requestID: '{requestId}'\nCannot create client, information is missing", requestId=requestId)
            return abort(404, "Cannot create, information is missing")
        else:
            client.create(payload)
            logger.info("requestID: '{requestId}'\nSuccessfully created client", requestId=requestId)
            return jsonify({"message": "Client created successfully."})

    @api.expect(clientModel)
    @api.marshal_with(clientModel)
    def put(self):
        """
        This method handles the PUT request to update a client.
        It takes the payload as input and updates the client with the provided data.
        It returns the updated client.
        """
        requestId = uuid4()
        logger.info("requestID: '{requestId}'\nReceived request to update client with data '{data}'", requestId=requestId, data=api.payload)
        response = client.update(api.payload)
        logger.info("requestID: '{requestId}'\nSuccessfully updated client", requestId=requestId)
        return response


@client_ns.route('/<string:id>')
class Client(Resource):
    def get(self, id):
        """
        This method handles the GET request to retrieve a client by ID.
        It takes the client ID as input and returns the client details.
        If the ID is None, it returns an error response indicating that information is missing.
        """
        requestId = uuid4()
        logger.info("requestID: '{requestId}'\nReceived request to retrieve client with id '{id}'", requestId=requestId, id=id)
        if id is None:
            logger.error("requestID: '{requestId}'\nCannot retrieve client, information is missing", requestId=requestId)
            return abort(404, "Cannot get, information is missing")
        else:
            response = client.get(id)
            logger.info("requestID: '{requestId}'\nSuccessfully retrieved client '{client}'", requestId=requestId, client=response)
            return response

    def delete(self, id):
        """
        This method handles the DELETE request to delete a client by ID.
        It takes the client ID as input and deletes the client with the provided ID.
        If the ID is None, it returns an error response indicating that information is missing.
        Otherwise, it deletes the client and returns a success message.
        """
        requestId = uuid4()
        logger.info("requestID: '{requestId}'\nReceived request to delete client with id '{id}'", requestId=requestId, id=id)
        if id is None:
            logger.error("requestID: '{requestId}'\nCannot delete client, information is missing", requestId=requestId)
            return abort(404, "Cannot delete, information is missing")
        else:
            client.delete(id)
            logger.info("requestID: '{requestId}'\nSuccessfully deleted client", requestId=requestId)
            return jsonify({"message": "Client deleted successfully."})


@client_ns.route('/latest')
class LatestClient(Resource):
    @api.marshal_with(clientModel)
    def get(self):
        """
        This method handles the GET request to retrieve the latest client.
        It returns the most recently created client.
        """
        requestId = uuid4()
        logger.info("requestID: '{requestId}'\nRetrieved request to retrieve the latest client", requestId=requestId)
        response = client.getLatestClient()
        logger.info("requestID: '{requestId}'\nSuccessfully retrieved the latest client '{client}'", requestId=requestId, client=response)
        return response


@client_ns.route('/relationship/<string:clientID>/<string:zorgprofID>')
class ClientRelationship(Resource):
    def put(self, clientID, zorgprofID):
        """
        This method handles the PUT request to set the relationship between a client and a healthcare professional.
        It takes the client ID and healthcare professional ID as input and establishes the relationship between them.
        """
        requestId = uuid4()
        logger.info("requestID: '{requestId}'\nReceived request to set the relationship between client '{client}' and HealthcareProfessional '{healthcareProfessional}'", requestId=requestId, client=clientID, healthcareProfessional=zorgprofID)
        response = client.setClientHealthcareProfRelationship(clientID, zorgprofID)
        logger.info("requestID: '{requestId}'\nSuccessfully set the relationship between the client and HealthcareProfessional", requestId=requestId)
        return response


@client_ns.route('/distinct-problem')
class DistinctApplication(Resource):
    def get(self):
        """
        This method handles the GET request to retrieve distinct client problems.
        It returns a list of distinct problems reported by clients.
        """
        requestId = uuid4()
        logger.info("requestID: '{requestId}'\nReceived request to retrieve distinct client problems", requestId=requestId)
        response = client.getDistinctProblems()
        logger.info("requestID: '{requestId}'\nSuccessfully retrieved the distinct client problems '{distinctProblems}'", requestId=requestId, distinctProblems=response)
        return response


@client_ns.route('/wordtverzorgd/<string:zorgprofID>')
class ClientsOfHCProf(Resource):
    def get(self, zorgprofID):
        """
        This method handles the GET request to retrieve clients associated with a specific healthcare professional.
        It takes the healthcare professional ID as input and returns the clients associated with that professional.
        """
        requestId = uuid4()
        logger.info("requestID: '{requestId}'\nReceived request to retrieve clients for HealthcareProfessional '{healthcareProfessional}'", requestId=requestId, healthcareProfessional=zorgprofID)
        response = client.getClientsOfHCProf(zorgprofID)
        logger.info("requestID: '{requestId}'\nSuccessfully retrieved clients '{clients}'", requestId=requestId, clients=response)
        return response

    
@application_ns.route('/')
class ApplicationResource(Resource):
    @api.marshal_with(applicationModel)
    def get(self):
        """
        This method handles the GET request to retrieve all applications.
        It returns a list of applications.
        """
        requestId = uuid4()
        logger.info("requestID: '{requestId}'\nReceived request to retrieve all applications", requestId=requestId)
        response = application.get_all()
        logger_response = [ApplicationModel.get_str_of_dict(a) for a in response]
        logger.info("requestID: '{requestId}'\nSuccessfully retrieved all applications '{applications}'", requestId=requestId, applications=logger_response)
        return response

    def post(self, data):
        """
        This method handles the POST request to create a new application.
        It takes the payload as input and creates a new application based on the provided data.
        If the payload is None, it returns an error response indicating that information is missing.
        Otherwise, it creates the application and returns a success message.
        """
        requestId = uuid4()
        logger.info("requestID: '{requestId}'\Received request to create an application with data '{data}'", requestId=requestId, data=data)
        if data is None:
            logger.error("requestID: '{requestId}'\nCannot create application, information is missing", requestId=requestId)
            return abort(404, "Cannot create, information is missing")
        else:
            client.create(data)
            logger.info("requestID: '{requestId}'\nSuccessfully created application", requestId=requestId)
            return jsonify({"message": "Application created successfully."})


@application_ns.route('/<string:property>/<value>')
class ApplicationPropertyResource(Resource):
    @api.marshal_with(applicationModel)
    def get(self, property, value):
        """
        This method handles the GET request to retrieve applications based on a specific property and value.
        It takes the property and value as input and returns the applications matching the criteria.
        """
        requestId = uuid4()
        logger.info("requestID: '{requestId}'\nReceived request to retrieve application with property '{property}' containing '{value}'", requestId=requestId, property=property, value=value)
        response = application.get(property, value)
        logger.info("requestID: '{requestId}'\nSuccessfully retrieved application '{application}'", requestId=requestId, application=response)
        return response

    def delete(self, property, value):
        """
        This method handles the DELETE request to delete applications based on a specific property and value.
        It takes the property and value as input and deletes the applications matching the criteria.
        If the property or value is None, it returns an error response indicating that information is missing.
        Otherwise, it deletes the applications and returns a success message.
        """
        requestId = uuid4()
        logger.info("requestID: '{requestId}'\nReceived request to delete application with property '{property}' containing '{value}'", requestId=requestId, property=property, value=value)
        if property or value is None:
            logger.error("requestID: '{requestId}'\nCannot delete application, information is missing", requestId)
            return abort(404, "Cannot delete, information is missing")
        else:
            application.delete(property, value)
            logger.info("requestID: '{requestId}'\nSuccessfully deleted application", requestId=requestId)
            return jsonify({"message": "Application deleted successfully."})


@application_ns.route('/HEEFT_TOEPASSING')
class HEEFT_TOEPASSING(Resource):
    @api.marshal_with(applicationModel)
    def get(self):
        """
        This method handles the GET request to retrieve applications with products.
        It returns a list of applications that have associated products.
        """
        requestId = uuid4()
        logger.info("requestID: '{requestId}'\nReceived request to retrieve all applications with their associated products", requestId=requestId)
        response = application.getApplicationWithProduct()
        logger.info("requestID: '{requestId}'\nSucessfully retrieved all applications with their associated products '{applicationsWithProducts}'", requestId=requestId, applicationsWithProducts=response)
        return response


@application_ns.route('/distinct')
class DistinctApplication(Resource):
    def get(self):
        """
        This method handles the GET request to retrieve distinct applications.
        It returns a list of distinct applications.
        """
        requestId = uuid4()
        logger.info("requestID: '{requestId}'\nReceived request to retrieve the distinct applications", requestId=requestId)
        response = application.getDistinctApplications()
        logger.info("requestID: '{requestId}'\nSuccessfuly retrieved the distinct applications '{distinctApplications}'", requestId=requestId, distinctApplications=response)
        return response


# product get single
@product_ns.route('/<string:id>')
class Product(Resource):
    def get(self, id):
        """
        This method handles the GET request to retrieve a product by ID.
        It takes the product ID as input and returns the product details.
        If the ID is None, it returns an error response indicating that information is missing.
        """
        requestId = uuid4()
        logger.info("requestID: '{requestId}'\nReceived request to retrieve product with id '{id}'", requestId=requestId, id=id)
        if id is None:
            logger.error("requestID: '{requestId}'\nCannot retrieve product, information is missing", requestId=requestId)
            return abort(404, "Cannot get, information is missing")
        else:
            response = product.get(id)
            logger.info("requestID: '{requestId}'\nSuccessfully retrieved product '{product}'", requestId=requestId, product=ProductModel.get_str_of_dict(response))
            return response

    def delete(self, id):
        """
        This method handles the DELETE request to delete a product by ID.
        It takes the product ID as input and deletes the product with the provided ID.
        If the ID is None, it returns an error response indicating that information is missing.
        Otherwise, it deletes the product and returns a success message.
        """
        requestId = uuid4()
        logger.info("requestID: '{requestId}'\nReceived request to delete product '{id}'", requestId=requestId, id=id)
        if id is None:
            logger.error("requestID: '{requestId}'\nCannot delete product, information is missing", requestId=requestId)
            return abort(404, "Cannot delete, information is missing")
        else:
            product.delete(id)
            logger.info("requestID: '{requestId}'\nSuccessfully deleted product", requestId=requestId)
            return jsonify({"message": "Product deleted successfully."})


@product_ns.route('')
class ProductResource(Resource):
    @api.marshal_with(productModel)
    def get(self):
        """
        This method handles the GET request to retrieve all products.
        It returns a list of products.
        """
        requestId = uuid4()
        logger.info("requestID: '{requestId}'\nReceived request to retrieve all products", requestId=requestId)
        response = product.get_all()
        logger_response = [ProductModel.get_str_of_dict(p) for p in response]
        logger.info("requestID: '{requestId}'\nSuccessfully retrieved all products '{products}'", requestId=requestId, products=logger_response)
        return response

    def post(self, data):
        """
        This method handles the POST request to create a new product.
        It takes the payload as input and creates a new product based on the provided data.
        If the payload is None, it returns an error response indicating that information is missing.
        Otherwise, it creates the product and returns a success message.
        """
        requestId = uuid4()
        logger.info("requestID: '{requestId}'\nReceived request to create new product with data '{data}'", requestId=requestId, data=data)
        if data is None:
            logger.error("requestID: '{requestId}'\nCannot create product, information is missing", requestId=requestId)
            return abort(404, "Cannot create, information is missing")
        else:
            client.create(data)
            logger.info("requestID: '{requestId}'\nSuccessfully created product", requestId=requestId)
            return jsonify({"message": "Product created successfully."})


@product_ns.route('/newest')
class NewProducts(Resource):
    @api.marshal_with(productModel)
    def get(self):
        """
        This method handles the GET request to retrieve the newest products.
        It returns a list of the newest products.
        """
        requestId = uuid4()
        logger.info("requestID: '{requestId}'\nReceived request to retrieve the newest products", requestId=requestId)
        response = product.getNewestProducts()
        logger_response = [ProductModel.get_str_of_dict(p) for p in response]
        logger.info("requestID: '{requestId}'\nSuccessfully retrieved the newest products '{products}'", requestId=requestId, products=logger_response)
        return response


@product_ns.route('/aanbeveling/<string:zorgprofID>/<string:probleem>')
class ProductsRecommendation(Resource):
    @api.marshal_with(productModel)
    def get(self, zorgprofID, probleem):
        """
        This method handles the GET request to retrieve recommended products for a specific healthcare professional and problem.
        It takes the healthcare professional ID and problem ID as input and returns the recommended products.
        """
        requestId = uuid4()
        logger.info("requestID: '{requestId}'\nReceived request to retrieve recommended products for HealthcareProfessional '{healthcareProfessional}' and problem '{problem}'", requestId=requestId, healthcareProfessional=zorgprofID, problem=probleem)
        response = product.getRecommendationProducts(zorgprofID, probleem)
        logger_response = [ProductModel.get_str_of_dict(p) for p in response]
        logger.info("requestID: '{requestId}'\nSuccessfully retrieved recommendation products '{recommendationProducts}'", requestId=requestId, recommendationProducts=logger_response)
        return response


@product_ns.route('/client/<string:clientID>')
class ProductOneClient(Resource):
    @api.marshal_with(productModel)
    def get(self, clientID):
        """
        This method handles the GET request to retrieve products associated with a specific client.
        It takes the client ID as input and returns the products associated with the client.
        """
        requestId = uuid4()
        logger.info("requestID: '{requestId}'\nReceived request to retrieve all products for client '{client}'", requestId=requestId, client=clientID)
        response = product.getProductsOneClient(clientID)
        logger_response = [ProductModel.get_str_of_dict(p) for p in response]
        logger.info("requestID: '{requestId}'\nSuccessfully retrieved the products '{products}'", requestId=requestId, products=logger_response)
        return response


@product_ns.route('/setRecommendedRelationship/<string:zpID>/<string:productID>')
class RecommendedRelationship(Resource):
    def put(self, zpID, productID):
        """
        This method handles the PUT request to set a recommended relationship between a healthcare professional and a product.
        It takes the healthcare professional ID and product ID as input and sets the recommended relationship between them.
        """
        requestId = uuid4()
        logger.info("requestID: '{requestId}'\nReceived request to set a recommended relationship between HealthcareProfessional '{healthcareProfessional}' and product '{product}'", requestId=requestId, healthcareProfessional=zpID, product=productID)
        product.setRecommendedRelationship(zpID, productID)
        logger.info("requestID: '{requestId}'\nSuccessfully set the recommended relationship", requestId=requestId)


@relationship_ns.route('/<string:start_node>/<string:start_id>/<string:end_node>/<string:end_id>/<string:relationship_name>')
class RelationshipResource(Resource):
    def post(self, start_node, start_id, end_node, end_id, relationship_name):
        """
        This method handles the POST request to create a relationship between two nodes.
        It takes the start node, start node ID, end node, end node ID, and relationship name as input
        and creates a relationship between the specified nodes.
        """
        requestId = uuid4()
        logger.info("requestID: '{requestId}'\nReceived request to create relationship '{relationship_name}' between startNode '{start_node}' with ID '{start_id}' and endNode '{end_node}' with ID '{end_id}'", requestId=requestId, relationship_name=relationship_name, start_node=start_node, start_id=start_id, end_node=end_node, end_id=end_id)
        response = relationship.setRelationship(start_node, start_id, end_node, end_id, relationship_name)
        logger.info("requestID: '{requestId}'\nSuccessfully set the relationship", requestId=requestId)
        return response

    def delete(self, start_node, start_id, end_node, end_id, relationship_name):
        """
        This method handles the DELETE request to delete a relationship between two nodes.
        It takes the start node, start node ID, end node, end node ID, and relationship name as input
        and deletes the relationship between the specified nodes.
        If any of the input parameters is None, it returns an error response indicating that information is missing.
        Otherwise, it deletes the relationship and returns a success message.
        """
        requestId = uuid4()
        logger.info("requestID: '{requestId}'\nReceived request to delete relationship '{relationship_name}' between startNode '{start_node}' with ID '{start_id}' and endNode '{end_node}' with ID '{end_id}'", requestId=requestId, relationship_name=relationship_name, start_node=start_node, start_id=start_id, end_node=end_node, end_id=end_id)
        if all(value is not None for value in (start_node, start_id, end_node, end_id, relationship_name)):
            relationship.deleteRelationship(start_node, start_id, end_node, end_id, relationship_name)
            logger.info("requestID: '{requestId}'\nSuccessfully deleted relationship", requestId=requestId)
            return jsonify({"message": "Relationship deleted successfully."})
        else:
            logger.error("requestID: '{requestId}'\nCannot delete relationship, information is missing")
            return abort(404, "Cannot delete, information is missing")

def main():
    # Remove the default logger and add the custom loggers
    logger.remove()
    logger.add(sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>", level="TRACE")
    logger.add(sys.stderr, format="<red>{time}</red> <level>{message}</level>", level="ERROR")
    logger.add("logs/file_{time}.log", level="TRACE", rotation="1 day")
    logger.trace("Starting app on port 5001")
    app.run(host='::', port=5001)

if __name__ == '__main__':
    main()
