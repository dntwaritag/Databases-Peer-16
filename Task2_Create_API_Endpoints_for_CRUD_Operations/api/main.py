from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
import models
import schemas
from database import get_db, engine

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/cars/", response_model=schemas.Car)
def create_car(car: schemas.CarCreate, db: Session = Depends(get_db)):
    # Call the addnewcar function
    db.execute(
        text("""
        SELECT addnewcar(
            :model, :year, :price, :transmissiontype, 
            :mileage, :fueltype, :tax, :mpg, :enginesize
        )
        """),
        {
            "model": car.model,
            "year": car.year,
            "price": car.price,
            "transmissiontype": car.transmissiontype,
            "mileage": car.mileage,
            "fueltype": car.fueltype,
            "tax": car.tax,
            "mpg": car.mpg,
            "enginesize": car.enginesize
        }
    )
    db.commit()
    
    # Get the last inserted car
    new_car = db.query(models.Car).order_by(models.Car.carid.desc()).first()
    print(f"\nNewly created car: {vars(new_car)}")
    return new_car

@app.get("/cars/", response_model=List[schemas.Car])
def read_cars(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cars = db.query(models.Car).offset(skip).limit(limit).all()
    total_cars = db.query(models.Car).count()
    print(f"\nTotal number of cars in database: {total_cars}")
    return cars

@app.get("/cars/{car_id}", response_model=schemas.Car)
def read_car(car_id: int, db: Session = Depends(get_db)):
    car = db.query(models.Car).filter(models.Car.carid == car_id).first()
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return car

@app.put("/cars/{car_id}", response_model=schemas.Car)
def update_car(car_id: int, car: schemas.CarUpdate, db: Session = Depends(get_db)):
    db_car = db.query(models.Car).filter(models.Car.carid == car_id).first()
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")

    update_data = car.dict(exclude_unset=True)
    
    # Handle transmission type update
    if "transmissiontype" in update_data:
        trans_type = update_data.pop("transmissiontype")
        trans = db.query(models.Transmission).filter(models.Transmission.transmissiontype == trans_type).first()
        if trans is None:
            trans = models.Transmission(transmissiontype=trans_type)
            db.add(trans)
            db.flush()
        update_data["transmissionid"] = trans.transmissionid

    # Handle fuel type update
    if "fueltype" in update_data:
        fuel_type = update_data.pop("fueltype")
        fuel = db.query(models.FuelType).filter(models.FuelType.fueltype == fuel_type).first()
        if fuel is None:
            fuel = models.FuelType(fueltype=fuel_type)
            db.add(fuel)
            db.flush()
        update_data["fueltypeid"] = fuel.fueltypeid

    for key, value in update_data.items():
        setattr(db_car, key, value)
    
    db.commit()
    db.refresh(db_car)
    return db_car

@app.delete("/cars/{car_id}")
def delete_car(car_id: int, db: Session = Depends(get_db)):
    # First check if car exists
    car = db.query(models.Car).filter(models.Car.carid == car_id).first()
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    
    try:
        # First delete related records in carlogs
        db.execute(
            text("DELETE FROM carlogs WHERE carid = :car_id"),
            {"car_id": car_id}
        )
        
        # Then delete the car
        db.delete(car)
        db.commit()
        return {"message": "Car and related logs deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e)) 