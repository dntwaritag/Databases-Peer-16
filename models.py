from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Car(Base):
    __tablename__ = "cars"

    carid = Column(Integer, primary_key=True, index=True)
    model = Column(String)
    year = Column(Integer)
    price = Column(Float)
    transmissionid = Column(Integer, ForeignKey("transmissions.transmissionid"))
    mileage = Column(Integer)
    fueltypeid = Column(Integer, ForeignKey("fueltypes.fueltypeid"))
    tax = Column(Integer)
    mpg = Column(Float)
    enginesize = Column(Float)

    transmission = relationship("Transmission", back_populates="cars")
    fueltype = relationship("FuelType", back_populates="cars")

class Transmission(Base):
    __tablename__ = "transmissions"

    transmissionid = Column(Integer, primary_key=True, index=True)
    type = Column(String)

    cars = relationship("Car", back_populates="transmission")

class FuelType(Base):
    __tablename__ = "fueltypes"

    fueltypeid = Column(Integer, primary_key=True, index=True)
    type = Column(String)

    cars = relationship("Car", back_populates="fueltype")

class CarLog(Base):
    __tablename__ = "carlogs"

    logid = Column(Integer, primary_key=True, index=True)
    carid = Column(Integer, ForeignKey("cars.carid"))
    action = Column(String)
    timestamp = Column(String) 