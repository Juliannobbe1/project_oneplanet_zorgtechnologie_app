import unittest
from flask import jsonify
from flask.ctx import AppContext
from flask.testing import FlaskClient
from neo4j import Driver
from helpers.get_test_client import get_test_client

from models.domain_model import Product, Client, HealthcareProfessional, Relationship
from database.connect_database import Database

class TestGetRecommendationProducts(unittest.TestCase):
    _app_context: AppContext
    _test_client: FlaskClient
    _driver: Driver

    maxDiff = None

    @classmethod
    def setUpClass(cls):
        app_context: AppContext
        test_client = FlaskClient
        (app_context, test_client) = get_test_client()
        (cls._app_context, cls._test_client) = (app_context, test_client)
        cls._app_context.push()
        cls._driver = Database.connectDatabase()
        return super().setUpClass()
    
    @classmethod
    def tearDownClass(cls) -> None:
        cls._driver.close()
        cls._app_context.pop()
        return super().tearDownClass()

    def test_get_recommendation_products(self):
        # Set up test data
        clients = [{"ID": "5ba76134-aee6-49d7-a6df-381a002be326", "probleem": "Medicatiebeheer"}]
        expected_clients = [{"ID": "5ba76134-aee6-49d7-a6df-381a002be326", "probleem": "Medicatiebeheer"}]

        healthproviders = [{"ID": "1dcfd55b-7b5e-431a-8753-6a7e66b0b8ff", "naam": "Maximilien Petrus"}]
        products = [{"naam": "Mobility INDOOR Rollator"}]
        expected_product = [{"naam": "Mobility INDOOR Rollator"}]

        for client in clients:
            Client(self._driver).create(client)
            
        for healthprovider in healthproviders:
            HealthcareProfessional(self._driver).create(healthprovider)

        for product in products:
            Product(self._driver).create(product)
            
        client = clients[0]  # Retrieve the first client

        Client(self._driver).setClientHealthcareProfRelationship(clientID=client["ID"], zorgprofID=healthproviders[0]["ID"])

        # When
        clients_response = self._test_client.get("/client/")

        final_response = self._test_client.get(f'/product/aanbeveling/{healthproviders[0]["ID"]}/{client["probleem"]}')
        
        # Cleanup
        for healthprovider in healthproviders:
            HealthcareProfessional(self._driver).delete(healthprovider["ID"])
            
        for client in clients:
            Client(self._driver).delete(client["ID"])

        actual_clientjson = clients_response.get_json()
        expected_clientjson = jsonify(expected_clients).get_json()
        self.assertEqual(expected_clientjson, actual_clientjson)

        actual_json = final_response.get_json()
        expected_json = jsonify(expected_product).get_json()  
        self.assertEqual(expected_json, actual_json)

        
if __name__ == '__main__':
    unittest.main()
