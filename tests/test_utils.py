
class User_Object:
    def __init__(self, name, id, status, age):
        self.id = id
        self.name = name
        self.status = status
        self.age = age

    def to_dict(self):
        return {"name":self.name, "id": self.id, "status":self.status, "age":self.age}

    def __eq__(self, other):
        return self.name == other.name and self.status == other.status and self.age == other.age and self.id == other.id

    def get_id(self):
        return self.id

def cleanup(test_client, id):
    endpoint = '/api/users/{}'.format(id)
    response = test_client.delete(endpoint)
    assert response.status_code == 202

def setup_env(test_client, created_user): 
    response = test_client.post('/api/users/', json={
        "name": created_user["name"], "age": created_user["age"]})
    assert response.status_code == 201
    return response.get_json()

def convert_to_dict(l):
    output = []
    for obj in l:
        output.append(obj.__dict__)
    return output