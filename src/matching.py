import math

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    
    Returns distance in kilometers
    """
    # Converting  decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  
    
    return c * r

def find_nearest_driver(drivers, rider_lat, rider_lon):
    """
    Find the nearest available driver to the rider using the Haversine formula
    
    Returns the driver object or None if no drivers are available
    """
    available_drivers = [d for d in drivers if d["available"]]
    
    if not available_drivers:
        return None
    
   
    for driver in available_drivers:
        distance = haversine_distance(
            rider_lat, rider_lon, 
            driver["lat"], driver["lon"]
        )
        driver["distance"] = distance
    
   
    sorted_drivers = sorted(available_drivers, key=lambda d: d["distance"])
    
    # Return the nearest driver
    nearest_driver = sorted_drivers[0]
    
   
    driver_data = {
        "id": nearest_driver["id"],
        "name": nearest_driver["name"],
        "lat": nearest_driver["lat"],
        "lon": nearest_driver["lon"],
        "distance": nearest_driver["distance"]
    }
    
    return driver_data