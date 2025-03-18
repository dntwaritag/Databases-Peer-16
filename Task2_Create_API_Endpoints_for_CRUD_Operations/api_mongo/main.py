from fastapi import FastAPI, HTTPException, Query, Path
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from bson import ObjectId
import os
from dotenv import load_dotenv
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='app.log'
)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI(
    title="Car Management API",
    description="An API for managing car information with MongoDB integration",
    version="1.0.0"
)

# MongoDB connection
MONGODB_URL = os.getenv("MONGODB_URL")
client = AsyncIOMotorClient(MONGODB_URL)
db = client["ford-data"]

class Car(BaseModel):
    model: str = Field(..., description="The model name of the car")
    year: int = Field(..., ge=1900, le=datetime.now().year + 1, description="The manufacturing year")
    price: float = Field(..., gt=0, description="The price of the car")
    mileage: float = Field(..., ge=0, description="The mileage of the car")
    tax: float = Field(..., ge=0, description="The tax amount")
    mpg: float = Field(..., gt=0, description="Miles per gallon")
    enginesize: float = Field(..., gt=0, description="The engine size in liters")
    transmissiontype: str = Field(..., description="The type of transmission")
    fueltype: str = Field(..., description="The type of fuel")

    @validator('year')
    def validate_year(cls, v):
        current_year = datetime.now().year
        if v < 1900 or v > current_year + 1:
            raise ValueError(f'Year must be between 1900 and {current_year + 1}')
        return v

    class Config:
        schema_extra = {
            "example": {
                "model": "Fiesta",
                "year": 2019,
                "price": 16500,
                "mileage": 1482,
                "tax": 145,
                "mpg": 48.7,
                "enginesize": 1,
                "transmissiontype": "Automatic",
                "fueltype": "Petrol"
            }
        }

class UpdateCar(BaseModel):
    model: Optional[str] = Field(None, description="The model name of the car")
    year: Optional[int] = Field(None, ge=1900, le=datetime.now().year + 1, description="The manufacturing year")
    price: Optional[float] = Field(None, gt=0, description="The price of the car")
    mileage: Optional[float] = Field(None, ge=0, description="The mileage of the car")
    tax: Optional[float] = Field(None, ge=0, description="The tax amount")
    mpg: Optional[float] = Field(None, gt=0, description="Miles per gallon")
    enginesize: Optional[float] = Field(None, gt=0, description="The engine size in liters")
    transmissiontype: Optional[str] = Field(None, description="The type of transmission")
    fueltype: Optional[str] = Field(None, description="The type of fuel")

    @validator('year')
    def validate_year(cls, v):
        if v is not None:
            current_year = datetime.now().year
            if v < 1900 or v > current_year + 1:
                raise ValueError(f'Year must be between 1900 and {current_year + 1}')
        return v

    class Config:
        schema_extra = {
            "example": {
                "price": 16500,
                "mileage": 1482
            }
        }

def car_helper(car) -> dict:
    """Convert MongoDB car document to API response format"""
    return {
        "id": str(car["_id"]),
        "model": car["model"],
        "year": car["year"],
        "price": car["price"],
        "mileage": car["mileage"],
        "tax": car["tax"],
        "mpg": car["mpg"],
        "enginesize": car["enginesize"],
        "transmissionid": car["transmissionid"],
        "fueltypeid": car["fueltypeid"]
    }

@app.get("/fueltypes/", response_model=List[str], tags=["Fuel Types"])
async def get_fuel_types():
    """Get all available fuel types"""
    try:
        fuel_types = []
        async for fuel in db.fueltype.find():
            fuel_types.append(fuel["fueltype"])
        return fuel_types
    except Exception as e:
        logger.error(f"Error fetching fuel types: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching fuel types")

@app.get("/transmissions/", response_model=List[str], tags=["Transmissions"])
async def get_transmission_types():
    """Get all available transmission types"""
    try:
        transmission_types = []
        async for transmission in db.transmissions.find():
            transmission_types.append(transmission["transmissiontype"])
        return transmission_types
    except Exception as e:
        logger.error(f"Error fetching transmission types: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching transmission types")

@app.post("/cars/", response_model=Dict[str, Any], tags=["Cars"])
async def create_car(car: Car):
    """Create a new car entry"""
    try:
        # Get transmission ID
        transmission = await db.transmissions.find_one(
            {"transmissiontype": {"$regex": f"^{car.transmissiontype}$", "$options": "i"}}
        )
        if not transmission:
            raise HTTPException(status_code=404, detail=f"Transmission type '{car.transmissiontype}' not found")
        
        # Get fuel type ID
        fuel_type = await db.fueltype.find_one(
            {"fueltype": {"$regex": f"^{car.fueltype}$", "$options": "i"}}
        )
        if not fuel_type:
            # Get available fuel types for error message
            fuel_types = [ft["fueltype"] async for ft in db.fueltype.find()]
            raise HTTPException(
                status_code=404, 
                detail=f"Fuel type '{car.fueltype}' not found. Available types: {fuel_types}"
            )
        
        car_dict = car.dict()
        car_dict["transmissionid"] = transmission["transmissionid"]
        car_dict["fueltypeid"] = fuel_type["fueltypeid"]
        
        # Remove transmissiontype and fueltype from dict before inserting
        del car_dict["transmissiontype"]
        del car_dict["fueltype"]
        
        result = await db.cars.insert_one(car_dict)
        created_car = await db.cars.find_one({"_id": result.inserted_id})
        logger.info(f"Created car: {car.model}")
        return car_helper(created_car)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating car: {str(e)}")
        raise HTTPException(status_code=500, detail="Error creating car")

@app.get("/cars/", response_model=List[Dict[str, Any]], tags=["Cars"])
async def get_cars(
    skip: int = Query(0, ge=0, description="Number of cars to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of cars to return")
):
    """Get all cars with pagination"""
    try:
        cars = []
        cursor = db.cars.find().skip(skip).limit(limit)
        async for car in cursor:
            cars.append(car_helper(car))
        return cars
    except Exception as e:
        logger.error(f"Error fetching cars: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching cars")

@app.get("/cars/{car_id}", response_model=Dict[str, Any], tags=["Cars"])
async def get_car(car_id: str):
    """Get a specific car by ID"""
    try:
        car = await db.cars.find_one({"_id": ObjectId(car_id)})
        if car:
            return car_helper(car)
        raise HTTPException(status_code=404, detail="Car not found")
    except Exception as e:
        logger.error(f"Error fetching car {car_id}: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid car ID")

@app.put("/cars/{car_id}", response_model=Dict[str, Any], tags=["Cars"])
async def update_car(
    car_id: str,
    car: UpdateCar
):
    """Update a specific car with partial updates allowed"""
    try:
        update_data = {}
        car_dict = car.dict(exclude_unset=True)  # Only get fields that were actually provided

        # Only validate transmission type if it's being updated
        if car.transmissiontype is not None:
            transmission = await db.transmissions.find_one(
                {"transmissiontype": {"$regex": f"^{car.transmissiontype}$", "$options": "i"}}
            )
            if not transmission:
                raise HTTPException(status_code=404, detail=f"Transmission type '{car.transmissiontype}' not found")
            update_data["transmissionid"] = transmission["transmissionid"]
            del car_dict["transmissiontype"]

        # Only validate fuel type if it's being updated
        if car.fueltype is not None:
            fuel_type = await db.fueltype.find_one(
                {"fueltype": {"$regex": f"^{car.fueltype}$", "$options": "i"}}
            )
            if not fuel_type:
                raise HTTPException(status_code=404, detail=f"Fuel type '{car.fueltype}' not found")
            update_data["fueltypeid"] = fuel_type["fueltypeid"]
            del car_dict["fueltype"]

        # Add any other fields that were provided
        update_data.update(car_dict)

        if not update_data:
            raise HTTPException(status_code=400, detail="No valid fields provided for update")

        result = await db.cars.update_one(
            {"_id": ObjectId(car_id)},
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Car not found")
            
        updated_car = await db.cars.find_one({"_id": ObjectId(car_id)})
        logger.info(f"Updated car: {car_id}")
        return car_helper(updated_car)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating car {car_id}: {str(e)}")
        raise HTTPException(status_code=400, detail="Error updating car")

@app.delete("/cars/{car_id}", tags=["Cars"])
async def delete_car(car_id: str):
    """Delete a specific car"""
    try:
        result = await db.cars.delete_one({"_id": ObjectId(car_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Car not found")
        logger.info(f"Deleted car: {car_id}")
        return {"message": "Car deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting car {car_id}: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid car ID")

@app.get("/predict/mpg/{car_id}", tags=["Predictions"])
async def predict_mpg(car_id: str):
    """Predict MPG for a specific car"""
    try:
        car = await db.cars.find_one({"_id": ObjectId(car_id)})
        if not car:
            raise HTTPException(status_code=404, detail="Car not found")
        
        # Simple mock prediction based on engine size
        mock_prediction = car["enginesize"] * 20
        
        return {
            "car_id": car_id,
            "actual_mpg": car["mpg"],
            "predicted_mpg": mock_prediction,
            "note": "This is a mock prediction. Replace with actual ML model."
        }
    except Exception as e:
        logger.error(f"Error predicting MPG for car {car_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error predicting MPG") 