import requests

class baseModel: 
    def __init__(self, driver):
        self.base_url = driver
        
    def get(self, label):
        with self.driver.session() as session:
            result = session.run(f"MATCH (n:{label}) RETURN n")
            return [record["n"] for record in result]
    
    def post(self, label, node_id):
        pass
    
    def delete(self, id=None):
        pass
    
    