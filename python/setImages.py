import os
import base64
from database.connect_database import database

# Function to retrieve the image file names in the specified folder
def get_image_files(folder_path):
    image_files = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.jpg'):
            image_files.append(filename)
    return sorted(image_files, key=lambda x: int(x.split('.')[0]))

# Function to encode an image file as base64
def encode_image_to_base64(image_path):
    with open(image_path, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

driver = database.connectDatabase()

# Folder path containing the images
image_folder_path = '/Users/juliannobbe/Projects/flutter projects/project_oneplanet_zorgtechnologie_app/Afbeeldingen Zorgtechnologiëen/'

# Connect to the Neo4j database
# driver = GraphDatabase.driver(uri, auth=(username, password))

# Retrieve the image files in the folder
image_files = get_image_files(image_folder_path)

# Ensure the number of image files matches the number of products
if len(image_files) != 50:
    print("Number of image files does not match the number of products: ", len(image_files))
else:
    # Update the image paths for the products in Neo4j
    with driver.session() as session:
        for i in range(len(image_files)):
            product_id = i + 1  # Assuming product IDs start from 1
            image_path = os.path.join(image_folder_path, image_files[i])
            base64_image = encode_image_to_base64(image_path)
            query = f"MATCH (p:product {{ID: {product_id}}}) SET p.imageBase64 = '{base64_image}'"
            session.run(query)

# Close the Neo4j driver
driver.close()
