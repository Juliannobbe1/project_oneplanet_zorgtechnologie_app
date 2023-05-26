from database.connect_database import database
import pandas as pd
import os

driver = database.connectDatabase()

path = "/Users/juliannobbe/Projects/flutter projects/project_oneplanet_zorgtechnologie_app/mockdata"
file_names = ["Leverancier v2.csv", "Organisatie v3.csv", "client v2.csv", "Zorgprofessional v2.csv", "verzorgd.csv", "contracten v2.csv", "Producten v2.csv", "review v2.csv", "toepassing v2.csv", "aanbeveling v2.csv"]
file_paths = [os.path.join(path, file_name) for file_name in file_names]
data = [pd.read_csv(file_path) for file_path in file_paths]

nodesqueries = {
    "product": "MERGE (:product {productNaam: $productNaam, productID: $productID, prijs: $prijs, beschrijving: $beschrijving, categorie: $categorie, link: $link, leverancierID: $leverancierID})",
    "toepassing": "MERGE (:toepassing {toepassingID: $toepassingID, productID: $productID, toepassing: $toepassing})",
    "review": "MERGE (:review {reviewID: $reviewID, beschrijving: $beschrijving, score: $score, datum: $datum, productID: $productID, zorgprofessionalID: $zorgprofessionalID})",
    "zorgprofessional": "MERGE (:zorgprofessional {zorgprofessionalID: $zorgprofessionalID, zorgprofessionalNaam: $zorgprofessionalNaam, email: $email, rol: $rol, organisatieID: $organisatieID})",
    "leverancier": "MERGE (:leverancier {leverancierID: $leverancierID, leverancierNaam: $leverancierNaam})",
    "organisatie": "MERGE (:organisatie {organisatieID: $organisatieID, organisatieNaam: $organisatieNaam})",
    "client": "MERGE (:client {clientID: $clientID, probleem: $probleem})",
    "aanbeveling": "MERGE (:aanbeveling {aanbevelingID: $aanbevelingID, aanbeveling: $aanbeveling, datum: $datum, productID: $productID, zorgprofessionalID: $zorgprofessionalID})"
}

relationshipqueries = {
    "HEEFT_TOEPASSING": """ 
    MATCH (a:product {productID: $productID}) 
    MATCH (b:toepassing {toepassingID: $toepassingID}) 
    MERGE (a)-[:HEEFT_TOEPASSING]->(b)
    """,
    
    "HEEFT_REVIEW": """ 
    MATCH (a:review {reviewID: $reviewID})
    MATCH (b:product {productID: $productID})
    MERGE (a)-[:OVER_PRODUCT]->(b) 
    """, 
    
    "GEEFT_REVIEW": """
    MATCH (a:zorgprofessional {zorgprofessionalID: $zorgprofessionalID})
    MATCH (b:review {reviewID: $reviewID})
    MERGE (a)-[:GEEFT_REVIEW]->(b)
    """,
    
    "VERZORGD_CLIENT": """
    MATCH (a:zorgprofessional {zorgprofessionalID: $zorgprofessionalID})
    MATCH (b:client {clientID: $clientID})
    MERGE (a)-[:VERZORGD_CLIENT]->(b)
    """, 
    
    "VAN_PRODUCT": """
    MATCH (a:aanbeveling {aanbevelingID: $aanbevelingID})
    MATCH (b:product {productID: $productID})
    MERGE (a)-[:VAN_PRODUCT]->(b)
    """,
    
    "GEEFT_AANBEVELING": """
    MATCH (a:zorgprofessional {zorgprofessionalID: $zorgprofessionalID})
    MATCH (b:aanbeveling {aanbevelingID: $aanbevelingID})
    MERGE (a)-[:GEEFT_AANBEVELING]->(b)
    """,
    
    "VERKOOPT_PRODUCT": """
    MATCH (a:leverancier {leverancierID: $leverancierID})
    MATCH (b:product {productID: $productID})
    MERGE (a)-[:VERKOOPT_PRODUCT]->(b)
    """,
    
    "WERKT_VOOR": """
    MATCH (a:zorgprofessional {zorgprofessionalID: $zorgprofessionalID})
    MATCH (b:organisatie {organisatieID: $organisatieID})
    MERGE (a)-[:WERKT_VOOR]->(b)
    """, 
    
    "HEEFT_CONTRACT_MET": """
    MATCH (a:organisatie {organisatieID: $organisatieID})
    MATCH (b:leverancier {leverancierID: $leverancierID})
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
        session.run(nodesqueries["product"], productNaam=row["productNaam"], productID=row["productID"], prijs=row["prijs"], beschrijving=row["beschrijving"], categorie=row["categorie"], link=row["link"], leverancierID=row["leverancierID"])
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
        session.run(nodesqueries["aanbeveling"], aanbevelingID=row["aanbevelingID"], aanbeveling=row["aanbeveling"], datum=pd.to_datetime(row['datum']).strftime('%Y-%m-%d'), productID=row["productID"], zorgprofessionalID=row["zorgprofessionalID"])
        # Create relationship
        session.run(relationshipqueries["VAN_PRODUCT"], aanbevelingID=row["aanbevelingID"], productID=row["productID"])
        session.run(relationshipqueries["GEEFT_AANBEVELING"], zorgprofessionalID=row["zorgprofessionalID"], aanbevelingID=row["aanbevelingID"])
        
