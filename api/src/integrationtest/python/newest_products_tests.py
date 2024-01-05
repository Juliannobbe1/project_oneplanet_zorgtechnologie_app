import unittest
from flask import jsonify
from flask.ctx import AppContext
from flask.testing import FlaskClient
from neo4j import Driver
from helpers.get_test_client import get_test_client

from models.domain_model import ProductModel
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

    def test_get_newest_products(self):
        # Given
        products = [{"beschrijving": "Een beveiligingscamera die je huis of kantoor bewaakt. Het heeft nachtzicht bewegingsdetectie en kan live videobeelden streamen naar je smartphone.", "ID": "35fdf7f3-0296-4cce-b491-8080b2d16c19", "leverancierID": "259a92a3-370a-4c57-a7c2-88c5c89d8dd8", "link": "https://example.com/beveiligingscamera", "naam": "Beveiligingscamera", "prijs": 129.99, "imageBase64": None}, {"beschrijving": "Een draadloze oplader die het mogelijk maakt om je telefoon draadloos op te laden. Het is compatibel met de meeste moderne smartphones en heeft een slank ontwerp.", "ID": "be4f32d9-5843-4104-9f00-a8bfdf96f11e", "leverancierID": "45e22d68-9632-42b9-83ad-6ff5a4e577b0", "link": "https://example.com/draadloze-oplader", "naam": "Draadloze Oplader", "prijs": 29.99, "imageBase64": None}, {"beschrijving": "Een opvouwbare toiletsteun die extra stabiliteit biedt bij het opstaan en gaan zitten. Het is gemakkelijk op te bergen en heeft antislipvoeten voor veiligheid.", "ID": "507be385-e85b-44c6-9ede-7615652f4492", "leverancierID": "45e22d68-9632-42b9-83ad-6ff5a4e577b0", "link": "https://example.com/opvouwbare-toiletsteun", "naam": "Opvouwbare Toiletsteun", "prijs": 49.99, "imageBase64": None}, {"beschrijving": "Een steunbeugel die kan worden ge\u00efnstalleerd in de badkamer om extra ondersteuning en stabiliteit te bieden. Het heeft een roestvrijstalen constructie en een geribbeld oppervlak voor grip.", "ID": "f9820126-a81b-45f2-a7c9-a4304130a059", "leverancierID": "45e22d68-9632-42b9-83ad-6ff5a4e577b0", "link": "https://example.com/steunbeugel-badkamer", "naam": "Steunbeugel voor Badkamer", "prijs": 39.99, "imageBase64": None}, {"beschrijving": "Een comfortabele stoel die mensen helpt bij het opstaan en gaan zitten. Het heeft een elektrische liftfunctie verstelbare positie en zachte bekleding.", "ID": "6eb3e14c-83b1-42ba-a63f-352b6433ec3a", "leverancierID": "45e22d68-9632-42b9-83ad-6ff5a4e577b0", "link": "https://example.com/sta-op-stoel", "naam": "Sta-op Stoel", "prijs": 599.99, "imageBase64": None}, {"beschrijving": "Een gehoorbeschermer die het gehoor beschermt tegen harde geluiden en gehoorverlies voorkomt. Het is lichtgewicht verstelbaar en comfortabel om te dragen.", "ID": "0b1b9708-9711-404e-944d-01b3659f15d5", "leverancierID": "45e22d68-9632-42b9-83ad-6ff5a4e577b0", "link": "https://example.com/gehoorbeschermer", "naam": "Gehoorbeschermer", "prijs": 19.99, "imageBase64": None}]
        expected_products = [{"beschrijving":"Een gehoorbeschermer die het gehoor beschermt tegen harde geluiden en gehoorverlies voorkomt. Het is lichtgewicht verstelbaar en comfortabel om te dragen.","ID":"0b1b9708-9711-404e-944d-01b3659f15d5","leverancierID":"45e22d68-9632-42b9-83ad-6ff5a4e577b0","link":"https://example.com/gehoorbeschermer","naam":"Gehoorbeschermer","prijs":19.99,"imageBase64":None},{"beschrijving":"Een comfortabele stoel die mensen helpt bij het opstaan en gaan zitten. Het heeft een elektrische liftfunctie verstelbare positie en zachte bekleding.","ID":"6eb3e14c-83b1-42ba-a63f-352b6433ec3a","leverancierID":"45e22d68-9632-42b9-83ad-6ff5a4e577b0","link":"https://example.com/sta-op-stoel","naam":"Sta-op Stoel","prijs":599.99,"imageBase64":None},{"beschrijving":"Een steunbeugel die kan worden ge\u00efnstalleerd in de badkamer om extra ondersteuning en stabiliteit te bieden. Het heeft een roestvrijstalen constructie en een geribbeld oppervlak voor grip.","ID":"f9820126-a81b-45f2-a7c9-a4304130a059","leverancierID":"45e22d68-9632-42b9-83ad-6ff5a4e577b0","link":"https://example.com/steunbeugel-badkamer","naam":"Steunbeugel voor Badkamer","prijs":39.99,"imageBase64":None},{"beschrijving":"Een opvouwbare toiletsteun die extra stabiliteit biedt bij het opstaan en gaan zitten. Het is gemakkelijk op te bergen en heeft antislipvoeten voor veiligheid.","ID":"507be385-e85b-44c6-9ede-7615652f4492","leverancierID":"45e22d68-9632-42b9-83ad-6ff5a4e577b0","link":"https://example.com/opvouwbare-toiletsteun","naam":"Opvouwbare Toiletsteun","prijs":49.99,"imageBase64":None},{"beschrijving":"Een draadloze oplader die het mogelijk maakt om je telefoon draadloos op te laden. Het is compatibel met de meeste moderne smartphones en heeft een slank ontwerp.","ID":"be4f32d9-5843-4104-9f00-a8bfdf96f11e","leverancierID":"45e22d68-9632-42b9-83ad-6ff5a4e577b0","link":"https://example.com/draadloze-oplader","naam":"Draadloze Oplader","prijs":29.99,"imageBase64":None},{"beschrijving":"Een beveiligingscamera die je huis of kantoor bewaakt. Het heeft nachtzicht bewegingsdetectie en kan live videobeelden streamen naar je smartphone.","ID":"35fdf7f3-0296-4cce-b491-8080b2d16c19","leverancierID":"259a92a3-370a-4c57-a7c2-88c5c89d8dd8","link":"https://example.com/beveiligingscamera","naam":"Beveiligingscamera","prijs":129.99,"imageBase64":None}]
        for product in products:
            ProductModel(self._driver).create(product)

        # When
        products_response = self._test_client.get("/product/newest")

        # Cleanup
        for product in products:
            ProductModel(self._driver).delete(product["ID"])

        # Assert
        self.assertEqual(jsonify(expected_products).get_json(), products_response.get_json())
        

if __name__ == '__main__':
    unittest.main()