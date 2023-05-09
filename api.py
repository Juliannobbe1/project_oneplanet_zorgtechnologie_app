from flask import Flask
from neo4j import GraphDatabase
import json

app = Flask(__name__)

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "iVOG0qvVg9iYYGz6WVf8BW19Xv4zmmHbDIkH0ur9PCU"))

@app.route('/products')
def get_products():
    with driver.session() as session:
        result = session.run("MATCH (p:product) RETURN p.productNaam as productNaam, p.productID as productID, p.prijs as prijs,p.beschrijving as beschrijving,p.categorie as categorie,p.link as link, p.leverancierID as leverancierID")
        # product = [record for record in result]
        json_data = json.dumps(result.data())
        return json_data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

