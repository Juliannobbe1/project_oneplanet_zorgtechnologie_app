from flask import Flask, abort, jsonify, send_file
from flask_restx import Api, Resource
from database.connect_database import database
from models.domain_model import *
import json
from api_initialation import NamespaceFactory

# Create Flask application
app = Flask(__name__)

# Create API
api = Api(app)

# Connect to the database
driver = database.connectDatabase()

# Initialize the NamespaceFactory with the database driver and API
factory = NamespaceFactory(driver=driver, api=api)

# Initialize models, namespaces, and object names using the factory
models, namespaces, object_names = factory.initialize_factory()

# Access the names of the created objects
org = eval(object_names['organisatie'])(driver)
product = eval(object_names['product'])(driver)
recommendation = eval(object_names['aanbeveling'])(driver)
application = eval(object_names['toepassing'])(driver)
client = eval(object_names['client'])(driver)
healthprof = eval(object_names['zorgprofessional'])(driver)
review = eval(object_names['review'])(driver)
supplier = eval(object_names['leverancier'])(driver)
relationship = eval(object_names['relatie'])(driver)

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
    def put(self, zorgprofessionalID, productID,clientID):
        """
        This method handles the PUT request to update a recommendation.
        It takes the payload as input and updates the recommendation with the provided data.
        It returns the updated recommendation.
        """
        recommendation.setRecommendation( zorgprofessionalID, productID,clientID)

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
        return org.get_all()

    def post(self, data):
        """
        This method handles the POST request to create a new organisation.
        It takes in data as input and creates a new organisation based on the provided data.
        If the data is None, it returns an error response indicating that information is missing.
        Otherwise, it creates the organisation and returns a success message.
        """
        if data is None:
            return abort(404, "Cannot create, information is missing")
        else:
            org.create(data)
            return jsonify({"message": "Organisation created successfully."})

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
        return org.get_all()

    def post(self, data):
        """
        This method handles the POST request to create a new organisation.
        It takes in data as input and creates a new organisation based on the provided data.
        If the data is None, it returns an error response indicating that information is missing.
        Otherwise, it creates the organisation and returns a success message.
        """
        if data is None:
            return abort(404, "Cannot create, information is missing")
        else:
            org.create(data)
            return jsonify({"message": "Organisation created successfully."})


@organisation_ns.route('/<string:property>/<value>')
class OrganisationPropertyResource(Resource):
    @api.marshal_with(orgModel)
    def get(self, property, value):
        """
        This method handles the GET request to retrieve organisations based on a specific property and its value.
        It takes in the property and value as input and returns a list of organisations matching the criteria.
        """
        return org.get(property, value)

    def delete(self, property, value):
        """
        This method handles the DELETE request to delete organisations based on a specific property and its value.
        It takes in the property and value as input and deletes the organisations matching the criteria.
        If either the property or value is None, it returns an error response indicating that information is missing.
        Otherwise, it deletes the organisations and returns a success message.
        """
        if property and value is None:
            return abort(404, "Cannot delete, information is missing")
        else:
            org.delete(property, value)
            return jsonify({"message": "Organisation deleted successfully."})


@review_ns.route('/')
class ReviewResource(Resource):
    @api.marshal_with(reviewModel)
    def get(self):
        """
        This method handles the GET request to retrieve all reviews.
        It returns a list of reviews.
        """
        return review.get_all()

    def post(self, data):
        """
        This method handles the POST request to create a new review.
        It takes in data as input and creates a new review based on the provided data.
        If the data is None, it returns an error response indicating that information is missing.
        Otherwise, it creates the review and returns a success message.
        """
        if data is None:
            return abort(404, "Cannot create, information is missing")
        else:
            review.create(data)
            return jsonify({"message": "Review created successfully."})


@review_ns.route('/<string:property>/<value>')
class ReviewPropertyResource(Resource):
    def get(self, property, value):
        """
        This method handles the GET request to retrieve reviews based on a specific property and its value.
        It takes in the property and value as input and returns a list of reviews matching the criteria.
        """
        return review.get(property, value)

    def delete(self, property, value):
        """
        This method handles the DELETE request to delete reviews based on a specific property and its value.
        It takes in the property and value as input and deletes the reviews matching the criteria.
        If either the property or value is None, it returns an error response indicating that information is missing.
        Otherwise, it deletes the reviews and returns a success message.
        """
        if property or value is None:
            return abort(404, "Cannot delete, information is missing")
        else:
            review.delete(property, value)
            return jsonify({"message": "Review deleted successfully."})




@supplier_ns.route('/')
class SupplierResource(Resource):
    @api.marshal_with(supplierModel)
    def get(self):
        """
        This method handles the GET request to retrieve all suppliers.
        It returns a list of suppliers.
        """
        return supplier.get_all()

    def post(self, data):
        """
        This method handles the POST request to create a new supplier.
        It takes in data as input and creates a new supplier based on the provided data.
        If the data is None, it returns an error response indicating that information is missing.
        Otherwise, it creates the supplier and returns a success message.
        """
        if data is None:
            return abort(404, "Cannot create, information is missing")
        else:
            supplier.create(data)
            return jsonify({"message": "Supplier created successfully."})


@supplier_ns.route('/<string:property>/<value>')
class SupplierPropertyResource(Resource):
    def get(self, property, value):
        """
        This method handles the GET request to retrieve suppliers based on a specific property and its value.
        It takes in the property and value as input and returns a list of suppliers matching the criteria.
        """
        return supplier.get(property, value)

    def delete(self, property, value):
        """
        This method handles the DELETE request to delete suppliers based on a specific property and its value.
        It takes in the property and value as input and deletes the suppliers matching the criteria.
        If either the property or value is None, it returns an error response indicating that information is missing.
        Otherwise, it deletes the suppliers and returns a success message.
        """
        if property or value is None:
            return abort(404, "Cannot delete, information is missing")
        else:
            supplier.delete(property, value)
            return jsonify({"message": "Supplier deleted successfully."})


@healthprof_ns.route('/')
class HealthProfessionalResource(Resource):
    @api.marshal_with(healthProfModel)
    def get(self):
        """
        This method handles the GET request to retrieve all health professionals.
        It returns a list of health professionals.
        """
        return healthprof.get_all()

    def post(self, data):
        """
        This method handles the POST request to create a new health professional.
        It takes in data as input and creates a new health professional based on the provided data.
        If the data is None, it returns an error response indicating that information is missing.
        Otherwise, it creates the health professional and returns a success message.
        """
        if data is None:
            return abort(404, "Cannot create, information is missing")
        else:
            healthprof.create(data)
            return jsonify({"message": "Health professional created successfully."})


@healthprof_ns.route('/<string:property>/<value>')
class HealthProfessionalPropertyResource(Resource):
    def get(self, property, value):
        """
        This method handles the GET request to retrieve health professionals based on a specific property and its value.
        It takes in the property and value as input and returns a list of health professionals matching the criteria.
        """
        return healthprof.get(property, value)

    def delete(self, property, value):
        """
        This method handles the DELETE request to delete health professionals based on a specific property and its value.
        It takes in the property and value as input and deletes the health professionals matching the criteria.
        If either the property or value is None, it returns an error response indicating that information is missing.
        Otherwise, it deletes the health professionals and returns a success message.
        """
        if property or value is None:
            return abort(404, "Cannot delete, information is missing")
        else:
            healthprof.delete(property, value)
            return jsonify({"message": "Health professional deleted successfully."})



@client_ns.route('/')
class ClientList(Resource):
    @api.marshal_with(clientModel)
    def get(self):
        """
        This method handles the GET request to retrieve all clients.
        It returns a list of clients.
        """
        return client.get_all()

    @api.expect(clientModel)
    @api.doc(description="Create a client with ID and problem")
    def post(self):
        """
        This method handles the POST request to create a new client.
        It takes the payload as input and creates a new client based on the provided data.
        If the payload is None, it returns an error response indicating that information is missing.
        Otherwise, it creates the client and returns a success message.
        """
        payload = api.payload
        if payload is None:
            return abort(404, "Cannot create, information is missing")
        else:
            client.create(payload)
            return jsonify({"message": "Client created successfully."})

    @api.expect(clientModel)
    @api.marshal_with(clientModel)
    def put(self):
        """
        This method handles the PUT request to update a client.
        It takes the payload as input and updates the client with the provided data.
        It returns the updated client.
        """
        return client.update(api.payload)


@client_ns.route('/<string:id>')
class Client(Resource):
    def get(self, id):
        """
        This method handles the GET request to retrieve a client by ID.
        It takes the client ID as input and returns the client details.
        If the ID is None, it returns an error response indicating that information is missing.
        """
        if id is None:
            return abort(404, "Cannot get, information is missing")
        else:
            return client.get(id)

    def delete(self, id):
        """
        This method handles the DELETE request to delete a client by ID.
        It takes the client ID as input and deletes the client with the provided ID.
        If the ID is None, it returns an error response indicating that information is missing.
        Otherwise, it deletes the client and returns a success message.
        """
        if id is None:
            return abort(404, "Cannot delete, information is missing")
        else:
            client.delete(id)
            return jsonify({"message": "Client deleted successfully."})


@client_ns.route('/latest')
class LatestClient(Resource):
    @api.marshal_with(clientModel)
    def get(self):
        """
        This method handles the GET request to retrieve the latest client.
        It returns the most recently created client.
        """
        return client.getLatestClient()


@client_ns.route('/relationship/<string:clientID>/<string:zorgprofID>')
class ClientRelationship(Resource):
    def put(self, clientID, zorgprofID):
        """
        This method handles the PUT request to set the relationship between a client and a healthcare professional.
        It takes the client ID and healthcare professional ID as input and establishes the relationship between them.
        """
        return client.setClientHealthcareProfRelationship(clientID, zorgprofID)


@client_ns.route('/distinct-problem')
class DistinctApplication(Resource):
    def get(self):
        """
        This method handles the GET request to retrieve distinct client problems.
        It returns a list of distinct problems reported by clients.
        """
        return client.getDistinctProblems()


@client_ns.route('/wordtverzorgd/<string:zorgprofID>')
class ClientsOfHCProf(Resource):
    def get(self, zorgprofID):
        """
        This method handles the GET request to retrieve clients associated with a specific healthcare professional.
        It takes the healthcare professional ID as input and returns the clients associated with that professional.
        """
        return client.getClientsOfHCProf(zorgprofID)

    
@application_ns.route('/')
class ApplicationResource(Resource):
    @api.marshal_with(applicationModel)
    def get(self):
        """
        This method handles the GET request to retrieve all applications.
        It returns a list of applications.
        """
        return application.get_all()

    def post(self, data):
        """
        This method handles the POST request to create a new application.
        It takes the payload as input and creates a new application based on the provided data.
        If the payload is None, it returns an error response indicating that information is missing.
        Otherwise, it creates the application and returns a success message.
        """
        if data is None:
            return abort(404, "Cannot create, information is missing")
        else:
            client.create(data)
            return jsonify({"message": "Organisation created successfully."})


@application_ns.route('/<string:property>/<value>')
class ApplicationPropertyResource(Resource):
    @api.marshal_with(applicationModel)
    def get(self, property, value):
        """
        This method handles the GET request to retrieve applications based on a specific property and value.
        It takes the property and value as input and returns the applications matching the criteria.
        """
        return application.get(property, value)

    def delete(self, property, value):
        """
        This method handles the DELETE request to delete applications based on a specific property and value.
        It takes the property and value as input and deletes the applications matching the criteria.
        If the property or value is None, it returns an error response indicating that information is missing.
        Otherwise, it deletes the applications and returns a success message.
        """
        if property or value is None:
            return abort(404, "Cannot delete, information is missing")
        else:
            application.delete(property, value)
            return jsonify({"message": "Application deleted successfully."})


@application_ns.route('/HEEFT_TOEPASSING')
class HEEFT_TOEPASSING(Resource):
    @api.marshal_with(applicationModel)
    def get(self):
        """
        This method handles the GET request to retrieve applications with products.
        It returns a list of applications that have associated products.
        """
        return application.getApplicationWithProduct()


@application_ns.route('/distinct')
class DistinctApplication(Resource):
    def get(self):
        """
        This method handles the GET request to retrieve distinct applications.
        It returns a list of distinct applications.
        """
        return application.getDistinctApplications()


# product get single
@product_ns.route('/<string:id>')
class Product(Resource):
    def get(self, id):
        """
        This method handles the GET request to retrieve a product by ID.
        It takes the product ID as input and returns the product details.
        If the ID is None, it returns an error response indicating that information is missing.
        """
        if id is None:
            return abort(404, "Cannot get, information is missing")
        else: 
            return product.get(id)

    def delete(self, id):
        """
        This method handles the DELETE request to delete a product by ID.
        It takes the product ID as input and deletes the product with the provided ID.
        If the ID is None, it returns an error response indicating that information is missing.
        Otherwise, it deletes the product and returns a success message.
        """
        if id is None:
            return abort(404, "Cannot delete, information is missing")
        else:
            product.delete(id)
            return jsonify({"message": "Product deleted successfully."})


@product_ns.route('')
class ProductResource(Resource):
    @api.marshal_with(productModel)
    def get(self):
        """
        This method handles the GET request to retrieve all products.
        It returns a list of products.
        """
        return product.get_all()

    def post(self, data):
        """
        This method handles the POST request to create a new product.
        It takes the payload as input and creates a new product based on the provided data.
        If the payload is None, it returns an error response indicating that information is missing.
        Otherwise, it creates the product and returns a success message.
        """
        if data is None:
            return abort(404, "Cannot create, information is missing")
        else:
            client.create(data)
            return jsonify({"message": "Product created successfully."})


@product_ns.route('/newest')
class NewProducts(Resource):
    @api.marshal_with(productModel)
    def get(self):
        """
        This method handles the GET request to retrieve the newest products.
        It returns a list of the newest products.
        """
        return product.getNewestProducts()


@product_ns.route('/aanbeveling/<string:zorgprofID>/<string:probleem>')
class ProductsRecommendation(Resource):
    @api.marshal_with(productModel)
    def get(self, zorgprofID, probleem):
        """
        This method handles the GET request to retrieve recommended products for a specific healthcare professional and client.
        It takes the healthcare professional ID and client ID as input and returns the recommended products.
        """
        return product.getRecommendationProducts(zorgprofID, probleem)


@product_ns.route('/client/<string:clientID>')
class ProductOneClient(Resource):
    @api.marshal_with(productModel)
    def get(self, clientID):
        """
        This method handles the GET request to retrieve products associated with a specific client.
        It takes the client ID as input and returns the products associated with the client.
        """
        return product.getProductsOneClient(clientID)


@product_ns.route('/setRecommendedRelationship/<string:zpID>/<string:productID>')
class RecommendedRelationship(Resource):
    def put(self, zpID, productID):
        """
        This method handles the PUT request to set a recommended relationship between a healthcare professional and a product.
        It takes the healthcare professional ID and product ID as input and sets the recommended relationship between them.
        """
        product.setRecommendedRelationship(zpID, productID)


@relationship_ns.route('/<string:start_node>/<string:start_id>/<string:end_node>/<string:end_id>/<string:relationship_name>')
class RelationshipResource(Resource):
    def post(self, start_node, start_id, end_node, end_id, relationship_name):
        """
        This method handles the POST request to create a relationship between two nodes.
        It takes the start node, start node ID, end node, end node ID, and relationship name as input
        and creates a relationship between the specified nodes.
        """
        return relationship.setRelationship(start_node, start_id, end_node, end_id, relationship_name)

    def delete(self, start_node, start_id, end_node, end_id, relationship_name):
        """
        This method handles the DELETE request to delete a relationship between two nodes.
        It takes the start node, start node ID, end node, end node ID, and relationship name as input
        and deletes the relationship between the specified nodes.
        If any of the input parameters is None, it returns an error response indicating that information is missing.
        Otherwise, it deletes the relationship and returns a success message.
        """
        if all(value is not None for value in (start_node, start_id, end_node, end_id, relationship_name)):
            relationship.deleteRelationship(start_node, start_id, end_node, end_id, relationship_name)
            return jsonify({"message": "Relationship deleted successfully."})
        else:
            return abort(404, "Cannot delete, information is missing")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
