# Import necessary libraries
from python.database.connect_database import Database
import pandas as pd
import os

# Connect to the database
driver = Database.connectDatabase()

# Set up file paths
path = "mockdata"
file_names = ["Leverancier v2.csv", "Organisatie v3.csv", "client v3.csv", "Zorgprofessional v2.csv",
              "verzorgd v2.csv", "contracten v2.csv", "Producten v2.csv", "review v2.csv",
              "toepassing v3.csv", "aanbeveling v3.csv"]
file_paths = [os.path.join(path, file_name) for file_name in file_names]

# Read data from CSV files
data = [pd.read_csv(file_path) for file_path in file_paths]

# Define queries for creating nodes in the database
nodesqueries = {
    "product": "MERGE (p:product {ID: $productID, naam: $naam, prijs: $prijs, beschrijving: $beschrijving, link: $link, leverancierID: $leverancierID}) ON CREATE SET p.ID = $productID",
    "toepassing": "MERGE (t:toepassing {ID: $toepassingID, productID: $productID, toepassing: $toepassing}) ON CREATE SET t.ID = $toepassingID",
    "review": "MERGE (r:review {ID: $reviewID, beschrijving: $beschrijving, score: $score, datum: $datum, productID: $productID, zorgprofessionalID: $zorgprofessionalID}) ON CREATE SET r.ID = $reviewID",
    "zorgprofessional": "MERGE (z:zorgprofessional {ID: $zorgprofessionalID,  naam: $zorgprofessionalNaam, email: $email, rol: $rol, organisatieID: $organisatieID}) ON CREATE SET z.ID = $zorgprofessionalID",
    "leverancier": "MERGE (l:leverancier {ID: $leverancierID, naam: $leverancierNaam}) ON CREATE SET l.ID = $leverancierID",
    "organisatie": "MERGE (o:organisatie {ID: $organisatieID, naam: $organisatieNaam}) ON CREATE SET o.ID = $organisatieID",
    "client": "MERGE (c:client {ID: $clientID, probleem: $probleem}) ON CREATE SET c.ID = $clientID",
}

# Define queries for creating relationships between nodes in the database
relationshipqueries = {
    "HEEFT_TOEPASSING": """
    MATCH (a:product {ID: $productID})
    MATCH (b:toepassing {ID: $toepassingID})
    MERGE (a)-[:HEEFT_TOEPASSING]->(b)
    """,
    "HEEFT_REVIEW": """
    MATCH (a:review {ID: $reviewID})
    MATCH (b:product {ID: $productID})
    MERGE (a)-[:OVER_PRODUCT]->(b)
    """,
    "GEEFT_REVIEW": """
    MATCH (a:zorgprofessional {ID: $zorgprofessionalID})
    MATCH (b:review {ID: $reviewID})
    MERGE (a)-[:GEEFT_REVIEW]->(b)
    """,
    "VERZORGD_CLIENT": """
    MATCH (a:zorgprofessional {ID: $zorgprofessionalID})
    MATCH (b:client {ID: $clientID})
    MERGE (a)-[:VERZORGD_CLIENT]->(b)
    """,
    "VAN_PRODUCT": """
    MATCH (a:aanbeveling {ID: $aanbevelingID})
    MATCH (b:product {ID: $productID})
    MERGE (a)-[:VAN_PRODUCT]->(b)
    """,
    "KRIJGT_AANBEVELING": """
    MATCH (a:zorgprofessional {ID: $zorgprofessionalID})
    MATCH (b:product {ID: $productID})
    MERGE (a)-[:KRIJGT_AANBEVELING {aanbevelingID:$aanbevelingID,zorgprofessionalID:$zorgprofessionalID,clientID:$clientID,productID:$productID}]->(b)
    """,
    "VERKOOPT_PRODUCT": """
    MATCH (a:leverancier {ID: $leverancierID})
    MATCH (b:product {ID: $productID})
    MERGE (a)-[:VERKOOPT_PRODUCT]->(b)
    """,
    "WERKT_VOOR": """
    MATCH (a:zorgprofessional {ID: $zorgprofessionalID})
    MATCH (b:organisatie {ID: $organisatieID})
    MERGE (a)-[:WERKT_VOOR]->(b)
    """,
    "HEEFT_CONTRACT_MET": """
    MATCH (a:organisatie {ID: $organisatieID})
    MATCH (b:leverancier {ID: $leverancierID})
    MERGE (a)-[:HEEFT_CONTRACT_MET]->(b)
    """
}

# Start a session with the database
with driver.session() as session:
    # Create nodes for "organisatie" from data[1]
    for index, row in data[1].iterrows():
        session.run(nodesqueries["organisatie"], organisatieID=row["organisatieID"], organisatieNaam=row["organisatieNaam"])
    
    # Create nodes for "leverancier" from data[0]
    for index, row in data[0].iterrows():
        session.run(nodesqueries["leverancier"], leverancierID=row["leverancierID"], leverancierNaam=row["leverancierNaam"])
    
    # Create nodes for "client" from data[2]
    for index, row in data[2].iterrows():
        session.run(nodesqueries["client"], clientID=row["clientID"], probleem=row["probleem"])
    
    # Create nodes and relationships for "zorgprofessional" from data[3]
    for index, row in data[3].iterrows():
        session.run(nodesqueries["zorgprofessional"], zorgprofessionalID=row["zorgprofessionalID"],
                    zorgprofessionalNaam=row["zorgprofessionalNaam"], email=row["email"], rol=row["rol"],
                    organisatieID=row["organisatieID"])
        session.run(relationshipqueries["WERKT_VOOR"], zorgprofessionalID=row["zorgprofessionalID"],
                    organisatieID=row["organisatieID"])
    
    # Create relationships for "verzorgd" from data[4]
    for index, row in data[4].iterrows():
        session.run(relationshipqueries["VERZORGD_CLIENT"], zorgprofessionalID=row["zorgprofessionalID"],
                    clientID=row["clientID"])
    
    # Create nodes and relationships for "product" from data[6]
    for index, row in data[6].iterrows():
        session.run(nodesqueries["product"], naam=row["naam"], productID=row["productID"], prijs=row["prijs"],
                    beschrijving=row["beschrijving"], link=row["link"], leverancierID=row["leverancierID"])
        session.run(relationshipqueries["VERKOOPT_PRODUCT"], leverancierID=row["leverancierID"],
                    productID=row["productID"])
    
    # Create nodes and relationships for "review" from data[7]
    for index, row in data[7].iterrows():
        session.run(nodesqueries["review"], reviewID=row["reviewID"], beschrijving=row["beschrijving"],
                    score=row["score"], datum=pd.to_datetime(row['datum']).strftime('%Y-%m-%d'),
                    productID=row["productID"], zorgprofessionalID=row["zorgprofessionalID"])
        session.run(relationshipqueries["HEEFT_REVIEW"], reviewID=row["reviewID"], productID=row["productID"])
        session.run(relationshipqueries["GEEFT_REVIEW"], zorgprofessionalID=row["zorgprofessionalID"],
                    reviewID=row["reviewID"])
    
    # Create nodes and relationships for "toepassing" from data[8]
    for index, row in data[8].iterrows():
        session.run(nodesqueries["toepassing"], toepassingID=row["toepassingID"], productID=row["productID"],
                    toepassing=row["toepassing"])
        session.run(relationshipqueries["HEEFT_TOEPASSING"], productID=row["productID"],
                    toepassingID=row["toepassingID"])
    
    # Create relationships for "aanbeveling" from data[9]
    for index, row in data[9].iterrows():
        session.run(relationshipqueries["KRIJGT_AANBEVELING"], aanbevelingID=row["aanbevelingID"], zorgprofessionalID=row["zorgprofessionalID"],
                    productID=row["productID"], clientID=row["clientID"])
