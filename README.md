# ride-sharing-backend

## 📌 Overview
This project is a simplified ride-sharing backend that demonstrates:
- **Code Versioning** → Implemented with Git
- **Algorithm Design** → Assigning drivers to riders based on distance and availability
- **API Integration** → Fetching real-time driver locations using OpenStreetMap API
- **Code Deployment** → Dockerized service for easy deployment to cloud platforms
---

## 🚀 Features
✅ **Ride-Matching Algorithm**
- Assigns the nearest driver to a rider using the Haversine formula

✅ **Real-Time Geolocation Fetching**
- Integrates with OpenStreetMap API to update driver locations

✅ **Dockerized & Deployment-Ready**
- Supports docker deployment with Docker Compose

✅ **REST API Endpoints**
- Exposes APIs for requesting rides, listing drivers, and tracking rides


## 📂 Project Structure

📦 ride-sharing-backend
├── 📂 src
│   ├── 📄 server.py → API and logic
│   ├── 📄 matching.py → Ride-matching algorithm
│   ├── 📄 api.py → External API integration
│   ├── 📄 config.env → Environment variables
├── 📂 tests
│   ├── 📄 test_matching.py → Test for matching algorithm
│   
├── 📄 Dockerfile → Containerization setup
├── 📄 docker-compose.yml → Local development setup
├── 📄 .github/workflows/ci-cd.yml → CI/CD pipeline
├── 📄 README.md → Documentation
├── 📄 requirements.txt → Python dependencies


## 🛠️ Installation & Setup
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/katusabescovia/ride-sharing-backend.git
cd ride-sharing-backend


2️⃣ Set Up Environment Variables
Create a config.env file in the src directory and add API keys & configs:
CopyPORT=8080
PORT=8080
OPENSTREETMAP_API_KEY=your_api_key_here
REDIS_URL=your_redis_url


3️⃣ Run with Docker
 cd ride-sharing-backend- Run- docker-compose up --build


4️⃣ Run Locally
# Install requirements
pip install -r requirements.txt

# Run the application
python src/server.py


🔌 API Endpoints

| Method | Endpoint            | Description                        |
|--------|---------------------|------------------------------------|
| POST   | `/request-ride`     | Request a ride, match  driver      |
| GET    | `/drivers`          | List available drivers            |
| GET    | `/ride-status/:id`  | Track an ongoing ride             |
| POST     | complete-ride/:id  |Mark a ride as completed

Example Request:

TESTING ENDPOINT:Postman
curl -X POST "http://localhost:8080/request-ride" -H "Content-Type: application/json" -d '{ "lat": 40.7128, "lon": -74.0060 }' 

  Results:{
  
  {
    "driver": {
        "distance": 0.7452342998124134,
        "id": "driver1",
        "lat": 40.717044226651076,
        "lon": -74.0128432124473,
        "name": "John Doe"
    },
    "ride_id": "c90690ee-b925-498b-9a55-d95ca28c4633",
    "status": "assigned"}


curl -X GET "http://localhost:8080/drivers"


Result:
{
    {
    "drivers": [
        {
            "available": true,
            "distance": 1.9553091505908613,
            "id": "driver2",
            "lat": 40.72879260170919,
            "lon": -74.00274158039682,
            "name": "Jane Smith"
        },
        {
            "available": true,
            "distance": 3.8144970078140856,
            "id": "driver3",
            "lat": 40.73313995154971,
            "lon": -73.99093962203189,
            "name": "Bob Johnson"
        }
    ]
}
}




🧪 Running Tests
# Run all tests
pytest

# Run specific test file
pytest tests/test_matching.py

🌍 Deployment
Deploy with Docker
- Build & Push to Container Registry
docker build -t ride-sharing-backend .
docker tag ride-sharing-backend your-container-registry/ride-sharing
docker push your-container-registry/ride-sharing



💡 Future Improvements
🔹 Implement real-time updates with WebSockets
🔹 Add payment integration for ride fare calculation
🔹 Enhance security with OAuth2 authentication
🔹 Implement ride history and user ratings
🔹 Add admin dashboard for monitoring and analytics

🏆 Contributing
Pull requests are welcome! Please open an issue first for major changes.


📜 License
MIT License © 2025 True African


