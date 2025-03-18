import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import unittest
from matching import haversine_distance, find_nearest_driver

class TestMatching(unittest.TestCase):
    def test_haversine_distance(self):
        # Test with known coordinates
        # New York to Los Angeles approximate distance ~3936 km
        ny_lat, ny_lon = 40.7128, -74.0060
        la_lat, la_lon = 34.0522, -118.2437
        
        distance = haversine_distance(ny_lat, ny_lon, la_lat, la_lon)
        
        # Allow for some error margin in the calculation
        self.assertAlmostEqual(distance, 3936, delta=100)
    
    def test_find_nearest_driver(self):
        # Test drivers list
        drivers = [
            {"id": "driver1", "name": "Driver 1", "lat": 40.7128, "lon": -74.0060, "available": True},
            {"id": "driver2", "name": "Driver 2", "lat": 40.7300, "lon": -74.0200, "available": True},
            {"id": "driver3", "name": "Driver 3", "lat": 40.7500, "lon": -74.0300, "available": False}  # Unavailable
        ]
        
        # Rider location
        rider_lat, rider_lon = 40.7200, -74.0100
        
        nearest_driver = find_nearest_driver(drivers, rider_lat, rider_lon)
        
        # Driver 1 should be nearest
        self.assertEqual(nearest_driver["id"], "driver1")
        
    def test_no_available_drivers(self):
        # Test with no available drivers
        drivers = [
            {"id": "driver1", "name": "Driver 1", "lat": 40.7128, "lon": -74.0060, "available": False},
            {"id": "driver2", "name": "Driver 2", "lat": 40.7300, "lon": -74.0200, "available": False}
        ]
        
        rider_lat, rider_lon = 40.7200, -74.0100
        
        nearest_driver = find_nearest_driver(drivers, rider_lat, rider_lon)
        
        # Should return None when no drivers are available
        self.assertIsNone(nearest_driver)

if __name__ == '__main__':
    unittest.main()