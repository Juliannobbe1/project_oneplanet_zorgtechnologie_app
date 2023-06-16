from collections import Counter
import json
from flask import abort, jsonify

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
        
    def StringToIntCheck(self, value):
        if isinstance(value, str) and value.isdigit():
            value = int(value)
        return value
        
    def get_all(self):
        query = f"MATCH (n:{self.label}) RETURN n"
        with self.driver.session() as session:
            result = session.run(query)
            if result: 
                data = self.extract(result)
                return data
            else: 
                return abort(404, "Something went wrong")
        
    def get(self, ID):
        with self.driver.session() as session:
            checkedValue = self.StringToIntCheck(ID)
            print("checkedValue: ", checkedValue)
            result = session.run(f"MATCH (n:{self.label}) WHERE n.ID = {checkedValue} RETURN n")
            if result:
                data = self.extract(result)
                return data
            else:
                raise abort(404, "Something went wrong")
            
    def create(self, data):
        query = f"CREATE (n:`{self.label}` $props)"
        with self.driver.session() as session:
            result = session.run(query, props=data)
            if result:
                return json.dumps({"message": "Resource created successfully."})
            else:
                return abort(404, "Could not save")
            
    def update(self,data):
        ID = data["ID"]
        # checkedID = self.StringToIntCheck(ID)
        counter = Counter(data)
        query = f"MATCH (n:{self.label}) WHERE n.ID = {int(ID)} SET "
        query += ', '.join([f'n.{key} = "{self.StringToIntCheck(value)}"' for key, value in counter.items()])
        query += " RETURN n"
            
        with self.driver.session() as session: 
            result = session.run(query)
            if result:
                return json.dumps({"message": "Resource updated successfully."})
            else:
                return abort(404, "Could not change")

            
    def delete(self, id):
        checkedId = self.StringToIntCheck(id)
        query = f"MATCH (n:{self.label}) WHERE n.ID = {checkedId} DELETE n"
        print("query:", query)
        with self.driver.session() as session:
            result = session.run(query)
            if result:
                return jsonify({"message": "Resource deleted successfully."}) 
            else:
                return abort(404, "Could not delete") 
    
    
    # {ID: 61, probleem: Verwarring en desoriëntatie}