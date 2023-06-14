from flask import Flask, abort, jsonify
from flask_restx import Api, Resource
from database.connect_database import database
from models.domain_model import *
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
        
    def post(self, property, value):
        # if data is None:
        if property and value is None:
            return abort(404, "cannot create, information is missing")
        else: 
            property_list = property.split(', ')
            value_list = value.split(', ')
            
        recommendation.create(property_list, value_list)
        return jsonify({"message": "Organisation created succesfully."})


@organisation_ns.route('/')        
class OrganisationResource(Resource):
    @api.doc(responses={200: 'Success'}, description='Get method description')
    @api.marshal_with(orgModel)
    def get(self):
       return org.get_all()

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
        
    def post(self, property, value):
        # if data is None:
        if property and value is None:
            return abort(404, "cannot create, information is missing")
        else: 
            property_list = property.split(', ')
            value_list = value.split(', ')
            print(property_list, value_list)

        org.create(property_list, value_list)
        return jsonify({"message": "Organisation created succesfully."})
        
# review
@review_ns.route('/')
class ReviewResource(Resource):
    @api.marshal_with(reviewModel) 
    def get(self):
        return review.get_all()

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
    
    def post(self, property, value):
        if property and value is None:
            return abort(404, "cannot create, information is missing")
        else: 
            property_list = property.split(', ')
            value_list = value.split(', ')
            print(property_list, value_list)

        review.create(property_list, value_list)
        return jsonify({"message": "Review created succesfully."})

# supplier
@supplier_ns.route('/')
class SupplierResource(Resource):
    @api.marshal_with(supplierModel) 
    def get(self):
        return supplier.get_all()

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
        
    def post(self, property, value):
        if property and value is None:
            return abort(404, "cannot create, information is missing")
        else: 
            property_list = property.split(', ')
            value_list = value.split(', ')
            print(property_list, value_list)

        supplier.create(property_list, value_list)
        return jsonify({"message": "Organisation created succesfully."})
            
# healthprofessional
@healthprof_ns.route('/')
class HealthProfessionalResource(Resource):
    @api.marshal_with(healthProfModel) 
    def get(self):
        return healthprof.get_all()

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
        
    def post(self, property, value):
        if property and value is None:
            return abort(404, "cannot create, information is missing")
        else: 
            property_list = property.split(', ')
            value_list = value.split(', ')
            print(property_list, value_list)

        healthprof.create(property_list, value_list)
        return jsonify({"message": "Organisation created succesfully."})

# Client
@client_ns.route('/')
class ClientResource(Resource):
    @api.marshal_with(clientModel) 
    def get(self):
        return client.get_all()

@client_ns.route('/<string:property>/<value>')
class ClientPropertyResource(Resource):
    def get(self, property, value):
        return client.get(property, value)
    
    def delete(self, property, value):
        if property or value is None:
            return abort(404, "Cannot delete, information is missing")
        else: 
            client.delete(property, value)
            return jsonify({"message": "client deleted successfully."})
    
    def post(self, property, value):
        if property and value is None:
            return abort(404, "cannot create, information is missing")
        else: 
            property_list = property.split(', ')
            value_list = value.split(', ')
            print(property_list, value_list)

        client.create(property_list, value_list)
        return jsonify({"message": "Organisation created succesfully."})
    
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
        
    def post(self, property, value):
        if property and value is None:
            return abort(404, "cannot create, information is missing")
        else: 
            property_list = property.split(', ')
            value_list = value.split(', ')
            print(property_list, value_list)

        application.create(property_list, value_list)
        return jsonify({"message": "Organisation created succesfully."})
    
@application_ns.route('/HEEFT_TOEPASSING')
class HEEFT_TOEPASSING(Resource):
    @api.marshal_with(applicationModel) 
    def get(self):
        return application.getApplicationWithProduct()

@application_ns.route('/distinct')
class DistinctApplication(Resource):
    def get(self):
        return application.getDistinctApplications()

# product 
@product_ns.route('')
class ProductResource(Resource):
    @api.marshal_with(productModel) 
    def get(self):
        return product.get_all()

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

@product_ns.route('/<string:property>/<value>')
class ProductPropertyResource(Resource):
    def get(self, property, value):
        return product.get(property, value)
    
    def delete(self, property, value):
        if property or value is None:
            return abort(404, "Cannot delete, information is missing")
        else: 
            product.delete(property, value)
            return jsonify({"message": "product deleted successfully."})
        
    def post(self, property, value):
        # if data is None:
        if property and value is None:
            return abort(404, "cannot create, information is missing")
        else: 
            property_list = property.split(', ')
            value_list = value.split(', ')

        product.create(property_list, value_list)
        return jsonify({"message": "Organisation created succesfully."})

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
