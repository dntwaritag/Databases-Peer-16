# Car Management API

A FastAPI application for managing car information with MongoDB integration.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your MongoDB connection string:
```
MONGODB_URL="mongodb+srv://ntwaliaubin:JwMC8NFIMPgN7h6g@ford-data.6zfql.mongodb.net/?retryWrites=true&w=majority&appName=ford-data"
```

4. Run the application:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Create a Car
POST `/cars/`
```json
{
  "model": "string",
  "year": 0,
  "price": 0,
  "mileage": 0,
  "tax": 0,
  "mpg": 0,
  "enginesize": 0,
  "transmissiontype": "string",
  "fueltype": "string"
}
```

### Get All Cars
GET `/cars/`

### Get Car by ID
GET `/cars/{car_id}`

### Update Car
PUT `/cars/{car_id}`
```json
{
  "model": "string",
  "year": 0,
  "price": 0,
  "mileage": 0,
  "tax": 0,
  "mpg": 0,
  "enginesize": 0,
  "transmissiontype": "string",
  "fueltype": "string"
}
```

### Delete Car
DELETE `/cars/{car_id}`

## API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc` 