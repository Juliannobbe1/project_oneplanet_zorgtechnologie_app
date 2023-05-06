from flask import Flask, jsonify
from neo4j import GraphDatabase

app = Flask(__name__)

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

@app.route('/products')
def get_people():
    with driver.session() as session:
        result = session.run("MATCH (p:product) RETURN p.productNaam, p.productID, p.prijs, p.beschrijving, p.categorie, p.link, p.leverancierID")
        product = [record for record in result]
        return jsonify(product)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
