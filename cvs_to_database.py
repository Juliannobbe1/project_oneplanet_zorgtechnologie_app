from connect_database import database
import pandas as pd

driver = database.connectDatabase()

path = "/Users/juliannobbe/Library/CloudStorage/OneDrive-Chr.HogeschoolEde/School/Hbo-ICT/Jaar 3/Sem 6 - oneplanet zorgtechnologie app/Data/cvs/"

# Read the CSV file into a DataFrame
product_data = pd.read_csv(path+"Producten v2.csv")
toepassing_data = pd.read_csv(path+"toepassing v2.csv")
review_data = pd.read_csv(path+"review v2.csv")
zorgprofessional_data = pd.read_csv(path+"Zorgprofessional v2.csv")
leverancier_data = pd.read_csv(path+"Leverancier v2.csv")
organisatie_data = pd.read_csv(path+"Organisatie v2.csv")
client_data = pd.read_csv(path+"client v2.csv")
verzorgd_data = pd.read_csv(path+"verzorgd.csv")
aanbeveling_data = pd.read_csv(path+"aanbeveling v2.csv")
contracten_data = pd.read_csv(path+"contracten v2.csv")

# Define the Cypher query to create nodes
create_product_node_query = "CREATE (:product {productNaam: $productNaam, productID: $productID, prijs: $prijs, beschrijving: $beschrijving, categorie: $categorie, link: $link, leverancierID: $leverancierID})"
create_toepassing_node_query = "CREATE (:toepassing {toepassinID: $toepassinID, productID: $productID, toepassing: $toepassing})"
create_review_node_query = "CREATE (:review {reviewID: $reviewID, beschrijving: $beschrijving, score: $score, datum: $datum, productID: $productID, zorgprofessionalID: $zorgprofessionalID})"
create_zorgprofessional_node_query = "CREATE (:zorgprofessional {zorgprofessionalID: $zorgprofessionalID, zorgprofessionalNaam: $zorgprofessionalNaam, email: $email, rol: $rol, organisatieID: $organisatieID})"
create_leverancier_node_query = "CREATE (:leverancier {leverancierID: $leverancierID, leverancierNaam: $leverancierNaam})"
create_organisatie_node_query = "CREATE (:organisatie {organisatieID: $organisatieID, organisatieNaam: $organisatieNaam})"
create_client_node_query = "CREATE (:client {clientID: $clientID, probleem: $probleem})"
create_verzorgd_node_query = "CREATE (:verzorgd {zorgprofessionalID: $zorgprofessionalID, clientID: $clientID})"
create_aanbeveling_node_query = "CREATE (:aanbeveling {aanbevelingID: $aanbevelingID, aanbeveling: $aanbeveling, datum: $datum, productID: $productID, zorgprofessionalID: $zorgprofessionalID})"
create_contracten_node_query = "CREATE (:review {leverancierID: $leverancierID, organisatieID: $organisatieID})"

# Define the Cypher query to create relationships
create_relationship_heefttoepassing_query = """
MATCH (a:product {productID: $productID})
MATCH (b:toepassing {toepassinID: $toepassinID})
CREATE (a)-[:HEEFT_TOEPASSING]->(b)
"""

create_relationship_heeftreview_query = """
MATCH (a:review {reviewID: $reviewID})
MATCH (b:product {productID: $productID})
CREATE (a)-[:OVER_PRODUCT]->(b)
"""

create_relationship_geeftreview_query = """
MATCH (a:zorgprofessional {zorgprofessionalID: $zorgprofessionalID})
MATCH (b:review {reviewID: $reviewID})
CREATE (a)-[:GEEFT_REVIEW]->(b)
"""

create_relationship_verzorgdclient_query = """
MATCH (a:zorgprofessional {zorgprofessionalID: $zorgprofessionalID})
MATCH (b:client {clientID: $clientID})
CREATE (a)-[:VERZORGD_CLIENT]->(b)
"""

create_relationship_vanproduct_query = """
MATCH (a:aanbeveling {aanbevelingID: $aanbevelingID})
MATCH (b:product {productID: $productID})
CREATE (a)-[:VAN_PRODUCT]->(b)
"""

create_relationship_geeftaanbeveling_query = """
MATCH (a:zorgprofessional {zorgprofessionalID: $zorgprofessionalID})
MATCH (b:aanbeveling {aanbevelingID: $aanbevelingID})
CREATE (a)-[:GEEFT_AANBEVELING]->(b)
"""

create_relationship_verkooptproduct_query = """
MATCH (a:leverancier {leverancierID: $leverancierID})
MATCH (b:product {productID: $productID})
CREATE (a)-[:VERKOOPT_PRODUCT]->(b)
"""

create_relationship_werktvoor_query = """
MATCH (a:zorgprofessional {zorgprofessionalID: $zorgprofessionalID})
MATCH (b:organisatie {organisatieID: $organisatieID})
CREATE (a)-[:WERKT_VOOR]->(b)
"""

create_relationship_heeftcontractmet_query = """
MATCH (a:organisatie {organisatieID: $organisatieID})
MATCH (b:leverancier {leverancierID: $leverancierID})
CREATE (a)-[:HEEFT_CONTRACT_MET]->(b)
"""

# # Loop through the data and create nodes and relationships
# with driver.session() as session:
#     for index, row in data.iterrows():
#         # Create nodes
#         session.run(create_node_query, name=row["name"])
        
#         # Create relationships
#         session.run(create_relationship_query, from_name=row["from_name"], to_name=row["to_name"])
