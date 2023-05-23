from flask import Flask, request, abort, Response, jsonify
from flask_restx import Api, Resource, fields, Namespace
from database.connect_database import database
from models.domain_model import *
from api_initialation import NamespaceFactory

app = Flask(__name__)
api = Api(app)
driver = database.connectDatabase()

factory = NamespaceFactory(driver=driver, api=api)
models, namespaces, object_names = factory.initialize_factory()

# Access the names of the created objects
org = object_names['organisatie']
product = object_names['product']
recommendation = object_names['aanbeveling']
application = object_names['toepassing']
client = object_names['client']
healthprof = object_names['zorgprofessional']
review = object_names['review']
supplier = object_names['leverancier']

recommendationModel = models['aanbeveling']
applicationModel = models['toepassing']
productModel = models['product']
clientModel = models['client']
healthProfModel = models['zorgprofessional']
orgModel = models['organisatie']
reviewModel = models['review']
supplierModel = models['leverancier']

recommendation_ns = namespaces['aanbeveling']
application_ns = namespaces['toepassing']
product_ns = namespaces['product']
client_ns = namespaces['client']
healthprof_ns = namespaces['zorgprofessional']
organisation_ns = namespaces['organisatie']
review_ns = namespaces['review']
supplier_ns = namespaces['leverancier']


@organisation_ns.route('/organisation')        
class OrganisationResource(Resource):
    @api.doc(responses={200: 'Success'}, description='Get method description')
    @api.marshal_with(orgModel)
    def get(self):
       return org.get_all

@organisation_ns.route('/organisation/<string:property>/<value>')        
class OrganisationPropertyResource(Resource):
    @api.marshal_with(orgModel) 
    def get(self, property, value):
        return org.get(property, value)
        
    def delete(self, property, value):
        if property or value is None:
            return abort(404, "Cannot delete, information is missing")
        else: 
            org.delete(property, value)
            return jsonify({"message": "Organisation deleted successfully."})
        
    def post(self, property, value):
        if property or value is None:
            return abort(404, "cannot create, information is missing")
        else: 
            org.create(property, value)
            return jsonify({"message": "Organisation created succesfully."})
        
# review
@review_ns.route('/review')
class ReviewResource(Resource):
    @api.marshal_with(reviewModel) 
    def get(self):
        return review.get_all()

@review_ns.route('/review/<string:property>/<value>')
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
@supplier_ns.route('/supplier')
class SupplierResource(Resource):
    @api.marshal_with(supplierModel) 
    def get(self):
        return supplier.get_all()

@supplier_ns.route('/supplier/<string:property>/<value>')
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
@healthprof_ns.route('/healthprofessional')
class HealthProfessionalResource(Resource):
    @api.marshal_with(healthProfModel) 
    def get(self):
        return healthprof.get_all()

@healthprof_ns.route('/healthprofessional/<string:property>/<value>')
class HealthProfessionalPropertyResource(Resource):
    def get(self, property, value):
        return healthprof.get(property, value)
    
    def delete(self, property, value):
        if property or value is None:
            return abort(404, "Cannot delete, information is missing")
        else: 
            healthprof.delete(property, value)
            return jsonify({"message": "healthporfessional deleted successfully."})

@client_ns.route('/client')
class ClientResource(Resource):
    @api.marshal_with(clientModel) 
    def get(self):
        return client.get_all()

@client_ns.route('/client/<string:property>/<value>')
class ClientPropertyResource(Resource):
    def get(self, property, value):
        return client.get(property, value)
    
    def delete(self, property, value):
        if property or value is None:
            return abort(404, "Cannot delete, information is missing")
        else: 
            client.delete(property, value)
            return jsonify({"message": "client deleted successfully."})

@application_ns.route('/application')
class ApplicationResource(Resource):
    @api.marshal_with(applicationModel) 
    def get(self):
        return application.get_all()

@application_ns.route('/application/<string:property>/<value>')
class ApplicationPropertyResource(Resource):
    def get(self, property, value):
        return application.get(property, value)
    
    def delete(self, property, value):
        if property or value is None:
            return abort(404, "Cannot delete, information is missing")
        else: 
            application.delete(property, value)
            return jsonify({"message": "application deleted successfully."})
        
@product_ns.route('/product')
class ProductResource(Resource):
    @api.marshal_with(productModel) 
    def get(self):
        return product.get_all()

@product_ns.route('/product/<string:property>/<value>')
class ProductPropertyResource(Resource):
    def get(self, property, value):
        return product.get(property, value)
    
    def delete(self, property, value):
        if property or value is None:
            return abort(404, "Cannot delete, information is missing")
        else: 
            product.delete(property, value)
            return jsonify({"message": "product deleted successfully."})

@recommendation_ns.route('/recommendations')
class RecommendationResource(Resource):
    @api.marshal_with(recommendationModel) 
    def get(self):
        return recommendation.get_all()

@recommendation_ns.route('/recommendations/<string:property>/<value>')
class RecommendationPropertyResource(Resource):
    def get(self, property, value):
        return recommendation.get(property, value)
    
    def delete(self, property, value):
        if property or value is None:
            return abort(404, "Cannot delete, information is missing")
        else: 
            recommendation.delete(property, value)
            return jsonify({"message": "Recommmendation deleted successfully."})
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
