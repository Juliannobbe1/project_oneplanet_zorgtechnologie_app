from flask import Flask, abort, jsonify, send_file
from flask_restx import Api, Resource
from database.connect_database import database
from models.domain_model import *
import json
from api_initialation import NamespaceFactory

app = Flask(__name__)
api = Api(app)
driver = database.connectDatabase()

factory = NamespaceFactory(driver=driver, api=api)
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

recommendationModel = models['aanbeveling']
applicationModel = models['toepassing']
productModel = models['product']
clientModel = models['client']
healthProfModel = models['zorgprofessional']
orgModel = models['organisatie']
reviewModel = models['review']
supplierModel = models['leverancier']
relationshipModel = models['relatie']

recommendation_ns = namespaces['aanbeveling']
application_ns = namespaces['toepassing']
product_ns = namespaces['product']
client_ns = namespaces['client']
healthprof_ns = namespaces['zorgprofessional']
organisation_ns = namespaces['organisatie']
review_ns = namespaces['review']
supplier_ns = namespaces['leverancier']
relationship_ns = namespaces['relatie']

@recommendation_ns.route('/')
class RecommendationResource(Resource):
    @api.marshal_with(recommendationModel) 
    def get(self):
        return recommendation.get_all()
    
    def post(self, data):
        if data is None:
            return abort(404, "cannot create, information is missing")
        else: 
            recommendation.create(data)
            return jsonify({"message": "Organisation created succesfully."})

@recommendation_ns.route('/<string:property>/<value>')
class RecommendationPropertyResource(Resource):
    def get(self, property, value):
        return recommendation.get(property, value)
    
    def delete(self, property, value):
        if property or value is None:
            return abort(404, "Cannot delete, information is missing")
        else: 
            recommendation.delete(property, value)
            return jsonify({"message": "Recommmendation deleted successfully."})

@organisation_ns.route('/')        
class OrganisationResource(Resource):
    @api.doc(responses={200: 'Success'}, description='Get method description')
    @api.marshal_with(orgModel)
    def get(self):
       return org.get_all()
   
    def post(self, data):
        # if data is None:
        if data is None:
            return abort(404, "cannot create, information is missing")
        else: 
            org.create(data)
            return jsonify({"message": "Organisation created succesfully."})

@organisation_ns.route('/<string:property>/<value>')        
class OrganisationPropertyResource(Resource):
    @api.marshal_with(orgModel) 
    def get(self, property, value):
        return org.get(property, value)
        
    def delete(self, property, value):
        if property and value is None:
            return abort(404, "Cannot delete, information is missing")
        else: 
            org.delete(property, value)
            return jsonify({"message": "Organisation deleted successfully."})
        
# review
@review_ns.route('/')
class ReviewResource(Resource):
    @api.marshal_with(reviewModel) 
    def get(self):
        return review.get_all()
    
    def post(self, data):
        # if data is None:
        if data is None:
            return abort(404, "cannot create, information is missing")
        else: 
            review.create(data)
            return jsonify({"message": "Organisation created succesfully."})

@review_ns.route('/<string:property>/<value>')
class ReviewPropertyResource(Resource):
    def get(self, property, value):
        return review.get(property, value)
    
    def delete(self, property, value):
        if property or value is None:
            return abort(404, "Cannot delete, information is missing")
        else: 
            review.delete(property, value)
            return jsonify({"message": "Review deleted successfully."})

# supplier
@supplier_ns.route('/')
class SupplierResource(Resource):
    @api.marshal_with(supplierModel) 
    def get(self):
        return supplier.get_all()
    
    def post(self, data):
        # if data is None:
        if data is None:
            return abort(404, "cannot create, information is missing")
        else: 
            supplier.create(data)
            return jsonify({"message": "Organisation created succesfully."})

@supplier_ns.route('/<string:property>/<value>')
class SupplierPropertyResource(Resource):
    def get(self, property, value):
        return supplier.get(property, value)
    
    def delete(self, property, value):
        if property or value is None:
            return abort(404, "Cannot delete, information is missing")
        else: 
            supplier.delete(property, value)
            return jsonify({"message": "supplier deleted successfully."})
            
# healthprofessional
@healthprof_ns.route('/')
class HealthProfessionalResource(Resource):
    @api.marshal_with(healthProfModel) 
    def get(self):
        return healthprof.get_all()
    
    def post(self, data):
        if data is None:
            return abort(404, "cannot create, information is missing")
        else: 
            healthprof.create(data)
            return jsonify({"message": "Organisation created succesfully."})

@healthprof_ns.route('/<string:property>/<value>')
class HealthProfessionalPropertyResource(Resource):
    def get(self, property, value):
        return healthprof.get(property, value)
    
    def delete(self, property, value):
        if property or value is None:
            return abort(404, "Cannot delete, information is missing")
        else: 
            healthprof.delete(property, value)
            return jsonify({"message": "healthporfessional deleted successfully."})

# Client
@client_ns.route('/')
class ClientList(Resource):
    @api.marshal_with(clientModel) 
    def get(self):
        return client.get_all()
    
    @api.expect(clientModel)
    @api.doc(description="Create a client with ID and probleem")
    def post(self):
        payload = api.payload
        if payload is None:
            return abort(404, "cannot create, information is missing")
        else: 
            client.create(payload)
            return jsonify({"message": "Client created succesfully."})
        
    @api.expect(clientModel)
    @api.marshal_with(clientModel)
    def put(self):
        '''Update a task given its identifier'''
        return client.update( api.payload)

@client_ns.route('/<int:id>')
class Client(Resource):
    def get(self, id):
        if id is None:
            return abort(404, "Cannot get, information missing")
        return client.get(id)
    
    def delete(self, id):
        if id is None:
            return abort(404, "Cannot delete, information is missing")
        else: 
            client.delete(id)
            return jsonify({"message": "client deleted successfully."})
        
@client_ns.route('/latest')
class LatestClient(Resource):
    @api.marshal_with(clientModel)
    def get(self):
        return client.getLatestClient()

@client_ns.route('/relationship/<int:clientID>/<int:zorgprofID>')
class ClientRelationship(Resource):
    def put(self, clientID, zorgprofID):
        return client.setClientHealthcareProfRelationship(clientID, zorgprofID)
    
@client_ns.route('/distinct-problem')
class DistinctApplication(Resource):
    def get(self):
        return client.getDistinctProblems()
    
@client_ns.route('/wordtverzorgd/<int:zorgprofID>')
class ClientsOfHCProf(Resource):
    def get(self, zorgprofID):
        return client.getClientsOfHCProf(zorgprofID)

# toepassing
@application_ns.route('/')
class ApplicationResource(Resource):
    @api.marshal_with(applicationModel) 
    def get(self):
        return application.get_all()
    
    def post(self, data):
        if data is None:
            return abort(404, "cannot create, information is missing")
        else: 
            client.create(data)
            return jsonify({"message": "Organisation created succesfully."})


@application_ns.route('/<string:property>/<value>')
class ApplicationPropertyResource(Resource):
    @api.marshal_with(applicationModel) 
    def get(self, property, value):
        return application.get(property, value)
    
    def delete(self, property, value):
        if property or value is None:
            return abort(404, "Cannot delete, information is missing")
        else: 
            application.delete(property, value)
            return jsonify({"message": "application deleted successfully."})      
        
@application_ns.route('/HEEFT_TOEPASSING')
class HEEFT_TOEPASSING(Resource):
    @api.marshal_with(applicationModel) 
    def get(self):
        return application.getApplicationWithProduct()

@application_ns.route('/distinct')
class DistinctApplication(Resource):
    def get(self):
        return application.getDistinctApplications()

# product get single        
@product_ns.route('/<int:id>')
class Product(Resource):
    def get(self, id):
        if id is None:
            return abort(404, "Cannot get, information missing")
        return product.get(id)
    
    def delete(self, id):
        if id is None:
            return abort(404, "Cannot delete, information is missing")
        else: 
            product.delete(id)
            return jsonify({"message": "client deleted successfully."})
        
# product 
@product_ns.route('')
class ProductResource(Resource):
    @api.marshal_with(productModel) 
    def get(self):
        return product.get_all()
    
    def post(self, data):
        if data is None:
            return abort(404, "cannot create, information is missing")
        else: 
            client.create(data)
            return jsonify({"message": "Organisation created succesfully."})

@product_ns.route('/newest')
class NewProducts(Resource):
    @api.marshal_with(productModel)
    def get(self):
        return product.getNewestProducts()
    
@product_ns.route('/aanbeveling/<int:zorgprofID>/<int:clientID>')
class ProductsRecommendation(Resource):
    @api.marshal_with(productModel)
    def get(self, zorgprofID, clientID):
        return product.getRecommendationProducts(zorgprofID, clientID)

@product_ns.route('/client/<int:clientID>')    
class ProductOneClient(Resource):
    @api.marshal_with(productModel)
    def get(self, clientID):
        return product.getProductsOneClient(clientID)
    
@product_ns.route('/setRecommendedRelationship/<int:zpID>/<int:productID>')
class RecommendedRelationship(Resource):
    def put(self,zpID, productID):
        product.setRecommendedRelationship(zpID,productID)

@relationship_ns.route('/<string:start_node>/<int:start_id>/<string:end_node>/<int:end_id>/<string:relationship_name>')    
class RelationshipResource(Resource):
    def post(self, start_node, start_id, end_node, end_id, relationship_name):
        return relationship.setRelationship(start_node, start_id, end_node, end_id, relationship_name)
    
    def delete(self, start_node, start_id, end_node, end_id, relationship_name):
        #!test this if works ???
        if all(value is not None for value in (start_node, start_id, end_node, end_id, relationship_name)):
            relationship.deleteRelationship(start_node, start_id, end_node, end_id, relationship_name)
            return jsonify({"message": "Recommmendation deleted successfully."})
        else: 
            return abort(404, "Cannot delete, information is missing")
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
