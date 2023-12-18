import unittest
from flask import jsonify
from flask.ctx import AppContext
from flask.testing import FlaskClient
from neo4j import Driver
from helpers.get_test_client import get_test_client

from models.domain_model import Client, HealthcareProfessional, Relationship
from database.connect_database import Database

class Test(unittest.TestCase):
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

    def test_get_client_HCProf(self):
        # Given
        clients = [{"ID": "5ba76134-aee6-49d7-a6df-381a002be326","probleem": "Medicatiebeheer"}]
        expected_clients = [{"ID": "5ba76134-aee6-49d7-a6df-381a002be326","probleem": "Medicatiebeheer"}]
        
        healthproviders = [{"ID": "1dcfd55b-7b5e-431a-8753-6a7e66b0b8ff","naam": "Maximilien Petrus"}]   
        expected_healthprovider = [{"ID": "1dcfd55b-7b5e-431a-8753-6a7e66b0b8ff","naam": "Maximilien Petrus"}]   
        for healthprovider in healthproviders:
            HealthcareProfessional(self._driver).create(healthprovider)
             
        for client in clients:
            Client(self._driver).create(client)
            
        Client(self._driver).setClientHealthcareProfRelationship(clientID=client["ID"], zorgprofID=healthprovider["ID"])
            
        healthprovider_response = self._test_client.get("/zorgprofessional/")
       

        # When
        clients_response = self._test_client.get("/client/")
        
        final_response = self._test_client.get("/client/wordtverzorgd/1dcfd55b-7b5e-431a-8753-6a7e66b0b8ff")
        
        # Cleanup
        for healthprovider in healthproviders:
            HealthcareProfessional(self._driver).delete(healthprovider["ID"])
            
        for client in clients:
            Client(self._driver).delete(client["ID"])

        actual_healthprovider_json = healthprovider_response.get_json()
        expected_healthprovider_json = jsonify(expected_healthprovider).get_json()
        self.assertEqual(actual_healthprovider_json, expected_healthprovider_json)
        
        actual_clientjson = clients_response.get_json()
        expected_clientjson = jsonify(expected_clients).get_json()
        self.assertEqual(expected_clientjson, actual_clientjson)
        
        actual_json = final_response.get_json()
        expected_json = jsonify(expected_clients).get_json()
        self.assertEqual(expected_json, actual_json)


        # self.assertEqual(jsonify(expected_clients).get_json(), clients_response.get_json())
        

if __name__ == '__main__':
    unittest.main()