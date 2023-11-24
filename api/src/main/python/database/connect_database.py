from neo4j import GraphDatabase
from loguru import logger

class Database:
    def connectDatabase():
        # Establish a connection to the Neo4j database using the Bolt protocol
        logger.trace("Attempting to establish connection with Neo4J database on 'bolt://localhost:7687'")
        driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "iVOG0qvVg9iYYGz6WVf8BW19Xv4zmmHbDIkH0ur9PCU"))
        logger.trace("Connection established with Neo4J database on 'bolt://localhost:7687'")
        return driver
