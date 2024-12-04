import json
from app import app, db

# Sample vehicle data
sample_vehicle = {
    "vin": "1HGCM82633A123456",
    "manName": "Honda",
    "description": "Reliable sedan with great fuel efficiency.",
    "horsePower": 158,
    "modelName": "Civic",
    "modelYear": 2023,
    "purchasePrice": 25000.99,
    "fuelType": "Gasoline"
}

invalid_vehicle = {
    "manName": "Honda" 
}

app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

def print_test_result(method, uri, status, req_entity=None, res_entity=None):
    """Prints the test results in the desired format."""
    print(f"Method: {method}")
    print(f"URI: {uri}")
    print(f"Response Status: {status}")
    if req_entity:
        print("Request Entity:")
        print(json.dumps(req_entity, indent=4))
    if res_entity:
        print("Response Entity:")
        print(json.dumps(req_entity, indent=4))
    print("-" * 50)

with app.test_client() as client:
    with app.app_context():
        db.create_all()

        # POST /vehicle Test 
        response = client.post('/vehicle', data=json.dumps(sample_vehicle), content_type='application/json')
        print_test_result(
            "POST",
            "/vehicle",
            response.status,
            req_entity=sample_vehicle,
            res_entity=response.get_data(as_text=True)
        )

        # GET /vehicle Test
        response = client.get('/vehicle')
        print_test_result(
            "GET",
            "/vehicle",
            response.status,
            res_entity=response.get_data(as_text=True)
        )

        # GET /vehicle/{:vin} Test
        response = client.get(f"/vehicle/{sample_vehicle['vin']}")
        print_test_result(
            "GET",
            f"/vehicle/{sample_vehicle['vin']}",
            response.status,
            res_entity=response.get_data(as_text=True)
        )

        # PUT /vehicle/{:vin} Test
        updated_data = {"horsePower": 200}
        response = client.put(
            f"/vehicle/{sample_vehicle['vin']}",
            data=json.dumps(updated_data),
            content_type='application/json'
        )
        print_test_result(
            "PUT",
            f"/vehicle/{sample_vehicle['vin']}",
            response.status,
            req_entity=updated_data,
            res_entity=response.get_data(as_text=True)
        )

        # DELETE /vehicle/{:vin} Test
        response = client.delete(f"/vehicle/{sample_vehicle['vin']}")
        print_test_result(
            "DELETE",
            f"/vehicle/{sample_vehicle['vin']}",
            response.status
        )

        # GET /vehicle/{:vin} after deletion Test
        response = client.get(f"/vehicle/{sample_vehicle['vin']}")
        print_test_result(
            "GET",
            f"/vehicle/{sample_vehicle['vin']}",
            response.status
        )

        # POST /vehicle with invalid data Test
        response = client.post('/vehicle', data=json.dumps(invalid_vehicle), content_type='application/json')
        print_test_result(
            "POST",
            "/vehicle",
            response.status,
            req_entity=invalid_vehicle,
            res_entity=response.get_data(as_text=True)
        )
