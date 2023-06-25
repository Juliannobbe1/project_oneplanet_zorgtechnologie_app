from collections import Counter
import json
from flask import abort, jsonify

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
        # Extracts 'n' from each item in the result data
        data = [item['n'] for item in result.data()]

        if not data:
            # Raises a 404 error if no data is found
            abort(404, "Item not found")
        else:
            return data

    def StringToIntCheck(self, value):
        # Checks if the value is a string containing digits and converts it to an integer
        if isinstance(value, str) and value.isdigit():
            value = int(value)
        return value

    def get_all(self):
        # Retrieves all nodes with the specified label
        query = f"MATCH (n:{self.label}) RETURN n"
        with self.driver.session() as session:
            result = session.run(query)
            if result:
                data = self.extract(result)
                return data
            else:
                # Raises a 404 error if something went wrong
                return abort(404, "Something went wrong")

    def get(self, ID):
        with self.driver.session() as session:
            checkedValue = self.StringToIntCheck(ID)
            print("checkedValue: ", checkedValue)
            # Retrieves a node with the specified ID
            result = session.run(f"MATCH (n:{self.label}) WHERE n.ID = {checkedValue} RETURN n")
            if result:
                data = self.extract(result)
                return data
            else:
                # Raises a 404 error if something went wrong
                raise abort(404, "Something went wrong")

    def create(self, data):
        # Creates a new node with the specified properties
        query = f"CREATE (n:`{self.label}` $props)"
        with self.driver.session() as session:
            result = session.run(query, props=data)
            if result:
                return json.dumps({"message": "Resource created successfully."})
            else:
                # Raises a 404 error if the resource could not be saved
                return abort(404, "Could not save")

    def update(self, data):
        ID = data["ID"]
        # checkedID = self.StringToIntCheck(ID)
        counter = Counter(data)
        # Updates the properties of a node with the specified ID
        query = f"MATCH (n:{self.label}) WHERE n.ID = {int(ID)} SET "
        query += ', '.join([f'n.{key} = "{self.StringToIntCheck(value)}"' for key, value in counter.items()])
        query += " RETURN n"

        with self.driver.session() as session:
            result = session.run(query)
            if result:
                return json.dumps({"message": "Resource updated successfully."})
            else:
                # Raises a 404 error if the resource could not be changed
                return abort(404, "Could not change")

    def delete(self, id):
        # Deletes a node with the specified ID
        query = f"MATCH (n:{self.label}) WHERE n.ID = '{id}' DETACH DELETE n"
        print("query:", query)
        with self.driver.session() as session:
            result = session.run(query)
            if result:
                return jsonify({"message": "Resource deleted successfully."})
            else:
                # Raises a 404 error if the resource could not be deleted
                return abort(404, "Could not delete")
    