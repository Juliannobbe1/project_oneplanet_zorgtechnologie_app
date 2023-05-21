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
@api.route('/organisation')
class OrgList(Resource):
    @api.marshal_with(orgModel) 
    def get_all(self):
        return org.get_all()
    
@api.route('/organisation/<string:property> <value>')    
class Org(Resource):
    @api.marshal_with(orgModel)
    def get(self, property, value):
        if value.isdigit():  # Check if value is an integer
            value = int(value)    
        return org.get(property, value)
        

# review
@api.route('/review')
class ReviewList(Resource):
    @api.marshal_with(reviewModel) 
    def get(self):
        return review.get_all()

# supplier
@api.route('/supplier')
class SupplierList(Resource):
    @api.marshal_with(supplierModel) 
    def get(self):
        return supplier.get_all()

@api.route('/healthprofessional')
class HealthProfList(Resource):
    @api.marshal_with(healthProfModel) 
    def get(self):
        return healthprof.get_all()

@api.route('/client')
class ClientList(Resource):
    @api.marshal_with(clientModel) 
    def get(self):
        return client.get_all()

@api.route('/application')
class ApplicationList(Resource):
    @api.marshal_with(applicationModel) 
    def get(self):
        return application.get_all()
    
@api.route('/products')
class ProductList(Resource):
    @api.marshal_with(productModel) 
    def get(self):
        return product.get_all()

@api.route('/recommendations')    
class RecommendationList(Resource):
    @api.marshal_with(recommendationModel)
    def get(self):
        return recommendation.get_all()
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
