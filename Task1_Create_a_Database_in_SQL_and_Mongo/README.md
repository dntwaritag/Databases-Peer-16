# Car Database Project

This project implements a relational database system for managing car information using PostgreSQL and MongoDB. It includes tables for storing car details, transmission types, fuel types, and logging functionality.

## ER Diagram

The **Entity-Relationship (ER) Diagram** illustrates the structure and relationships of the database.

[ER Diagram will be added here]

## 1️⃣ PostgreSQL Database Setup

### Step 1: Create Tables

#### Transmissions Table
```sql
CREATE TABLE Transmissions (
    TransmissionID SERIAL PRIMARY KEY,
    TransmissionType VARCHAR(50) UNIQUE
);
```

#### FuelTypes Table
```sql
CREATE TABLE FuelTypes (
    FuelTypeID SERIAL PRIMARY KEY,
    FuelType VARCHAR(50) UNIQUE
);
```

#### Cars Table
```sql
CREATE TABLE Cars (
    CarID SERIAL PRIMARY KEY,
    Model VARCHAR(255),
    Year INT,
    Price DECIMAL(10, 2),
    TransmissionID INT,
    Mileage INT,
    FuelTypeID INT,
    Tax INT,
    MPG FLOAT,
    EngineSize FLOAT,
    FOREIGN KEY (TransmissionID) REFERENCES Transmissions(TransmissionID),
    FOREIGN KEY (FuelTypeID) REFERENCES FuelTypes(FuelTypeID)
);
```

#### CarLogs Table
```sql
CREATE TABLE CarLogs (
    LogID SERIAL PRIMARY KEY,
    CarID INT,
    LogDate TIMESTAMP DEFAULT NOW(),
    LogAction VARCHAR(50),
    FOREIGN KEY (CarID) REFERENCES Cars(CarID)
);
```

### Step 2: Functions and Triggers

#### AddNewCar Function
```sql
CREATE OR REPLACE FUNCTION AddNewCar(
    p_Model VARCHAR(255),
    p_Year INT,
    p_Price DECIMAL(10, 2),
    p_TransmissionType VARCHAR(50),
    p_Mileage INT,
    p_FuelType VARCHAR(50),
    p_Tax INT,
    p_MPG FLOAT,
    p_EngineSize FLOAT
) RETURNS VOID AS $$
DECLARE
    v_TransmissionID INT;
    v_FuelTypeID INT;
BEGIN
    -- Get or insert TransmissionType
    SELECT TransmissionID INTO v_TransmissionID FROM Transmissions WHERE TransmissionType = p_TransmissionType;
    IF v_TransmissionID IS NULL THEN
        INSERT INTO Transmissions (TransmissionType) VALUES (p_TransmissionType) RETURNING TransmissionID INTO v_TransmissionID;
    END IF;

    -- Get or insert FuelType
    SELECT FuelTypeID INTO v_FuelTypeID FROM FuelTypes WHERE FuelType = p_FuelType;
    IF v_FuelTypeID IS NULL THEN
        INSERT INTO FuelTypes (FuelType) VALUES (p_FuelType) RETURNING FuelTypeID INTO v_FuelTypeID;
    END IF;

    -- Insert the car
    INSERT INTO Cars (Model, Year, Price, TransmissionID, Mileage, FuelTypeID, Tax, MPG, EngineSize)
    VALUES (p_Model, p_Year, p_Price, v_TransmissionID, p_Mileage, v_FuelTypeID, p_Tax, p_MPG, p_EngineSize);
END;
$$ LANGUAGE plpgsql;
```

#### LogNewCar Trigger Function
```sql
CREATE OR REPLACE FUNCTION LogNewCar() RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO CarLogs (CarID, LogDate, LogAction)
    VALUES (NEW.CarID, NOW(), 'Added');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

#### Create Trigger
```sql
CREATE TRIGGER CarAdded
AFTER INSERT ON Cars
FOR EACH ROW
EXECUTE FUNCTION LogNewCar();
```

## 2️⃣ MongoDB Integration

### Setup MongoDB with Python

#### Install Dependencies
```bash
pip install pymongo python-dotenv
```

#### Connect to MongoDB
```python
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("MONGO_URI environment variable is not set")

mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client['car_database']

# Initialize collections
collections = ["car_logs", "unstructured_data"]
for collection in collections:
    if collection not in mongo_db.list_collection_names():
        mongo_db.create_collection(collection)
        print(f"Created collection: {collection}")
```

## 📌 Final Queries for Verification

```sql
-- Check database tables
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public';

-- Count records in each table
SELECT 'Transmissions' as table_name, COUNT(*) as count FROM Transmissions
UNION ALL
SELECT 'FuelTypes', COUNT(*) FROM FuelTypes
UNION ALL
SELECT 'Cars', COUNT(*) FROM Cars
UNION ALL
SELECT 'CarLogs', COUNT(*) FROM CarLogs;
```

## **The End! thank you**
