from flask import Flask, request
from flask_restx import Api, Resource, fields
from database.connect_database import database
from models.domain_model import *

app = Flask(__name__)
api = Api(app)

driver = database.connectDatabase()
product = Product(driver)
getModel = product.Model()
productModel = api.model('product', getModel)

@api.route('/products')
class ProductList(Resource):
    @api.marshal_with(productModel) 
    def get(self):
        return product.get_all()
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
