import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import unittest
from unittest.mock import patch, MagicMock
from api import update_driver_locations, geocode_address

class TestAPI(unittest.TestCase):
    def test_update_driver_locations(self):
        # Mock drivers
        drivers = [
            {"id": "driver1", "name": "Driver 1", "lat": 40.7128, "lon": -74.0060, "available": True},
            {"id": "driver2", "name": "Driver 2", "lat": 40.7300, "lon": -74.0200, "available": False}
        ]
        
        # Update locations
        updated_drivers = update_driver_locations(drivers)
        
        # Check that only available driver's location changed
        self.assertNotEqual(updated_drivers[0]["lat"], 40.7128)
        self.assertNotEqual(updated_drivers[0]["lon"], -74.0060)
        
        # Check that unavailable driver's location didn't change
        self.assertEqual(updated_drivers[1]["lat"], 40.7300)
        self.assertEqual(updated_drivers[1]["lon"], -74.0200)
    
    @patch('api.requests.get')
    def test_geocode_address(self, mock_get):
        # Mock the API response
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
        
        # Test geocoding
        result = geocode_address("New York")
        
        # Check the result
        self.assertEqual(result["lat"], 40.7128)
        self.assertEqual(result["lon"], -74.0060)
    
    @patch('api.requests.get')
    def test_geocode_address_no_results(self, mock_get):
        # Mock empty API response
        mock_response = MagicMock()
        mock_response.json.return_value = []
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Test geocoding with no results
        result = geocode_address("Nonexistent Address")
        
        # Check the result is None
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()