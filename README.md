# CRUD--Style-API

A RESTful API built with Flask for managing vehicle information. This service allows users to create, retrieve, update, and delete vehicle records in a SQLite database. It uses Flask, SQLAlchemy for ORM, and Marshmallow for data serialization and validation.

---

## Features
- **CRUD Operations**: Create, Read, Update, and Delete vehicles.
- **Validation**: Ensures required fields are provided and enforces unique constraints on `VIN`.
- **Ordered Responses**: Returns JSON responses in a consistent, ordered format.
- **Error Handling**: Provides meaningful error messages with appropriate HTTP status codes.

---

## Prerequisites
Before running the application, ensure you have the following installed:
- Python 
- `pip` 

---

## Installation
1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Set up a virtual environment**:
   ```bash
   pipenv shell
   pipenv install flask flask-sqlalchemy flask-marshmallow marshmallow-sqlalchemy
   ```


---

## Running the Application
You can either start the server and send the request to http://127.0.0.1:5000/ or run the test file
1. **Start the server**:
   ```bash
   python app.py
   ```

2. **Run the Test File**:
   python test.py

---

## API Endpoints

### 1. Create a Vehicle
**POST** `/vehicle`

- **Request Body**:
   ```json
   {
       "vin": "1HGCM82633A123456",
       "manName": "Honda",
       "description": "Reliable sedan with great fuel efficiency.",
       "horsePower": 158,
       "modelName": "Civic",
       "modelYear": 2023,
       "purchasePrice": 25000.99,
       "fuelType": "Gasoline"
   }
   ```
- **Response**:
   - `201 Created` on success
   - `400 Bad Request` or `422 Unprocessable Entity` on errors

---

### 2. Get All Vehicles
**GET** `/vehicle`

- **Response**:
   - `200 OK`:
   ```json
   [
       {
           "vin": "1HGCM82633A123456",
           "manName": "Honda",
           "description": "Reliable sedan with great fuel efficiency.",
           "horsePower": 158,
           "modelName": "Civic",
           "modelYear": 2023,
           "purchasePrice": 25000.99,
           "fuelType": "Gasoline"
       }
   ]
   ```

---

### 3. Get a Vehicle by VIN
**GET** `/vehicle/<vin>`

- **Response**:
   - `200 OK` on success
   - `404 Not Found` if the vehicle does not exist

---

### 4. Update a Vehicle
**PUT** `/vehicle/<vin>`

- **Request Body** (partial or full update):
   ```json
   {
       "horsePower": 180,
       "purchasePrice": 26000.99
   }
   ```
- **Response**:
   - `200 OK` on success
   - `404 Not Found` if the vehicle does not exist
   - `422 Unprocessable Entity` on errors

---

### 5. Delete a Vehicle
**DELETE** `/vehicle/<vin>`

- **Response**:
   - `204 No Content` on success
   - `404 Not Found` if the vehicle does not exist

---

## Error Codes
| Code | Description                 |
|------|-----------------------------|
| 200  | Success                     |
| 201  | Resource Created            |
| 204  | No Content (Delete Success) |
| 400  | Bad Request (Invalid Data)  |
| 404  | Not Found                   |
| 409  | Conflict (Duplicate Entry)  |
| 422  | Unprocessable Entity        |

