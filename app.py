from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Initialize application
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['JSON_SORT_KEYS'] = False


# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'vehicles.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database and Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Vehicle model
class Vehicle(db.Model):
    vin = db.Column(db.String(17), primary_key=True, nullable=False, unique=True)
    manName = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    horsePower = db.Column(db.Integer, nullable=False)
    modelName = db.Column(db.String(255), nullable=False)
    modelYear = db.Column(db.Integer, nullable=False)
    purchasePrice = db.Column(db.Float, nullable=False)
    fuelType = db.Column(db.String(50), nullable=False)

    def __init__(self, vin, manName, description, horsePower, modelName, modelYear, purchasePrice, fuelType):
        self.vin = vin
        self.manName = manName
        self.description = description
        self.horsePower = horsePower
        self.modelName = modelName
        self.modelYear = modelYear
        self.purchasePrice = purchasePrice
        self.fuelType = fuelType

# Vehicle schema
class VehicleSchema(ma.Schema):
    class Meta:
        ordered = True  
        fields = (
            "vin",
            "manName",
            "description",
            "horsePower",
            "modelName",
            "modelYear",
            "purchasePrice",
            "fuelType",
        )
vehicle_schema = VehicleSchema()
vehicles_schema = VehicleSchema(many=True)


# API Endpoints
@app.route('/vehicle', methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.query.all()
    return jsonify(vehicles_schema.dump(vehicles)), 200

@app.route('/vehicle', methods=['POST'])
def create_vehicle():
    try:
        data = request.get_json()
        if Vehicle.query.get(data['vin']):
            return jsonify({"error": "Vehicle with this VIN already exists"}), 409
        new_vehicle = Vehicle(
            vin=data['vin'],
            manName=data['manName'],
            description=data['description'],
            horsePower=data['horsePower'],
            modelName=data['modelName'],
            modelYear=data['modelYear'],
            purchasePrice=data['purchasePrice'],
            fuelType=data['fuelType']
        )
        db.session.add(new_vehicle)
        db.session.commit()
        return jsonify(vehicle_schema.dump(new_vehicle)), 201
    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 422

@app.route('/vehicle/<string:vin>', methods=['GET'])
def get_vehicle(vin):
    vehicle = Vehicle.query.get(vin)
    if not vehicle:
        abort(404, description="Vehicle not found")
    return jsonify(vehicle_schema.dump(vehicle)), 200

@app.route('/vehicle/<string:vin>', methods=['PUT'])
def update_vehicle(vin):
    vehicle = Vehicle.query.get(vin)
    if not vehicle:
        abort(404, description="Vehicle not found")
    try:
        data = request.get_json()
        vehicle.manName = data.get('manName', vehicle.manName)
        vehicle.description = data.get('description', vehicle.description)
        vehicle.horsePower = data.get('horsePower', vehicle.horsePower)
        vehicle.modelName = data.get('modelName', vehicle.modelName)
        vehicle.modelYear = data.get('modelYear', vehicle.modelYear)
        vehicle.purchasePrice = data.get('purchasePrice', vehicle.purchasePrice)
        vehicle.fuelType = data.get('fuelType', vehicle.fuelType)
        db.session.commit()
        return jsonify(vehicle_schema.dump(vehicle)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 422

@app.route('/vehicle/<string:vin>', methods=['DELETE'])
def delete_vehicle(vin):
    vehicle = Vehicle.query.get(vin)
    if not vehicle:
        abort(404, description="Vehicle not found") 
    db.session.delete(vehicle)
    db.session.commit()
    return '', 204




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)