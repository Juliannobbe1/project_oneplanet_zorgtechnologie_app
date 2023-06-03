from connect_database import database
import pandas as pd
import os

driver = database.connectDatabase()

path = "/Users/juliannobbe/Projects/flutter projects/project_oneplanet_zorgtechnologie_app/mockdata"
file_names = ["Leverancier v2.csv", "Organisatie v3.csv", "client v3.csv", "Zorgprofessional v2.csv", "verzorgd v2.csv", "contracten v2.csv", "Producten v2.csv", "review v2.csv", "toepassing v3.csv", "aanbeveling v3.csv"]
file_paths = [os.path.join(path, file_name) for file_name in file_names]
data = [pd.read_csv(file_path) for file_path in file_paths]

nodesqueries = {
    "product": "MERGE (p:product {ID: $productID, naam: $productNaam, prijs: $prijs, beschrijving: $beschrijving, link: $link, leverancierID: $leverancierID}) ON CREATE SET p.ID = $productID",
    "toepassing": "MERGE (t:toepassing {ID: $toepassingID, productID: $productID, toepassing: $toepassing}) ON CREATE SET t.ID = $toepassingID",
    "review": "MERGE (r:review {ID: $reviewID, beschrijving: $beschrijving, score: $score, datum: $datum, productID: $productID, zorgprofessionalID: $zorgprofessionalID}) ON CREATE SET r.ID = $reviewID",
    "zorgprofessional": "MERGE (z:zorgprofessional {ID: $zorgprofessionalID,  naam: $zorgprofessionalNaam, email: $email, rol: $rol, organisatieID: $organisatieID}) ON CREATE SET z.ID = $zorgprofessionalID",
    "leverancier": "MERGE (l:leverancier {ID: $leverancierID, naam: $leverancierNaam}) ON CREATE SET l.ID = $leverancierID",
    "organisatie": "MERGE (o:organisatie {ID: $organisatieID, naam: $organisatieNaam}) ON CREATE SET o.ID = $organisatieID",
    "client": "MERGE (c:client {ID: $clientID, probleem: $probleem}) ON CREATE SET c.ID = $clientID",
    # "aanbeveling": "MERGE (a:aanbeveling {ID: $aanbevelingID, aanbeveling: $aanbeveling, datum: $datum, productID: $productID, zorgprofessionalID: $zorgprofessionalID}) ON CREATE SET a.ID = $aanbevelingID"
}

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
    MERGE (a)-[:KRIJGT_AANBEVELING {zorgprofessionalID:$zorgprofessionalID,clientID:$clientID,productID:$productID}]->(b)
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
# for label, query in queries.items():
#     session.run(query)

with driver.session() as session:
    for index, row in data[1].iterrows():
        # Create nodes
        session.run(nodesqueries["organisatie"], organisatieID=row["organisatieID"], organisatieNaam=row["organisatieNaam"])
    # leverancier
    for index, row in data[0].iterrows():
        # Create nodes
        session.run(nodesqueries["leverancier"], leverancierID=row["leverancierID"], leverancierNaam=row["leverancierNaam"])
        
    for index, row in data[2].iterrows():
        # Create nodes
        session.run(nodesqueries["client"], clientID=row["clientID"], probleem=row["probleem"])
        
    # zorgprofessional
    for index, row in data[3].iterrows():
        # Create nodes
        session.run(nodesqueries["zorgprofessional"], zorgprofessionalID=row["zorgprofessionalID"], zorgprofessionalNaam=row["zorgprofessionalNaam"], email=row["email"], rol=row["rol"], organisatieID=row["organisatieID"])
        # Create relationship
        session.run(relationshipqueries["WERKT_VOOR"] , zorgprofessionalID=row["zorgprofessionalID"], organisatieID=row["organisatieID"])
        
    for index, row in data[4].iterrows():
        # Create relationship
        session.run(relationshipqueries["VERZORGD_CLIENT"], zorgprofessionalID=row["zorgprofessionalID"], clientID=row["clientID"])
        
    for index, row in data[5].iterrows():
        # Create relationship
        session.run(relationshipqueries["HEEFT_CONTRACT_MET"], leverancierID=row["leverancierID"], organisatieID=row["organisatieID"] ) 
        
    # Product
    for index, row in data[6].iterrows():
        # Create nodes
        session.run(nodesqueries["product"], productNaam=row["productNaam"], productID=row["productID"], prijs=row["prijs"], beschrijving=row["beschrijving"], link=row["link"], leverancierID=row["leverancierID"])
        # Create relationship
        session.run(relationshipqueries["VERKOOPT_PRODUCT"], leverancierID=row["leverancierID"], productID=row["productID"]) 
    
    # review 
    for index, row in data[7].iterrows():
        # Create nodes
        session.run(nodesqueries["review"], reviewID=row["reviewID"], beschrijving=row["beschrijving"], score=row["score"], datum=pd.to_datetime(row['datum']).strftime('%Y-%m-%d'), productID=row["productID"], zorgprofessionalID=row["zorgprofessionalID"])
        #create relationship
        session.run(relationshipqueries["HEEFT_REVIEW"], reviewID=row["reviewID"], productID=row["productID"])
        session.run(relationshipqueries["GEEFT_REVIEW"], zorgprofessionalID=row["zorgprofessionalID"], reviewID=row["reviewID"])
        
    # toepassing
    for index, row in data[8].iterrows():
        # Create nodes
        session.run(nodesqueries["toepassing"], toepassingID=row["toepassingID"], productID=row["productID"], toepassing=row["toepassing"])
        #Create relationships
        session.run(relationshipqueries["HEEFT_TOEPASSING"], productID=row["productID"], toepassingID=row["toepassingID"])
    
    # aanbeveling
    for index, row in data[9].iterrows():
        # Create nodes
        # session.run(nodesqueries["aanbeveling"], aanbevelingID=row["aanbevelingID"], productID=row["productID"], zorgprofessionalID=row["zorgprofessionalID"])
        # Create relationship
        # session.run(relationshipqueries["VAN_PRODUCT"], aanbevelingID=row["aanbevelingID"], productID=row["productID"])
        session.run(relationshipqueries["KRIJGT_AANBEVELING"], zorgprofessionalID=row["zorgprofessionalID"], productID=row["productID"], clientID=row["clientID"])
        
