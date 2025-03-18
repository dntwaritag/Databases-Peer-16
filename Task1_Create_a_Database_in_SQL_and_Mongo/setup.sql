-- Create the Transmissions table
CREATE TABLE IF NOT EXISTS Transmissions (
    TransmissionID SERIAL PRIMARY KEY,
    TransmissionType VARCHAR(50) UNIQUE
);

-- Create the FuelTypes table
CREATE TABLE IF NOT EXISTS FuelTypes (
    FuelTypeID SERIAL PRIMARY KEY,
    FuelType VARCHAR(50) UNIQUE
);

-- Create the Cars table
CREATE TABLE IF NOT EXISTS Cars (
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

-- Create the CarLogs table (must be created before the trigger)
CREATE TABLE IF NOT EXISTS CarLogs (
    LogID SERIAL PRIMARY KEY,
    CarID INT,
    LogDate TIMESTAMP DEFAULT NOW(),
    LogAction VARCHAR(50),
    FOREIGN KEY (CarID) REFERENCES Cars(CarID)
);

-- Function to add a new car
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

-- Trigger function to log new car additions
CREATE OR REPLACE FUNCTION LogNewCar() RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO CarLogs (CarID, LogDate, LogAction)
    VALUES (NEW.CarID, NOW(), 'Added');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger
CREATE TRIGGER CarAdded
AFTER INSERT ON Cars
FOR EACH ROW
EXECUTE FUNCTION LogNewCar();

-- Insert sample data
INSERT INTO Transmissions (TransmissionType) VALUES 
('Automatic'),
('Manual'),
('Semi-Automatic');

INSERT INTO FuelTypes (FuelType) VALUES 
('Petrol'),
('Diesel'),
('Electric'),
('Hybrid');

-- Insert a sample car using the AddNewCar function
SELECT AddNewCar(
    'Fiesta',
    2019,
    16500.00,
    'Automatic',
    1482,
    'Petrol',
    145,
    48.7,
    1.0
);

-- Verify the setup
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