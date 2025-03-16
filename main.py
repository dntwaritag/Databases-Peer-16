from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from database import engine, get_db
from sqlalchemy import text

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Car CRUD operations
@app.post("/cars/", response_model=dict)
def create_car(car: schemas.CarCreate, db: Session = Depends(get_db)):
    try:
        # Call the stored procedure using SQLAlchemy
        query = text("""
            CALL addnewcar(:p_model, :p_year, :p_price, :p_transmissiontype, 
                          :p_mileage, :p_fueltype, :p_tax, :p_mpg, :p_enginesize);
        """)
        
        db.execute(query, {
            'p_model': car.model,
            'p_year': car.year,
            'p_price': car.price,
            'p_transmissiontype': car.transmission_type,
            'p_mileage': car.mileage,
            'p_fueltype': car.fuel_type,
            'p_tax': car.tax,
            'p_mpg': car.mpg,
            'p_enginesize': car.enginesize
        })
        db.commit()
        return {"message": "Car added successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to add car: {str(e)}")

@app.get("/cars/", response_model=List[schemas.Car])
def read_cars(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cars = db.query(models.Car).offset(skip).limit(limit).all()
    return cars

@app.get("/cars/{car_id}", response_model=schemas.Car)
def read_car(car_id: int, db: Session = Depends(get_db)):
    db_car = db.query(models.Car).filter(models.Car.carid == car_id).first()
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return db_car

@app.put("/cars/{car_id}", response_model=schemas.Car)
def update_car(car_id: int, car: schemas.CarCreate, db: Session = Depends(get_db)):
    db_car = db.query(models.Car).filter(models.Car.carid == car_id).first()
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    
    # Call the stored procedure to update the car
    try:
        query = text("""
            SELECT addnewcar(:model, :year, :price, :transmission_type, 
                           :mileage, :fuel_type, :tax, :mpg, :engine_size)
        """)
        
        db.execute(query, {
            'model': car.model,
            'year': car.year,
            'price': car.price,
            'transmission_type': car.transmission_type,
            'mileage': car.mileage,
            'fuel_type': car.fuel_type,
            'tax': car.tax,
            'mpg': car.mpg,
            'engine_size': car.enginesize
        })
        db.commit()
        
        # Fetch the updated car
        updated_car = db.query(models.Car).filter(models.Car.carid == car_id).first()
        return updated_car
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/cars/{car_id}")
def delete_car(car_id: int, db: Session = Depends(get_db)):
    db_car = db.query(models.Car).filter(models.Car.carid == car_id).first()
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    
    db.delete(db_car)
    db.commit()
    return {"message": "Car deleted successfully"}

# Transmission CRUD operations
@app.post("/transmissions/", response_model=schemas.Transmission)
def create_transmission(transmission: schemas.TransmissionCreate, db: Session = Depends(get_db)):
    db_transmission = models.Transmission(**transmission.dict())
    db.add(db_transmission)
    db.commit()
    db.refresh(db_transmission)
    return db_transmission

@app.get("/transmissions/", response_model=List[schemas.Transmission])
def read_transmissions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    transmissions = db.query(models.Transmission).offset(skip).limit(limit).all()
    return transmissions

# FuelType CRUD operations
@app.post("/fueltypes/", response_model=schemas.FuelType)
def create_fueltype(fueltype: schemas.FuelTypeCreate, db: Session = Depends(get_db)):
    db_fueltype = models.FuelType(**fueltype.dict())
    db.add(db_fueltype)
    db.commit()
    db.refresh(db_fueltype)
    return db_fueltype

@app.get("/fueltypes/", response_model=List[schemas.FuelType])
def read_fueltypes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    fueltypes = db.query(models.FuelType).offset(skip).limit(limit).all()
    return fueltypes 