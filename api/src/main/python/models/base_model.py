from collections import Counter
import json
from flask import abort, jsonify
from loguru import logger

class base_model:
    def __init__(self, node_label, driver):
        self.label = node_label
        self.driver = driver
        self.model_data = {}

    def model(self):
        logger.trace("Retrieving model_data for '{label}'", label=self.label)
        return self.model_data

    def extract(self, result):
        logger.trace("Attempting data extraction for '{label}'", label=self.label)
        # Extracts 'n' from each item in the result data
        data = [item['n'] for item in result.data()]

        if not data:
            logger.error("Item not found while extracting result '{result}'", result=result)
            # Raises a 404 error if no data is found
            abort(404, "Item not found")
        else:
            logger.trace("Successfully extracted data from result for '{label}'", label=self.label)
            return data

    def StringToIntCheck(self, value):
        # Checks if the value is a string containing digits and converts it to an integer
        if isinstance(value, str) and value.isdigit():
            value = int(value)
            logger.trace("[StringToIntCheck] Value has been converted to int")
        logger.trace("[StringToIntCheck] Value was already int")
        return value

    def get_all(self):
        logger.trace("Attempting to retrieve all nodes with the specified label '{label}'", label=self.label)
        # Retrieves all nodes with the specified label
        query = f"MATCH (n:{self.label}) RETURN n"
        with self.driver.session() as session:
            result = session.run(query)
            if result:
                data = self.extract(result)
                logger.trace("Successfully retrieved all nodes with label '{label}'", label=self.label)
                return data
            else:
                # Raises a 404 error if something went wrong
                logger.error("Can't retrieve nodes with label '{label}'")
                return abort(404, "Something went wrong")

    def get(self, ID):
        logger.trace("Attempting to extract node with ID '{ID}'", ID=ID)
        with self.driver.session() as session:
            checkedValue = self.StringToIntCheck(ID)
            # Retrieves a node with the specified ID
            result = session.run(f"MATCH (n:{self.label}) WHERE n.ID = {checkedValue} RETURN n")
            if result:
                data = self.extract(result)
                logger.trace("Successfully extracted node with ID '{ID}' to '{data}'", ID=ID, data=data)
                return data
            else:
                # Raises a 404 error if something went wrong
                logger.error("Can't extract node with ID '{ID}'", ID=ID)
                return abort(404, "Something went wrong")

    def create(self, data):
        logger.trace("Attempting to create node with data '{data}'", data=data)
        # Creates a new node with the specified properties
        query = f"CREATE (n:`{self.label}` $props)"
        with self.driver.session() as session:
            result = session.run(query, props=data)
            if result:
                logger.trace("Node with data '{data}' created successfully", data=data)
                return json.dumps({"message": "Resource created successfully."})
            else:
                # Raises a 404 error if the resource could not be saved
                logger.error("Can't create node with data '{data}'", data=data)
                return abort(404, "Could not save")

    def update(self, data):
        logger.trace("Attempting to update node with data '{data}'", data=data)
        ID = data["ID"]
        counter = Counter(data)
        # Updates the properties of a node with the specified ID
        query = f"MATCH (n:{self.label}) WHERE n.ID = {int(ID)} SET "
        query += ', '.join([f'n.{key} = "{self.StringToIntCheck(value)}"' for key, value in counter.items()])
        query += " RETURN n"

        with self.driver.session() as session:
            result = session.run(query)
            if result:
                logger.trace("Node with data '{data}' updated successfully", data=data)
                return json.dumps({"message": "Resource updated successfully."})
            else:
                # Raises a 404 error if the resource could not be changed
                logger.error("Can't update node with data '{data}'")
                return abort(404, "Could not change")

    def delete(self, id):
        logger.trace("Attempting to delete node '{id}'", id=id)
        # Deletes a node with the specified ID
        query = f"MATCH (n:{self.label}) WHERE n.ID = '{id}' DETACH DELETE n"
        with self.driver.session() as session:
            result = session.run(query)
            if result:
                logger.trace("Successfully deleted node '{id}'", id=id)
                return jsonify({"message": "Resource deleted successfully."})
            else:
                # Raises a 404 error if the resource could not be deleted
                logger.error("Failed to delete node '{id}'", id=id)
                return abort(404, "Could not delete")
    