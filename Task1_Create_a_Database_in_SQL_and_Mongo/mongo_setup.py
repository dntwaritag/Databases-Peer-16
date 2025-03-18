from pymongo import MongoClient
from dotenv import load_dotenv
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mongo_setup.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def setup_mongodb():
    try:
        load_dotenv()
        MONGO_URI = os.getenv("MONGO_URI")
        if not MONGO_URI:
            raise ValueError("MONGO_URI environment variable is not set")

        # Connect to MongoDB
        mongo_client = MongoClient(MONGO_URI)
        mongo_db = mongo_client['ford-data'] 
        
        collections = ["transmissions", "fueltype", "cars"]
        for collection in collections:
            if collection not in mongo_db.list_collection_names():
                mongo_db.create_collection(collection)
                logger.info(f"Created collection: {collection}")

                # Insert initial data only if collection was just created
                if collection == "transmissions":
                    transmissions_data = [
                        {"transmission_type": "Automatic"},
                        {"transmission_type": "Manual"},
                        {"transmission_type": "Semi-Automatic"}
                    ]
                    mongo_db.transmissions.insert_many(transmissions_data)
                    logger.info("Inserted transmission types")
                
                elif collection == "fueltype":
                    fuel_types_data = [
                        {"fuel_type": "Petrol"},
                        {"fuel_type": "Diesel"},
                        {"fuel_type": "Electric"},
                        {"fuel_type": "Hybrid"}
                    ]
                    mongo_db.fueltype.insert_many(fuel_types_data)
                    logger.info("Inserted fuel types")
                
                elif collection == "cars" and mongo_db.cars.count_documents({}) == 0:
                    car_data = {
                        "model": "Civic",
                        "year": 2018,
                        "price": 16000,
                        "transmissionid": 1,
                        "mileage": 15000,
                        "fueltypeid": 1,
                        "tax": 130,
                        "mpg": 38.2,
                        "enginesize": 2
                    }
                    mongo_db.cars.insert_one(car_data)
                    logger.info("Inserted sample car data")
            else:
                logger.info(f"Collection {collection} already exists")

        return mongo_db

    except Exception as e:
        logger.error(f"Error setting up MongoDB: {str(e)}")
        raise

def verify_data(mongo_db):
    """Verify data in MongoDB collections"""
    try:
        # Check collections
        collections = mongo_db.list_collection_names()
        logger.info(f"Available collections: {collections}")

        # Check document counts
        for collection in collections:
            count = mongo_db[collection].count_documents({})
            logger.info(f"Document count in {collection}: {count}")

        # Sample queries to verify data structure
        for collection in collections:
            sample = mongo_db[collection].find_one()
            if sample:
                logger.info(f"Sample document in {collection}: {sample}")

    except Exception as e:
        logger.error(f"Error verifying data: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        # Setup MongoDB connection and create collections
        mongo_db = setup_mongodb()
        
        # Verify data
        verify_data(mongo_db)
        
        logger.info("MongoDB setup completed successfully")
        
    except Exception as e:
        logger.error(f"Failed to complete MongoDB setup: {str(e)}")
        raise 