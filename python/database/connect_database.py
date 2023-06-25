from neo4j import GraphDatabase

class Database:
    def connectDatabase():
        # Establish a connection to the Neo4j database using the Bolt protocol
        driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "iVOG0qvVg9iYYGz6WVf8BW19Xv4zmmHbDIkH0ur9PCU"))
        return driver
