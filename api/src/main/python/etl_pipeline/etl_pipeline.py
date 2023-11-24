import re
import uuid
from flask import Flask, request, render_template
import pandas as pd
from neo4j import GraphDatabase
from handler.filehandler import FileHandler


app = Flask(__name__, template_folder='/Users/juliannobbe/Projects/flutter projects/project_oneplanet_zorgtechnologie_app/python/etl_pipeline/UI')

# Neo4j configuration
uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "iVOG0qvVg9iYYGz6WVf8BW19Xv4zmmHbDIkH0ur9PCU"))

class DataTransformation:
    def clean_data(df):
        """
        Clean and validate the given DataFrame.

        Args:
            df (pandas.DataFrame): The DataFrame to be cleaned.

        Returns:
            pandas.DataFrame: The cleaned DataFrame.
        """
        
        # Check if the required columns are present
        required_columns = ['naam', 'beschrijving']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

        # Remove rows with missing information in the required columns
        df.dropna(subset=required_columns, how='any', inplace=True)

        # Check if 'image' column values are in base64 format
        image_pattern = r'^[A-Za-z0-9+/=]+$'
        if 'image' in df.columns:
            df = df[df['image'].apply(lambda x: bool(re.match(image_pattern, str(x))))]

        # Check if 'prijs' column values use '.' as decimal separator instead of ','
        if 'prijs' in df.columns:
            if df['prijs'].dtype == 'str':
                df['prijs'] = df['prijs'].str.replace(',', '.').astype(float)

        # Check if column data types are correct
        df['naam'] = df['naam'].astype(str)
        if 'link' in df.columns:
            df['link'] = df['link'].astype(str)
        df['beschrijving'] = df['beschrijving'].astype(str)

        # Remove duplicates based on all columns
        df.drop_duplicates(keep='first', inplace=True)

        # Remove or replace unwanted characters and invalid characters
        df['naam'] = df['naam'].apply(lambda x: re.sub(r'[^\w\s]', '', x))
        df['beschrijving'] = df['beschrijving'].apply(lambda x: re.sub(r'[^\w\s]', '', x))
        
        with driver.session() as session:
            for index, row in df.iterrows():
                naam = row['naam']
                leverancier = row['leverancierID']
                
                # Query to check if data exists in the Neo4j database
                query = "MATCH (n:product{naam: $naam, leverancierID: $leverancier}) RETURN n.ID AS ID"
                result = session.run(query, naam=naam, leverancier=leverancier)
                data = result.data()
                if not data:
                    # Data doesn't exist, generate and add a new ID
                    df.at[index, 'ID'] = str(uuid.uuid4())
                    print("result is generate random UUID")
                elif 'ID' in data[0]:
                    # Data exists, retrieve the ID and add it to the DataFrame
                    df.at[index, 'ID'] = data[0]['ID']
                    print("result is single")
                    
        # Close the Neo4j driver
        driver.close()

        return df


# Route for file upload via the website
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            df = FileHandler().process_file(file)
            df['leverancierID'] = 'b53385d9-b5d9-40f7-a6ec-abfb94950f24'
            clean_df = DataTransformation.clean_data(df)
            
            """ load into database """

            # Retrieve columns and convert to dictionaries
            naam_column = clean_df.get("naam").to_dict()  # required
            beschrijving_column = clean_df.get("beschrijving").to_dict()  # required
            prijs_column = clean_df.get("prijs").to_dict() if "prijs" in clean_df else [{}]
            link_column = clean_df.get("link").to_dict() if "link" in clean_df else [{}]
            ID_column = clean_df.get("ID").to_dict() if "ID" in clean_df else [{}]

            # Create attributes dictionary
            attributes = {"naam": naam_column, "beschrijving": beschrijving_column, "prijs": prijs_column, "link": link_column, "ID": ID_column, "leverancierID": clean_df['leverancierID']}

            # Iterate over the range of the length of the values in the first attribute
            for i in range(len(list(attributes.values())[0])):
                valid_attributes = {}
                for k, v in attributes.items():
                    # Check if the value is not None, the index 'i' is present in the value, and the value at index 'i' is not None
                    if v is not None and i in v and v[i] is not None:
                        valid_attributes[k] = v[i]
                if valid_attributes:
                    with driver.session() as session:
                        # Check if a node with the specified 'ID' already exists
                        query = "MATCH (n:product {ID: $ID}) RETURN n"
                        result = session.run(query, ID=valid_attributes["ID"])
                        if result.single() is None:
                            # If node doesn't exist, create it and set its properties
                            query = "CREATE (n:product) SET n = $attributes"
                            session.run(query, attributes=valid_attributes)
                        else:
                            query = "MATCH (n:product {ID: $ID}) SET n = $attributes"
                            result = session.run(query, ID=valid_attributes["ID"], attributes=valid_attributes)
                            
                    message = "De data is succesvol opgeslagen in de database"

            return message

    return render_template('upload.html')

if __name__ == '__main__':
    app.run()
