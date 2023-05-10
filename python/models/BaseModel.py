import json

class BaseModel: 
    def __init__(self, driver):
        self.base_url = driver
        
    def get(self, label, id=None):
        with self.driver.session() as session:
            if id is not None:
                result = session.run(f"MATCH ({label}:{label}) WHERE {label}.{label}ID = $id RETURN {label}", id=id)
            else:
                result = session.run(f"MATCH ({label}:{label}) RETURN {label}")
        return json.dumps(result.data())
            
    
    def post(self, label):
        with self.driver.session() as session:
            pass
            
    def delete(self, label, id):
        with self.driver.session() as session:
            result = session.run(f"MATCH ({label}:{label}) WHERE {label}.{label}ID = $id DETACH DELETE {label}", id=id)
            return json.dumps(result.data())
    
    