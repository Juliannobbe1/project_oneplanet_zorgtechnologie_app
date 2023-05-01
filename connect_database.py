from neo4j import GraphDatabase

class database:
    def connectDatabase():
        driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "iVOG0qvVg9iYYGz6WVf8BW19Xv4zmmHbDIkH0ur9PCU"))
        return driver

    def runQuery(self):#, query):
        # Define a Cypher query to retrieve nodes with a specific label
        query = "MATCH (n:Label) RETURN n"

        # Run the query and retrieve the results
        with self.driver.session() as session:
            result = session.run(query)
            data = result.data()
            
        # Print the data retrieved from the database
        print(data)
            
        return data

        
