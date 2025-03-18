import requests
import os
import random
import time
import json
import math
import redis
from dotenv import load_dotenv

# Loading  environment variables
load_dotenv('src/config.env')

# OpenStreetMap Nominatim API URL
NOMINATIM_API_URL = os.getenv('OPENSTREETMAP_API_URL', 'https://nominatim.openstreetmap.org/search')

# Connect to Redis
REDIS_URL = os.getenv('REDIS_URL')
redis_client = None

try:
    if REDIS_URL:
        redis_client = redis.from_url(REDIS_URL)
        print("Connected to Redis successfully")
except Exception as e:
    print(f"Error connecting to Redis: {e}")
    redis_client = None

def get_random_location_nearby(base_lat, base_lon, max_distance_km=1.0):
    """
    Generate a random location within max_distance_km of the base location
    Used for simulation when real API is not available
    """
    # Converting km to degrees (approximate)
    max_lat_change = max_distance_km / 111.0  # 1 degree lat is about 111 km
    max_lon_change = max_distance_km / (111.0 * abs(math.cos(math.radians(base_lat))))
    
    # Random offset
    lat_change = random.uniform(-max_lat_change, max_lat_change)
    lon_change = random.uniform(-max_lon_change, max_lon_change)
    
    return base_lat + lat_change, base_lon + lon_change

def get_location_by_address(address):
    """
    Get latitude and longitude for a given address using OpenStreetMap Nominatim API
    With Redis caching for performance
    """
    # Check cache first if Redis is available
    if redis_client:
        cached_result = redis_client.get(f"geocode:{address}")
        if cached_result:
            return json.loads(cached_result)
    
    params = {
        'q': address,
        'format': 'json',
        'limit': 1,
    }
    
    headers = {
        'User-Agent': 'RideSharingBackend/1.0'  # Nominatim requires a User-Agent
    }
    
    try:
        response = requests.get(NOMINATIM_API_URL, params=params, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        if data and len(data) > 0:
            lat = float(data[0]['lat'])
            lon = float(data[0]['lon'])
            
            # Cache the result if Redis is available (expire after 24 hours)
            if redis_client:
                redis_client.setex(
                    f"geocode:{address}",
                    86400, 
                    json.dumps((lat, lon))
                )
            
            return lat, lon
        else:
            return None
    except Exception as e:
        print(f"Error fetching location: {e}")
        return None

def update_driver_locations(drivers):
    """
    Simulate movement of drivers by updating their locations
    In a real application, this would fetch actual GPS data from drivers' devices
    Also updates Redis cache with driver locations
    """
    for driver in drivers:
        # Only update locations for available drivers
        if driver["available"]:
            # Simulate movement (in a real app, this would come from the API)
            new_lat, new_lon = get_random_location_nearby(driver["lat"], driver["lon"], 0.5)
            driver["lat"] = new_lat
            driver["lon"] = new_lon
            
            # Update Redis cache if available
            if redis_client:
                driver_data = {
                    "id": driver["id"],
                    "name": driver["name"],
                    "lat": driver["lat"],
                    "lon": driver["lon"],
                    "available": driver["available"],
                    "updated_at": time.time()
                }
                redis_client.setex(
                    f"driver:{driver['id']}",
                    3600, 
                    json.dumps(driver_data)
                )
    
    return drivers

def get_driver_location(driver_id):
    """
    Get a driver's current location from Redis cache or return None if not found
    """
    if not redis_client:
        return None
        
    driver_data = redis_client.get(f"driver:{driver_id}")
    if driver_data:
        return json.loads(driver_data)
    return None

def geocode_address(address):
    """
    Convert an address to latitude and longitude coordinates
    """
    try:
        location = get_location_by_address(address)
        if location:
            return {"lat": location[0], "lon": location[1]}
        else:
            return None
    except Exception as e:
        print(f"Error geocoding address: {e}")
        return None