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
        if value.isdigit():
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
        
    def get(self, property, value):
        with self.driver.session() as session:
            checkedValue = self.StringToIntCheck(value)
            result = session.run(f"MATCH (n:{self.label}) WHERE n.{property} = $value RETURN n", value=checkedValue)
            if result:
                data = self.extract(result, "n")
                return data
            else:
                raise abort(404, "Something went wrong")
            
    def create(self, property_list, value_list):
        
        query = "CREATE (n:`{}` {{".format(self.label)
        for i in range(len(property_list)):
            self.StringToIntCheck(value_list[i])
            query += '{}: "{}",'.format(property_list[i], value_list[i])
        query = query.rstrip(",") + "})"
        
        # properties = json.dumps(properties)
        with self.driver.session() as session:
            result = session.run(query)
            if result:
                return json.dumps({"message": "Resource created successfully."})
            else:
                return abort(404, "Could not save")
            
    def delete(self, property, value):
        with self.driver.session() as session:
            checkedValue = self.StringToIntCheck(value)
            result = session.run(f"MATCH (n:{self.label}) WHERE n.{property} = $value DETACH DELETE n", value=checkedValue)
            if result:
                return jsonify({"message": "Resource deleted successfully."}) 
            else:
                return abort(404, "Could not delete") 
    
            

    