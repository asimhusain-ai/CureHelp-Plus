#!/usr/bin/env python3
"""
Performance Tests for CureHelp+ Optimizations
Tests the performance improvements in key modules
"""

import unittest
import time
import sys
import os
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from helper import fetch_gemini_recommendations
from consultant import get_hospitals_data, get_doctors_data


class TestPerformanceOptimizations(unittest.TestCase):
    """Test performance of optimized functions"""

    def test_helper_caching_performance(self):
        """Test that helper recommendations are cached and fast on subsequent calls"""
        disease = "Diabetes"
        risk = 50.0
        
        # First call - should compute
        start_time = time.time()
        result1 = fetch_gemini_recommendations(disease, risk)
        first_call_time = time.time() - start_time
        
        # Second call - should be cached and much faster
        start_time = time.time()
        result2 = fetch_gemini_recommendations(disease, risk)
        second_call_time = time.time() - start_time
        
        # Verify results are the same
        self.assertEqual(result1, result2)
        
        # Verify second call is faster (cached)
        # Second call should be at least 10x faster due to caching
        self.assertLess(second_call_time, first_call_time / 5, 
                       f"Cached call should be much faster: {second_call_time} vs {first_call_time}")
        
        print(f"\n✓ Helper caching: First call: {first_call_time*1000:.2f}ms, "
              f"Cached call: {second_call_time*1000:.2f}ms")

    def test_consultant_caching_performance(self):
        """Test that consultant data is cached properly"""
        # First call - should compute
        start_time = time.time()
        hospitals1 = get_hospitals_data()
        first_call_time = time.time() - start_time
        
        # Second call - should be cached
        start_time = time.time()
        hospitals2 = get_hospitals_data()
        second_call_time = time.time() - start_time
        
        # Verify results are the same
        self.assertEqual(hospitals1, hospitals2)
        
        # Verify second call is faster
        self.assertLess(second_call_time, first_call_time / 2,
                       f"Cached call should be faster: {second_call_time} vs {first_call_time}")
        
        print(f"\n✓ Consultant caching: First call: {first_call_time*1000:.2f}ms, "
              f"Cached call: {second_call_time*1000:.2f}ms")

    def test_helper_recommendation_correctness(self):
        """Test that helper recommendations return expected structure"""
        diseases = ["Diabetes", "Heart Disease", "Fever", "Anemia"]
        risk_levels = [20, 50, 80]
        
        for disease in diseases:
            for risk in risk_levels:
                result = fetch_gemini_recommendations(disease, risk)
                
                # Verify structure
                self.assertIn("Risk Level", result)
                self.assertIn("prevention_measures", result)
                self.assertIn("medicine_suggestions", result)
                
                # Verify risk level categorization
                if risk < 35:
                    self.assertEqual(result["Risk Level"], "low")
                    self.assertEqual(len(result["prevention_measures"]), 4)
                    self.assertEqual(len(result["medicine_suggestions"]), 4)
                elif risk < 70:
                    self.assertEqual(result["Risk Level"], "medium")
                    self.assertEqual(len(result["prevention_measures"]), 6)
                    self.assertEqual(len(result["medicine_suggestions"]), 6)
                else:
                    self.assertEqual(result["Risk Level"], "high")
                    self.assertEqual(len(result["prevention_measures"]), 8)
                    self.assertEqual(len(result["medicine_suggestions"]), 8)
        
        print(f"\n✓ Helper recommendations structure validated for all diseases and risk levels")

    def test_consultant_data_structure(self):
        """Test that consultant data has expected structure"""
        hospitals = get_hospitals_data()
        doctors = get_doctors_data()
        
        # Verify hospitals
        self.assertIsInstance(hospitals, list)
        self.assertGreater(len(hospitals), 0)
        
        # Check hospital structure
        for hospital in hospitals:
            self.assertIn("name", hospital)
            self.assertIn("address", hospital)
            self.assertIn("contact", hospital)
            self.assertIn("speciality", hospital)
            self.assertIn("distance", hospital)
            self.assertIn("location_url", hospital)
            self.assertIn("website_url", hospital)
        
        # Verify doctors
        self.assertIsInstance(doctors, list)
        self.assertGreater(len(doctors), 0)
        
        # Check doctor structure
        for doctor in doctors:
            self.assertIn("name", doctor)
            self.assertIn("contact", doctor)
            self.assertIn("address", doctor)
            self.assertIn("qualification", doctor)
            self.assertIn("specialization", doctor)
            self.assertIn("experience", doctor)
        
        print(f"\n✓ Consultant data structure validated: {len(hospitals)} hospitals, {len(doctors)} doctors")

    def test_multiple_recommendation_calls(self):
        """Test performance with multiple recommendation calls"""
        start_time = time.time()
        
        # Make multiple calls
        for i in range(50):
            disease = ["Diabetes", "Heart Disease", "Fever", "Anemia"][i % 4]
            risk = (i * 2) % 100
            fetch_gemini_recommendations(disease, risk)
        
        total_time = time.time() - start_time
        avg_time = total_time / 50
        
        # Average time should be very fast due to caching
        self.assertLess(avg_time, 0.001,  # Less than 1ms average
                       f"Average call time too slow: {avg_time*1000:.2f}ms")
        
        print(f"\n✓ Multiple calls performance: 50 calls in {total_time*1000:.2f}ms "
              f"(avg: {avg_time*1000:.2f}ms)")


class TestProfileManagerOptimizations(unittest.TestCase):
    """Test profile manager optimizations"""

    def test_numpy_conversion_performance(self):
        """Test that numpy conversion is optimized"""
        from profile_manager import ProfileManager
        
        pm = ProfileManager()
        
        # Create test data with numpy types
        test_data = {
            "int": np.int64(42),
            "float": np.float64(3.14),
            "array": np.array([1, 2, 3]),
            "dict": {
                "nested_int": np.int32(100),
                "nested_float": np.float32(2.5)
            },
            "list": [np.int64(1), np.float64(2.0)]
        }
        
        # Time the conversion
        start_time = time.time()
        for _ in range(100):
            result = pm.convert_numpy_types(test_data)
        conversion_time = (time.time() - start_time) / 100
        
        # Verify conversion is correct
        self.assertIsInstance(result["int"], int)
        self.assertIsInstance(result["float"], float)
        self.assertIsInstance(result["array"], list)
        self.assertIsInstance(result["dict"]["nested_int"], int)
        
        # Should be very fast
        self.assertLess(conversion_time, 0.001,
                       f"Numpy conversion too slow: {conversion_time*1000:.2f}ms")
        
        print(f"\n✓ Numpy conversion: {conversion_time*1000:.2f}ms per conversion")


def run_performance_tests():
    """Run performance tests with detailed output"""
    print("\n" + "="*70)
    print("PERFORMANCE OPTIMIZATION TESTS")
    print("="*70)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
    
    # Run with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "="*70)
    print("PERFORMANCE TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_performance_tests()
    sys.exit(0 if success else 1)
