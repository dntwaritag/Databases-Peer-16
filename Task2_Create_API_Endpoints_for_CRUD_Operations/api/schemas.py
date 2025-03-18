from pydantic import BaseModel
from typing import Optional

class CarBase(BaseModel):
    model: str
    year: int
    price: float
    mileage: int
    tax: int
    mpg: float
    enginesize: float

class CarCreate(CarBase):
    transmissiontype: str
    fueltype: str

class Car(CarBase):
    carid: Optional[int] = None
    transmissionid: Optional[int] = None
    fueltypeid: Optional[int] = None

    class Config:
        from_attributes = True

class CarUpdate(BaseModel):
    model: Optional[str] = None
    year: Optional[int] = None
    price: Optional[float] = None
    mileage: Optional[int] = None
    tax: Optional[int] = None
    mpg: Optional[float] = None
    enginesize: Optional[float] = None
    transmissiontype: Optional[str] = None
    fueltype: Optional[str] = None 