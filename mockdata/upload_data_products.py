from neo4j import GraphDatabase
import pandas as pd
import os

# Neo4j database connection settings
uri = "bolt://localhost:7687"  # Update with your Neo4j server URI
username = "neo4j"
password = "iVOG0qvVg9iYYGz6WVf8BW19Xv4zmmHbDIkH0ur9PCU"

# CSV file path
path = "mockdata"
file_names = ["ddg-products.csv", "ddg-aanbeveling.csv", "ddg-client.csv", "ddg-zorgprofesional.csv", "ddg-verzorgd.csv" ]
csv_file_path = "mockdata/ddg-products.csv"

file_paths = [os.path.join(path, file_name) for file_name in file_names]

df = [pd.read_csv(file_path, delimiter=';') for file_path in file_paths]


# Neo4j queries
merge_product_node_query = """
    MERGE (p:product {ID: $id})
    ON CREATE SET p.naam = $name, p.beschrijving = $description, p.imageBase64 = $imageBase64
"""

merge_zorgprofessional_node_query = """
    MERGE (z:zorgprofessional {ID: $zorgprofessionalID,  naam: $zorgprofessionalNaam, email: $email, rol: $rol}) 
    ON CREATE SET z.ID = $zorgprofessionalID
"""

merge_client_node_query = """
    MERGE (c:client {ID: $clientID}) 
    ON CREATE SET c.ID = $clientID, c.probleem = $probleem
"""

create_relationship_verzorgd_client_query = """
    MATCH (a:zorgprofessional {ID: $zorgprofessionalID})
    MATCH (b:client {ID: $clientID})
    MERGE (a)-[:VERZORGD_CLIENT]->(b)
"""

create_relationship_van_product_query = """
    MATCH (a:aanbeveling {ID: $aanbevelingID})
    MATCH (b:product {ID: $productID})
    MERGE (a)-[:VAN_PRODUCT]->(b)
"""

create_relationship_krijgt_aanbeveling_query = """
    MATCH (a:zorgprofessional {ID: $zorgprofessionalID})
    MATCH (b:product {ID: $productID})
    MERGE (a)-[:KRIJGT_AANBEVELING {aanbevelingID:$aanbevelingID,zorgprofessionalID:$zorgprofessionalID,clientID:$clientID,productID:$productID}]->(b)
"""


# Function to merge product node in Neo4j
def merge_product_node(tx, id, name, description, imageBase64):
    tx.run(merge_product_node_query, id=id, name=name, description=description, imageBase64=imageBase64)

# Function to merge zorgprofessional node in Neo4j
def merge_zorgprofessional_node(tx, zorgprofessionalID, zorgprofessionalNaam, email, rol):
    tx.run(merge_zorgprofessional_node_query, zorgprofessionalID=zorgprofessionalID, zorgprofessionalNaam=zorgprofessionalNaam, email=email, rol=rol)

# Function to merge client node in Neo4j
def merge_client_node(tx, clientID, probleem):
    tx.run(merge_client_node_query, clientID=clientID, probleem=probleem)

# Function to create VERZORGD_CLIENT relationship in Neo4j
def create_relationship_verzorgd_client(tx, zorgprofessionalID, clientID):
    tx.run(create_relationship_verzorgd_client_query, zorgprofessionalID=zorgprofessionalID, clientID=clientID)

# Function to create VAN_PRODUCT relationship in Neo4j
def create_relationship_van_product(tx, aanbevelingID, productID):
    tx.run(create_relationship_van_product_query, aanbevelingID=aanbevelingID, productID=productID)

# Function to create KRIJGT_AANBEVELING relationship in Neo4j
def create_relationship_krijgt_aanbeveling(tx, zorgprofessionalID, clientID, productID, aanbevelingID):
    tx.run(create_relationship_krijgt_aanbeveling_query, zorgprofessionalID=zorgprofessionalID, clientID=clientID, productID=productID, aanbevelingID=aanbevelingID)

# Connect to Neo4j
driver = GraphDatabase.driver(uri, auth=(username, password))

# Merge client nodes in Neo4j
#! 1
with driver.session() as session:
    for index, row in df[2].iterrows():
        session.write_transaction(merge_client_node, row['clientID'], row['probleem'])
        
# Merge zorgprofessional nodes in Neo4j
#! 2
with driver.session() as session:
    for index, row in df[3].iterrows():
        session.write_transaction(merge_zorgprofessional_node, row['zorgprofessionalID'], row['zorgprofessionalNaam'], row['email'], row['rol'])

# Merge product nodes in Neo4j
#! 4
with driver.session() as session:
    for index, row in df[0].iterrows():
        session.write_transaction(merge_product_node, row['ID'], row['naam'], row['beschrijving'], row['imageBase64'])

# Create KRIJGT_AANBEVELING relationships in Neo4j
#! 5
with driver.session() as session:
    for index, row in df[1].iterrows():
        session.write_transaction(create_relationship_krijgt_aanbeveling, row['zorgprofessionalID'], row['clientID'], row['productID'], row['aanbevelingID'])
        
# Create VERZORGD_CLIENT relationships in Neo4j
#! 3
with driver.session() as session:
    for index, row in df[4].iterrows():
        session.write_transaction(create_relationship_verzorgd_client, row['zorgprofessionalID'], row['clientID'])

# # Create VAN_PRODUCT relationships in Neo4j
# with driver.session() as session:
#     for index, row in df[1].iterrows():
#         session.write_transaction(create_relationship_van_product, row['aanbevelingID'], row['productID'])


# Close Neo4j connection
driver.close()

