from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class TransmissionType(str, Enum):
    AUTOMATIC = "Automatic"
    MANUAL = "Manual"
    SEMI_AUTO = "Semi-Auto"

class FuelType(str, Enum):
    PETROL = "Petrol"
    DIESEL = "Diesel"
    HYBRID = "Hybrid"
    ELECTRIC = "Electric"
    OTHER = "Other"

class CarBase(BaseModel):
    model: str
    year: int
    price: float
    transmission_type: TransmissionType
    mileage: int
    fuel_type: FuelType
    tax: int
    mpg: float
    enginesize: float

    class Config:
        use_enum_values = True

class CarCreate(CarBase):
    pass

class Car(BaseModel):
    carid: int
    model: str
    year: int
    price: float
    transmissionid: int
    mileage: int
    fueltypeid: int
    tax: int
    mpg: float
    enginesize: float

    class Config:
        from_attributes = True

class TransmissionBase(BaseModel):
    type: str

class TransmissionCreate(TransmissionBase):
    pass

class Transmission(TransmissionBase):
    transmissionid: int

    class Config:
        from_attributes = True

class FuelTypeBase(BaseModel):
    type: str

class FuelTypeCreate(FuelTypeBase):
    pass

class FuelType(FuelTypeBase):
    fueltypeid: int

    class Config:
        from_attributes = True

class CarStoredProcedure(BaseModel):
    model: str
    year: int
    price: float
    transmission_type: TransmissionType
    mileage: int
    fuel_type: FuelType
    tax: int
    mpg: float
    engine_size: float

    class Config:
        use_enum_values = True 