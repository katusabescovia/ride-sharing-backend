import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import unittest
from unittest.mock import patch, MagicMock
from api import update_driver_locations, geocode_address
import redis

class TestAPI(unittest.TestCase):
    
    @patch('api.requests.get')
    def test_geocode_address(self, mock_get):
        # Mocking the API response
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {
                "lat": "40.7128",  # Mock lat as string
                "lon": "-74.0060",  # Mock lon as string
                "display_name": "New York, United States"
            }
        ]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Testing geocoding
        result = geocode_address("New York")
        
        # Checking the result and ensure lat/lon are converted to float
        self.assertEqual(float(result["lat"]), 40.7128)
        self.assertEqual(float(result["lon"]), -74.0060)
    
    @patch('api.requests.get')
    def test_geocode_address_no_results(self, mock_get):
        # Mocking empty API response
        mock_response = MagicMock()
        mock_response.json.return_value = []
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Testing geocoding with no results
        result = geocode_address("Nonexistent Address")
        
        # Checking the result is None
        self.assertIsNone(result)

    @patch('redis.client.Redis')
    def test_update_driver_locations(self, MockRedis):
        # Mocking the Redis connection
        mock_redis_instance = MockRedis.return_value
        mock_redis_instance.setex.return_value = True  # Mock successful Redis interaction
        
        # Mocking drivers
        drivers = [
            {"id": "driver1", "name": "Driver 1", "lat": 40.7128, "lon": -74.0060, "available": True},
            {"id": "driver2", "name": "Driver 2", "lat": 40.7300, "lon": -74.0200, "available": False}
        ]
        
        # Updating locations
        updated_drivers = update_driver_locations(drivers)
        
        # Checking that only available driver's location changed
        self.assertNotEqual(updated_drivers[0]["lat"], 40.7128)
        self.assertNotEqual(updated_drivers[0]["lon"], -74.0060)
        
        # Checking  that unavailable driver's location didn't change
        self.assertEqual(updated_drivers[1]["lat"], 40.7300)
        self.assertEqual(updated_drivers[1]["lon"], -74.0200)

if __name__ == '__main__':
    unittest.main()
