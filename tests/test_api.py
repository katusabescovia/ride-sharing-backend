import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import unittest
from unittest.mock import patch, MagicMock
from api import update_driver_locations, get_location_by_address
import redis

class TestAPI(unittest.TestCase):
    
    @patch('api.requests.get')
    def test_get_location_by_address(self, mock_get):
        """Test if geolocation API correctly returns lat/lon."""
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {
                "lat": "40.7128",
                "lon": "-74.0060",
                "display_name": "New York, United States"
            }
        ]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = get_location_by_address("New York")
        
        self.assertIsNotNone(result)
        self.assertAlmostEqual(result[0], 40.7128, places=4)
        self.assertAlmostEqual(result[1], -74.0060, places=4)
    
    @patch('api.requests.get')
    def test_get_location_by_address_no_results(self, mock_get):
        """Test geolocation API when no results are found."""
        mock_response = MagicMock()
        mock_response.json.return_value = []
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = get_location_by_address("Nonexistent Address")
        
        self.assertIsNone(result)

    @patch('redis.client.Redis')
    @patch('api.get_random_location_nearby')
    def test_update_driver_locations(self, mock_random_location, MockRedis):
        """Test if update_driver_locations correctly updates driver locations."""
        mock_redis_instance = MockRedis.return_value
        mock_redis_instance.setex.return_value = True  

        # Simulating new location near original position
        mock_random_location.return_value = (40.7129, -74.0059)
        
        drivers = [
            {"id": "driver1", "name": "Driver 1", "lat": 40.7128, "lon": -74.0060, "available": True},
            {"id": "driver2", "name": "Driver 2", "lat": 40.7300, "lon": -74.0200, "available": False}
        ]
        
        updated_drivers = update_driver_locations(drivers)
        
        # Check that available driver moved
        self.assertAlmostEqual(updated_drivers[0]["lat"], 40.7129, places=4)
        self.assertAlmostEqual(updated_drivers[0]["lon"], -74.0059, places=4)

        # Check that unavailable driver did NOT move
        self.assertEqual(updated_drivers[1]["lat"], 40.7300)
        self.assertEqual(updated_drivers[1]["lon"], -74.0200)

if __name__ == '__main__':
    unittest.main()
