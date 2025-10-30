"""
Unit tests for helper.py
Tests the disease recommendation system based on risk levels
"""

import unittest
import sys
import os

# Add parent directory to path to import helper module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from helper import fetch_gemini_recommendations


class TestHelperRecommendations(unittest.TestCase):
    """Test cases for fetch_gemini_recommendations function"""
    
    def test_diabetes_low_risk(self):
        """Test diabetes recommendations for low risk (<35%)"""
        result = fetch_gemini_recommendations("Diabetes", 20)
        
        self.assertEqual(result["Risk Level"], "low")
        self.assertIn("prevention_measures", result)
        self.assertIn("medicine_suggestions", result)
        self.assertEqual(len(result["prevention_measures"]), 4)
        self.assertEqual(len(result["medicine_suggestions"]), 4)
        
        # Verify preventions are non-empty
        for prevention in result["prevention_measures"]:
            self.assertIsInstance(prevention, str)
            self.assertGreater(len(prevention), 0)
        
        # Verify medicines are non-empty
        for medicine in result["medicine_suggestions"]:
            self.assertIsInstance(medicine, str)
            self.assertGreater(len(medicine), 0)
    
    def test_diabetes_medium_risk(self):
        """Test diabetes recommendations for medium risk (35-70%)"""
        result = fetch_gemini_recommendations("Diabetes", 50)
        
        self.assertEqual(result["Risk Level"], "medium")
        self.assertEqual(len(result["prevention_measures"]), 6)
        self.assertEqual(len(result["medicine_suggestions"]), 6)
    
    def test_diabetes_high_risk(self):
        """Test diabetes recommendations for high risk (>=70%)"""
        result = fetch_gemini_recommendations("Diabetes", 85)
        
        self.assertEqual(result["Risk Level"], "high")
        self.assertEqual(len(result["prevention_measures"]), 8)
        self.assertEqual(len(result["medicine_suggestions"]), 8)
    
    def test_heart_disease_low_risk(self):
        """Test heart disease recommendations for low risk"""
        result = fetch_gemini_recommendations("Heart Disease", 25)
        
        self.assertEqual(result["Risk Level"], "low")
        self.assertEqual(len(result["prevention_measures"]), 4)
        self.assertEqual(len(result["medicine_suggestions"]), 4)
    
    def test_heart_disease_medium_risk(self):
        """Test heart disease recommendations for medium risk"""
        result = fetch_gemini_recommendations("Heart Disease", 55)
        
        self.assertEqual(result["Risk Level"], "medium")
        self.assertEqual(len(result["prevention_measures"]), 6)
        self.assertEqual(len(result["medicine_suggestions"]), 6)
    
    def test_heart_disease_high_risk(self):
        """Test heart disease recommendations for high risk"""
        result = fetch_gemini_recommendations("Heart Disease", 90)
        
        self.assertEqual(result["Risk Level"], "high")
        self.assertEqual(len(result["prevention_measures"]), 8)
        self.assertEqual(len(result["medicine_suggestions"]), 8)
    
    def test_fever_low_risk(self):
        """Test fever recommendations for low risk"""
        result = fetch_gemini_recommendations("Fever", 15)
        
        self.assertEqual(result["Risk Level"], "low")
        self.assertEqual(len(result["prevention_measures"]), 4)
        self.assertEqual(len(result["medicine_suggestions"]), 4)
    
    def test_fever_medium_risk(self):
        """Test fever recommendations for medium risk"""
        result = fetch_gemini_recommendations("Fever", 45)
        
        self.assertEqual(result["Risk Level"], "medium")
        self.assertEqual(len(result["prevention_measures"]), 6)
        self.assertEqual(len(result["medicine_suggestions"]), 6)
    
    def test_fever_high_risk(self):
        """Test fever recommendations for high risk"""
        result = fetch_gemini_recommendations("Fever", 75)
        
        self.assertEqual(result["Risk Level"], "high")
        self.assertEqual(len(result["prevention_measures"]), 8)
        self.assertEqual(len(result["medicine_suggestions"]), 8)
    
    def test_anemia_low_risk(self):
        """Test anemia recommendations for low risk"""
        result = fetch_gemini_recommendations("Anemia", 30)
        
        self.assertEqual(result["Risk Level"], "low")
        self.assertEqual(len(result["prevention_measures"]), 4)
        self.assertEqual(len(result["medicine_suggestions"]), 4)
    
    def test_anemia_medium_risk(self):
        """Test anemia recommendations for medium risk"""
        result = fetch_gemini_recommendations("Anemia", 60)
        
        self.assertEqual(result["Risk Level"], "medium")
        self.assertEqual(len(result["prevention_measures"]), 6)
        self.assertEqual(len(result["medicine_suggestions"]), 6)
    
    def test_anemia_high_risk(self):
        """Test anemia recommendations for high risk"""
        result = fetch_gemini_recommendations("Anemia", 95)
        
        self.assertEqual(result["Risk Level"], "high")
        self.assertEqual(len(result["prevention_measures"]), 8)
        self.assertEqual(len(result["medicine_suggestions"]), 8)
    
    def test_case_insensitivity(self):
        """Test that disease names are case-insensitive"""
        result_lower = fetch_gemini_recommendations("diabetes", 50)
        result_upper = fetch_gemini_recommendations("DIABETES", 50)
        result_mixed = fetch_gemini_recommendations("DiAbEtEs", 50)
        
        self.assertEqual(result_lower["Risk Level"], "medium")
        self.assertEqual(result_upper["Risk Level"], "medium")
        self.assertEqual(result_mixed["Risk Level"], "medium")
    
    def test_boundary_values(self):
        """Test boundary values for risk thresholds"""
        # Test at exact boundary (35%)
        result_34 = fetch_gemini_recommendations("Diabetes", 34)
        result_35 = fetch_gemini_recommendations("Diabetes", 35)
        
        self.assertEqual(result_34["Risk Level"], "low")
        self.assertEqual(result_35["Risk Level"], "medium")
        
        # Test at exact boundary (70%)
        result_69 = fetch_gemini_recommendations("Diabetes", 69)
        result_70 = fetch_gemini_recommendations("Diabetes", 70)
        
        self.assertEqual(result_69["Risk Level"], "medium")
        self.assertEqual(result_70["Risk Level"], "high")
    
    def test_extreme_values(self):
        """Test extreme risk values"""
        result_zero = fetch_gemini_recommendations("Diabetes", 0)
        result_hundred = fetch_gemini_recommendations("Diabetes", 100)
        
        self.assertEqual(result_zero["Risk Level"], "low")
        self.assertEqual(result_hundred["Risk Level"], "high")
    
    def test_unknown_disease(self):
        """Test behavior with unknown disease name"""
        result = fetch_gemini_recommendations("Unknown Disease", 50)
        
        # Should return empty lists for unknown diseases
        self.assertEqual(result["prevention_measures"], [])
        self.assertEqual(result["medicine_suggestions"], [])
    
    def test_all_diseases_have_recommendations(self):
        """Test that all supported diseases have recommendations at all risk levels"""
        diseases = ["Diabetes", "Heart Disease", "Fever", "Anemia"]
        risk_levels = [20, 50, 80]  # low, medium, high
        
        for disease in diseases:
            for risk in risk_levels:
                result = fetch_gemini_recommendations(disease, risk)
                self.assertGreater(len(result["prevention_measures"]), 0,
                                 f"{disease} at risk {risk} should have preventions")
                self.assertGreater(len(result["medicine_suggestions"]), 0,
                                 f"{disease} at risk {risk} should have medicines")


class TestHelperRecommendationsContent(unittest.TestCase):
    """Test the actual content quality of recommendations"""
    
    def test_recommendations_are_relevant(self):
        """Test that recommendations contain disease-related keywords"""
        result = fetch_gemini_recommendations("Diabetes", 50)
        
        # Combine all text
        all_text = " ".join(result["prevention_measures"] + result["medicine_suggestions"]).lower()
        
        # Check for diabetes-related terms
        diabetes_terms = ["glucose", "blood sugar", "insulin", "diet", "exercise"]
        has_relevant_term = any(term in all_text for term in diabetes_terms)
        self.assertTrue(has_relevant_term, "Recommendations should contain diabetes-related terms")
    
    def test_recommendations_increase_with_risk(self):
        """Test that higher risk levels provide more detailed recommendations"""
        low_risk = fetch_gemini_recommendations("Diabetes", 20)
        high_risk = fetch_gemini_recommendations("Diabetes", 80)
        
        # High risk should have more recommendations
        self.assertGreater(
            len(high_risk["prevention_measures"]),
            len(low_risk["prevention_measures"])
        )
        self.assertGreater(
            len(high_risk["medicine_suggestions"]),
            len(low_risk["medicine_suggestions"])
        )


if __name__ == '__main__':
    unittest.main()
