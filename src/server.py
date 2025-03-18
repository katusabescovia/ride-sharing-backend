from flask import Flask, request, jsonify
import uuid
from matching import find_nearest_driver
from api import update_driver_locations
import os
import threading
import time
import json

app = Flask(__name__)

# In-memory database for demonstration
drivers = []
rides = {}

# Load initial drivers (in production this would come from a database)
drivers = [
    {"id": "driver1", "name": "John Doe", "lat": 40.7128, "lon": -74.0060, "available": True},
    {"id": "driver2", "name": "Jane Smith", "lat": 40.7300, "lon": -74.0200, "available": True},
    {"id": "driver3", "name": "Bob Johnson", "lat": 40.7400, "lon": -73.9900, "available": True},
]

# Background thread to periodically update driver locations
def update_locations_periodically():
    while True:
        try:
            update_driver_locations(drivers)
            print("Updated driver locations")
        except Exception as e:
            print(f"Error updating driver locations: {e}")
        time.sleep(60)  # Update every minute

# Start the background location update thread
location_thread = threading.Thread(target=update_locations_periodically, daemon=True)
location_thread.start()

@app.route('/request-ride', methods=['POST'])
def request_ride():
    data = request.json
    
    if not data or 'lat' not in data or 'lon' not in data:
        return jsonify({"error": "Missing location data"}), 400
    
    rider_lat = data['lat']
    rider_lon = data['lon']
    
    # Find the nearest available driver
    driver = find_nearest_driver(drivers, rider_lat, rider_lon)
    
    if not driver:
        return jsonify({"error": "No drivers available"}), 404
    
    # Create a new ride
    ride_id = str(uuid.uuid4())
    rides[ride_id] = {
        "id": ride_id,
        "rider_lat": rider_lat,
        "rider_lon": rider_lon,
        "driver": driver,
        "status": "assigned",
        "created_at": time.time()
    }
    
    # Mark the driver as unavailable
    for d in drivers:
        if d["id"] == driver["id"]:
            d["available"] = False
    
    return jsonify({
        "ride_id": ride_id,
        "driver": driver,
        "status": "assigned"
    }), 201

@app.route('/drivers', methods=['GET'])
def list_drivers():
    available_drivers = [d for d in drivers if d["available"]]
    return jsonify({"drivers": available_drivers})

@app.route('/ride-status/<ride_id>', methods=['GET'])
def ride_status(ride_id):
    if ride_id not in rides:
        return jsonify({"error": "Ride not found"}), 404
    
    return jsonify(rides[ride_id])

@app.route('/complete-ride/<ride_id>', methods=['POST'])
def complete_ride(ride_id):
    if ride_id not in rides:
        return jsonify({"error": "Ride not found"}), 404
    
    # Update ride status
    rides[ride_id]["status"] = "completed"
    
    # Mark the driver as available again
    driver_id = rides[ride_id]["driver"]["id"]
    for d in drivers:
        if d["id"] == driver_id:
            d["available"] = True
    
    return jsonify({"status": "success", "ride": rides[ride_id]})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)