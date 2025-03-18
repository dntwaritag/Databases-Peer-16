# **Car API (Ford Data API)** 🚗  
A FastAPI application for managing car information with PostgreSQL integration.  

## **Setup** 🛠️  

### **1. Create a Virtual Environment**  
```bash
python -m venv venv  
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **2. Install Dependencies**  
```bash
pip install -r requirements.txt
```

### **3. Create a `.env` File**  
Create a `.env` file in the root directory and add your **PostgreSQL** connection string:  
```
DATABASE_URL="postgresql://your_username:your_password@your_host:your_port/your_database"
```

### **4. Run Database Migrations**  
If using **Alembic** for migrations, run:  
```bash
alembic upgrade head
```
Otherwise, manually create tables in PostgreSQL based on your ORM models.

### **5. Run the Application**  
```bash
uvicorn main:app --reload
```
The API will be available at **http://localhost:8000**  

---

## **API Endpoints**  

### **1. Create a Car**  
📌 **POST** `/cars/`  
**Request Body:**  
```json
{
  "model": "string",
  "year": 2023,
  "price": 25000.0,
  "mileage": 15000,
  "tax": 150,
  "mpg": 30.5,
  "enginesize": 2.0,
  "transmissionid": 1,
  "fueltypeid": 1
}
```

### **2. Get All Cars**  
📌 **GET** `/cars/`  

### **3. Get a Car by ID**  
📌 **GET** `/cars/{car_id}`  

### **4. Update a Car**  
📌 **PUT** `/cars/{car_id}`  
**Request Body:**  
```json
{
  "model": "string",
  "year": 2023,
  "price": 26000.0,
  "mileage": 14000,
  "tax": 140,
  "mpg": 31.0,
  "enginesize": 2.2,
  "transmissionid": 2,
  "fueltypeid": 2
}
```

### **5. Delete a Car**  
📌 **DELETE** `/cars/{car_id}`  

---

## **Database Schema** 📊  
The application uses **SQLAlchemy** ORM with the following tables:  

### **1. Cars Table**
| Column         | Type     | Description           |
|---------------|---------|-----------------------|
| carid        | Integer | Primary Key (Auto)   |
| model        | String  | Car Model Name       |
| year         | Integer | Year of Manufacture  |
| price        | Float   | Car Price ($)        |
| mileage      | Integer | Car Mileage (Km)     |
| tax          | Integer | Annual Tax ($)       |
| mpg          | Float   | Miles per Gallon     |
| enginesize   | Float   | Engine Size (L)      |
| transmissionid | Integer | Foreign Key (Transmissions) |
| fueltypeid   | Integer | Foreign Key (FuelTypes) |

---

## **API Documentation** 📜  
- **Swagger UI:** (https://databases-peer-16-2.onrender.com/docs)  
- **ReDoc:** (https://databases-peer-16-2.onrender.com/redoc)  

---

## **Contributing** 🤝  
1. Fork the repository  
2. Create a new branch (`git checkout -b feature-branch`)  
3. Commit your changes (`git commit -m "Add new feature"`)  
4. Push to the branch (`git push origin feature-branch`)  
5. Open a **Pull Request**  

---

## **License** 📝  
This project is licensed under the **MIT License**.  

