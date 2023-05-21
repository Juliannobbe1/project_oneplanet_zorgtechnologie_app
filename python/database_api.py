from flask import Flask, request
from flask_restx import Api, Resource, fields
from database.connect_database import database
from models.domain_model import *


app = Flask(__name__)
api = Api(app)
driver = database.connectDatabase()

product = Product(driver)
recommendation = Recommendation(driver)
application = Application(driver)
client = Client(driver)
healthprof = HealthcareProfessional(driver)
org = Organisation(driver)
review = Review(driver)
supplier = Supplier(driver)

recommendationModel = api.model('aanbeveling', recommendation.model())
applicationModel = api.model('toepassing', application.model())
productModel = api.model('product', product.model())
clientModel = api.model('client', client.model())
healthProfModel = api.model('zorgprofessional', healthprof.model())
orgModel = api.model('organisatie', org.model())
reviewModel = api.model('review', review.model())
supplierModel = api.model('leverancier', supplier.model())

# organisatie
@api.route('/organisation', '/organisation/<string:property>/<string:value>')
class OrganisationAPI(Resource):
    @api.marshal_with(orgModel) 
    def get(self, property=None, value=None):
        if property is None and value is None:
            return org.get_all()
        else:
            if value.isdigit():  # Check if value is an integer
                value = int(value)
            return org.get(property, value)
        
# review
@api.route('/review', '/review/<string:property>/<string:value>')
class ReviewAPI(Resource):
    @api.marshal_with(reviewModel) 
    def get(self, property=None, value=None):
        if property is None and value is None:
            return review.get_all()
        else:
            if value.isdigit():  # Check if value is an integer
                value = int(value)
            return review.get(property, value)

# supplier
@api.route('/supplier','/supplier/<string:property>/<string:value>')
class SupplierAPI(Resource):
    @api.marshal_with(supplierModel) 
    def get(self, property=None, value=None):
        if property is None and value is None:
            return supplier.get_all()
        else:
            if value.isdigit():  # Check if value is an integer
                value = int(value)
            return supplier.get(property, value)

@api.route('/healthprofessional','/healthprofessional/<string:property>/<string:value>')
class HealthProfAPI(Resource):
    @api.marshal_with(healthProfModel) 
    def get(self, property=None, value=None):
        if property is None and value is None:
            return healthprof.get_all()
        else:
            if value.isdigit():  # Check if value is an integer
                value = int(value)
            return healthprof.get(property, value)

@api.route('/client', '/client/<string:property>/<string:value>')
class ClientAPI(Resource):
    @api.marshal_with(clientModel) 
    def get(self, property=None, value=None):
        if property is None and value is None:
            return client.get_all()
        else:
            if value.isdigit():  # Check if value is an integer
                value = int(value)
            return client.get(property, value)

@api.route('/application', '/application/<string:property>/<string:value>')
class ApplicationAPI(Resource):
    @api.marshal_with(applicationModel) 
    def get(self, property=None, value=None):
        if property is None and value is None:
            return application.get_all()
        else:
            if value.isdigit():  # Check if value is an integer
                value = int(value)
            return application.get(property, value)
    
@api.route('/products', '/products/<string:property>/<string:value>')
class ProductAPI(Resource):
    @api.marshal_with(productModel) 
    def get(self, property=None, value=None):
        if property is None and value is None:
            return product.get_all()
        else:
            if value.isdigit():  # Check if value is an integer
                value = int(value)
            return product.get(property, value)
        
@api.route('/recommendations','/recommendations/<string:property>/<string:value>')    
class RecommendationAPI(Resource):
    @api.marshal_with(recommendationModel)
    def get(self, property=None, value=None):
        if property is None and value is None:
            return recommendation.get_all()
        else:
            if value.isdigit():  # Check if value is an integer
                value = int(value)
            return recommendation.get(property, value)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
