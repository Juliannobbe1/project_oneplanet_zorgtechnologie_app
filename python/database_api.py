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

recommendationModel = api.model('aanbeveling', recommendation.model())
applicationModel = api.model('toepassing', application.model())
productModel = api.model('product', product.model())
clientModel = api.model('client', client.model())
healthProfModel = api.model('zorgprofessional', healthprof.model())

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
