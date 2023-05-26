from neo4j import GraphDatabase

class database:
    def connectDatabase():
        driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "iVOG0qvVg9iYYGz6WVf8BW19Xv4zmmHbDIkH0ur9PCU"))
        return driver     
