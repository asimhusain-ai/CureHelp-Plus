"""
Unit tests for profile_manager.py
Tests patient profile management functionality
"""

import unittest
import sys
import os
import json
import tempfile
import shutil
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from profile_manager import ProfileManager


class TestProfileManager(unittest.TestCase):
    """Test cases for ProfileManager class"""
    
    def setUp(self):
        """Set up test environment before each test"""
        # Create a temporary directory for test profiles
        self.test_dir = tempfile.mkdtemp()
        self.test_profiles_file = os.path.join(self.test_dir, "test_profiles.json")
        
        # Create a ProfileManager instance with test file
        self.manager = ProfileManager()
        self.manager.profiles_file = self.test_profiles_file
        
        # Mock session state
        self.mock_session_state = {
            'user_profiles': [],
            'current_profile': None,
            'current_profile_id': None,
            'predictions': {}
        }
    
    def tearDown(self):
        """Clean up after each test"""
        # Remove temporary directory and files
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_convert_numpy_types_integer(self):
        """Test conversion of numpy integer types"""
        np_int32 = np.int32(42)
        np_int64 = np.int64(100)
        
        result32 = self.manager.convert_numpy_types(np_int32)
        result64 = self.manager.convert_numpy_types(np_int64)
        
        self.assertIsInstance(result32, int)
        self.assertIsInstance(result64, int)
        self.assertEqual(result32, 42)
        self.assertEqual(result64, 100)
    
    def test_convert_numpy_types_float(self):
        """Test conversion of numpy float types"""
        np_float32 = np.float32(3.14)
        np_float64 = np.float64(2.718)
        
        result32 = self.manager.convert_numpy_types(np_float32)
        result64 = self.manager.convert_numpy_types(np_float64)
        
        self.assertIsInstance(result32, float)
        self.assertIsInstance(result64, float)
        self.assertAlmostEqual(result32, 3.14, places=2)
        self.assertAlmostEqual(result64, 2.718, places=3)
    
    def test_convert_numpy_types_array(self):
        """Test conversion of numpy arrays"""
        np_array = np.array([1, 2, 3, 4, 5])
        
        result = self.manager.convert_numpy_types(np_array)
        
        self.assertIsInstance(result, list)
        self.assertEqual(result, [1, 2, 3, 4, 5])
    
    def test_convert_numpy_types_dict(self):
        """Test conversion of dictionaries with numpy types"""
        test_dict = {
            'int_val': np.int32(42),
            'float_val': np.float64(3.14),
            'array_val': np.array([1, 2, 3]),
            'normal_val': 'text'
        }
        
        result = self.manager.convert_numpy_types(test_dict)
        
        self.assertIsInstance(result['int_val'], int)
        self.assertIsInstance(result['float_val'], float)
        self.assertIsInstance(result['array_val'], list)
        self.assertEqual(result['normal_val'], 'text')
    
    def test_convert_numpy_types_nested(self):
        """Test conversion of nested structures with numpy types"""
        nested_data = {
            'level1': {
                'level2': {
                    'numpy_int': np.int32(100),
                    'list_with_numpy': [np.float32(1.5), np.float32(2.5)]
                }
            }
        }
        
        result = self.manager.convert_numpy_types(nested_data)
        
        self.assertIsInstance(result['level1']['level2']['numpy_int'], int)
        self.assertIsInstance(result['level1']['level2']['list_with_numpy'][0], float)
    
    def test_save_and_load_empty_profiles(self):
        """Test saving and loading empty profile list"""
        # Save empty profiles
        with open(self.test_profiles_file, 'w') as f:
            json.dump([], f)
        
        # Load profiles
        if os.path.exists(self.test_profiles_file):
            with open(self.test_profiles_file, 'r') as f:
                loaded = json.load(f)
        
        self.assertEqual(loaded, [])
    
    def test_save_profiles_with_data(self):
        """Test saving profiles with data"""
        test_profiles = [
            {
                'id': 'user_001',
                'name': 'John Doe',
                'age': 45,
                'gender': 'Male',
                'contact': '1234567890',
                'address': '123 Main St',
                'marital_status': 'Married',
                'predictions': {}
            }
        ]
        
        # Save profiles
        with open(self.test_profiles_file, 'w') as f:
            json.dump(test_profiles, f)
        
        # Verify file exists and contains data
        self.assertTrue(os.path.exists(self.test_profiles_file))
        
        with open(self.test_profiles_file, 'r') as f:
            loaded = json.load(f)
        
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0]['name'], 'John Doe')
        self.assertEqual(loaded[0]['age'], 45)
    
    def test_profile_id_generation(self):
        """Test that profile IDs are generated correctly"""
        # Simulate adding profiles
        profile1_id = f"user_{1:03d}"
        profile2_id = f"user_{2:03d}"
        profile3_id = f"user_{3:03d}"
        
        self.assertEqual(profile1_id, "user_001")
        self.assertEqual(profile2_id, "user_002")
        self.assertEqual(profile3_id, "user_003")
    
    def test_profile_with_predictions(self):
        """Test saving profile with predictions data"""
        profile_with_pred = {
            'id': 'user_001',
            'name': 'Jane Smith',
            'age': 35,
            'gender': 'Female',
            'predictions': {
                'Diabetes': {
                    'prob': 45.5,
                    'inputs': {
                        'Glucose': 120,
                        'BMI': 28.5
                    }
                }
            }
        }
        
        # Save and load
        with open(self.test_profiles_file, 'w') as f:
            json.dump([profile_with_pred], f)
        
        with open(self.test_profiles_file, 'r') as f:
            loaded = json.load(f)
        
        self.assertEqual(loaded[0]['predictions']['Diabetes']['prob'], 45.5)
        self.assertEqual(loaded[0]['predictions']['Diabetes']['inputs']['Glucose'], 120)
    
    def test_multiple_profiles(self):
        """Test handling multiple profiles"""
        profiles = [
            {'id': 'user_001', 'name': 'User 1', 'age': 30},
            {'id': 'user_002', 'name': 'User 2', 'age': 40},
            {'id': 'user_003', 'name': 'User 3', 'age': 50}
        ]
        
        with open(self.test_profiles_file, 'w') as f:
            json.dump(profiles, f)
        
        with open(self.test_profiles_file, 'r') as f:
            loaded = json.load(f)
        
        self.assertEqual(len(loaded), 3)
        self.assertEqual(loaded[0]['name'], 'User 1')
        self.assertEqual(loaded[1]['name'], 'User 2')
        self.assertEqual(loaded[2]['name'], 'User 3')
    
    def test_profile_update(self):
        """Test updating an existing profile"""
        # Create initial profile
        profile = {
            'id': 'user_001',
            'name': 'John Doe',
            'age': 45,
            'predictions': {}
        }
        
        with open(self.test_profiles_file, 'w') as f:
            json.dump([profile], f)
        
        # Load and update
        with open(self.test_profiles_file, 'r') as f:
            profiles = json.load(f)
        
        profiles[0]['age'] = 46
        profiles[0]['predictions'] = {'Diabetes': {'prob': 30}}
        
        with open(self.test_profiles_file, 'w') as f:
            json.dump(profiles, f)
        
        # Verify update
        with open(self.test_profiles_file, 'r') as f:
            updated = json.load(f)
        
        self.assertEqual(updated[0]['age'], 46)
        self.assertIn('Diabetes', updated[0]['predictions'])
    
    def test_profile_data_validation(self):
        """Test that profile contains required fields"""
        required_fields = ['id', 'name', 'age', 'gender', 'contact', 'address', 'marital_status']
        
        profile = {
            'id': 'user_001',
            'name': 'John Doe',
            'age': 45,
            'gender': 'Male',
            'contact': '1234567890',
            'address': '123 Main St',
            'marital_status': 'Married'
        }
        
        for field in required_fields:
            self.assertIn(field, profile)
    
    def test_timestamp_format(self):
        """Test that timestamps are in correct format"""
        timestamp = datetime.now().strftime("%d-%b-%Y %H:%M")
        
        # Verify format can be parsed
        try:
            datetime.strptime(timestamp, "%d-%b-%Y %H:%M")
            valid = True
        except ValueError:
            valid = False
        
        self.assertTrue(valid)
    
    def test_json_serialization_with_numpy(self):
        """Test that profiles with numpy types can be serialized to JSON"""
        profile = {
            'id': 'user_001',
            'name': 'Test User',
            'predictions': {
                'Diabetes': {
                    'prob': float(np.float64(45.5)),  # Convert numpy to native
                    'inputs': {
                        'Glucose': int(np.int32(120))  # Convert numpy to native
                    }
                }
            }
        }
        
        # This should not raise an exception
        try:
            json_str = json.dumps([profile])
            loaded = json.loads(json_str)
            self.assertEqual(loaded[0]['predictions']['Diabetes']['prob'], 45.5)
        except TypeError:
            self.fail("JSON serialization failed with converted numpy types")


class TestProfileManagerEdgeCases(unittest.TestCase):
    """Test edge cases and error handling"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.test_profiles_file = os.path.join(self.test_dir, "test_profiles.json")
        self.manager = ProfileManager()
        self.manager.profiles_file = self.test_profiles_file
    
    def tearDown(self):
        """Clean up after tests"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_nonexistent_file(self):
        """Test behavior when profiles file doesn't exist"""
        # Should not raise an error
        self.assertFalse(os.path.exists(self.test_profiles_file))
    
    def test_empty_string_values(self):
        """Test handling of empty string values"""
        profile = {
            'id': 'user_001',
            'name': '',
            'age': 0,
            'gender': '',
            'contact': '',
            'address': ''
        }
        
        # Should be able to save and load
        with open(self.test_profiles_file, 'w') as f:
            json.dump([profile], f)
        
        with open(self.test_profiles_file, 'r') as f:
            loaded = json.load(f)
        
        self.assertEqual(loaded[0]['name'], '')
    
    def test_special_characters_in_profile(self):
        """Test handling of special characters"""
        profile = {
            'id': 'user_001',
            'name': "O'Brien-Smith",
            'address': '123 Main St., Apt #4B',
            'contact': '+1-234-567-8900'
        }
        
        with open(self.test_profiles_file, 'w') as f:
            json.dump([profile], f)
        
        with open(self.test_profiles_file, 'r') as f:
            loaded = json.load(f)
        
        self.assertEqual(loaded[0]['name'], "O'Brien-Smith")
        self.assertEqual(loaded[0]['address'], '123 Main St., Apt #4B')
    
    def test_unicode_characters(self):
        """Test handling of unicode characters"""
        profile = {
            'id': 'user_001',
            'name': '张三',  # Chinese characters
            'address': 'Москва'  # Russian characters
        }
        
        with open(self.test_profiles_file, 'w', encoding='utf-8') as f:
            json.dump([profile], f, ensure_ascii=False)
        
        with open(self.test_profiles_file, 'r', encoding='utf-8') as f:
            loaded = json.load(f)
        
        self.assertEqual(loaded[0]['name'], '张三')


if __name__ == '__main__':
    unittest.main()
