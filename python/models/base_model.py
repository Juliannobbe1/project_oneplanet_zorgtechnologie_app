import json
from flask import abort
import requests

class base_model: 
    def __init__(self, node_label, driver):
        self.label = node_label
        self.driver = driver
        self.model_data = {}
        
    def model(self):
        return self.model_data
    
    def extract(self, result): 
        data = [item['n'] for item in result.data()]
        if not data: 
            abort(404, "Item not found")
        else:
            return data
        
    def get_all(self):
        query = f"MATCH (n:{self.label}) RETURN n"
        with self.driver.session() as session:
            result = session.run(query)
            if result: 
                print(result)
                # Extract the data
                data = self.extract(result)
                return data
            else: 
                return abort(404, "Something went wrong")
        
    def get(self, property, value):
        with self.driver.session() as session:
            result = session.run(f"MATCH (n:{self.label}) WHERE n.{self.label}{property} = $value RETURN n", value=value)
            if result:
                data = self.extract(result)
                return data
            else:
                raise abort(404, "Something went wrong")
            
    def create(self, properties):
        query = f"MERGE (n:{self.label} {properties}) RETURN n"
        properties = json.dumps(properties)
        with self.driver.session() as session:
            result = session.run(query)
            if result:
                return json.dumps({"message": "Resource created successfully."})
            else:
                return abort(404, "Could not save")
            
    def delete(self, label, id):
        with self.driver.session() as session:
            result = session.run(f"MATCH (n:{label}) WHERE n.{label}ID = $id DETACH DELETE n", id=id)
            if result:
                return json.dumps({"message": "Resource deleted successfully."})
            else:
                return json.dumps({"message": "Could not delete resource"})
    
    def put(self, id, properties):
        with self.driver.session() as session:
            node_exists = session.run(f"MATCH (n:{self.label}) WHERE n.{self.label}ID = $id RETURN n", id=id).single()
            if not node_exists:
                return json.dumps({"message": "Resource not found."})
            result = session.run(f"MATCH (n:{self.label}) WHERE n.{self.label}ID = $id SET n += $properties RETURN n", id=id, properties=properties)
            if result:
                return json.dumps({"message": "Resource updated successfully."})
            else:
                return json.dumps({"message": "Could not update resource."})
            
    def setRelationship(self, start_id, end_id, relationship_type):
        query = f"MATCH (start:{self.label} {{ {self.label}ID: $start_id }}), (end:{self.label} {{ {self.label}ID: $end_id }}) CREATE (start)-[:{relationship_type}]->(end) RETURN start, end"
        with self.driver.session() as session:
            result = session.run(query, start_id=start_id, end_id=end_id)
            if result:
                return json.dumps({"message": "Relationship created successfully."})
            else:
                return json.dumps({"message": "Could not create relationship"})

    