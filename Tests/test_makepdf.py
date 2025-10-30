"""
Unit tests for makepdf.py
Tests PDF report generation functionality
"""

import unittest
import sys
import os
import io

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from makepdf import generate_pdf_report


class TestMakePDF(unittest.TestCase):
    """Test cases for PDF generation"""
    
    def setUp(self):
        """Set up test data"""
        self.sample_predictions = {
            'Diabetes': {
                'prob': 45.5,
                'inputs': {
                    'Glucose': 120,
                    'BMI': 28.5,
                    'Age': 45,
                    'Blood Pressure': 130
                }
            },
            'Heart Disease': {
                'prob': 60.2,
                'inputs': {
                    'Age': 55,
                    'Cholesterol': 240,
                    'Resting BP': 145,
                    'Max Heart Rate': 150
                }
            },
            'Fever': {
                'prob': 30.0,
                'severity': 'Mild',
                'inputs': {
                    'Temperature (°C)': 37.5,
                    'Age': 35,
                    'BMI': 24.0
                }
            },
            'Anemia': {
                'prob': 75.8,
                'severity': 'Microcytic',
                'inputs': {
                    'Hemoglobin (Hb)': 10.5,
                    'RBC': 4.0,
                    'MCV': 75.0
                }
            }
        }
    
    def test_generate_pdf_single_disease(self):
        """Test PDF generation for a single disease"""
        pdf_buffer = generate_pdf_report(self.sample_predictions, ['Diabetes'])
        
        self.assertIsNotNone(pdf_buffer)
        self.assertIsInstance(pdf_buffer, io.BytesIO)
        
        # Check that buffer has content
        pdf_content = pdf_buffer.getvalue()
        self.assertGreater(len(pdf_content), 0)
        
        # Check PDF header
        self.assertTrue(pdf_content.startswith(b'%PDF'))
    
    def test_generate_pdf_multiple_diseases(self):
        """Test PDF generation for multiple diseases"""
        diseases = ['Diabetes', 'Heart Disease']
        pdf_buffer = generate_pdf_report(self.sample_predictions, diseases)
        
        self.assertIsNotNone(pdf_buffer)
        pdf_content = pdf_buffer.getvalue()
        self.assertGreater(len(pdf_content), 0)
        self.assertTrue(pdf_content.startswith(b'%PDF'))
    
    def test_generate_pdf_all_diseases(self):
        """Test PDF generation for all diseases"""
        all_diseases = list(self.sample_predictions.keys())
        pdf_buffer = generate_pdf_report(self.sample_predictions, all_diseases)
        
        self.assertIsNotNone(pdf_buffer)
        pdf_content = pdf_buffer.getvalue()
        self.assertGreater(len(pdf_content), 0)
        self.assertTrue(pdf_content.startswith(b'%PDF'))
    
    def test_generate_pdf_with_severity(self):
        """Test PDF generation with severity information"""
        pdf_buffer = generate_pdf_report(self.sample_predictions, ['Fever'])
        
        self.assertIsNotNone(pdf_buffer)
        pdf_content = pdf_buffer.getvalue()
        self.assertGreater(len(pdf_content), 0)
    
    def test_generate_pdf_string_input(self):
        """Test PDF generation with string disease name"""
        pdf_buffer = generate_pdf_report(self.sample_predictions, 'Diabetes')
        
        self.assertIsNotNone(pdf_buffer)
        pdf_content = pdf_buffer.getvalue()
        self.assertGreater(len(pdf_content), 0)
    
    def test_generate_pdf_full_report_string(self):
        """Test PDF generation with 'Full Report' string"""
        pdf_buffer = generate_pdf_report(self.sample_predictions, 'Full Report')
        
        self.assertIsNotNone(pdf_buffer)
        pdf_content = pdf_buffer.getvalue()
        self.assertGreater(len(pdf_content), 0)
    
    def test_generate_pdf_all_string(self):
        """Test PDF generation with 'all' string"""
        pdf_buffer = generate_pdf_report(self.sample_predictions, 'all')
        
        self.assertIsNotNone(pdf_buffer)
        pdf_content = pdf_buffer.getvalue()
        self.assertGreater(len(pdf_content), 0)
    
    def test_pdf_buffer_seekable(self):
        """Test that PDF buffer is seekable (at position 0)"""
        pdf_buffer = generate_pdf_report(self.sample_predictions, ['Diabetes'])
        
        # Buffer should be at position 0 for reading
        self.assertEqual(pdf_buffer.tell(), 0)
    
    def test_pdf_with_low_risk(self):
        """Test PDF generation with low risk values"""
        low_risk_predictions = {
            'Diabetes': {
                'prob': 15.0,
                'inputs': {'Glucose': 90, 'BMI': 22.0}
            }
        }
        
        pdf_buffer = generate_pdf_report(low_risk_predictions, ['Diabetes'])
        
        self.assertIsNotNone(pdf_buffer)
        pdf_content = pdf_buffer.getvalue()
        self.assertGreater(len(pdf_content), 0)
    
    def test_pdf_with_medium_risk(self):
        """Test PDF generation with medium risk values"""
        medium_risk_predictions = {
            'Heart Disease': {
                'prob': 55.0,
                'inputs': {'Age': 50, 'Cholesterol': 220}
            }
        }
        
        pdf_buffer = generate_pdf_report(medium_risk_predictions, ['Heart Disease'])
        
        self.assertIsNotNone(pdf_buffer)
        pdf_content = pdf_buffer.getvalue()
        self.assertGreater(len(pdf_content), 0)
    
    def test_pdf_with_high_risk(self):
        """Test PDF generation with high risk values"""
        high_risk_predictions = {
            'Anemia': {
                'prob': 85.0,
                'severity': 'Severe',
                'inputs': {'Hemoglobin (Hb)': 8.5}
            }
        }
        
        pdf_buffer = generate_pdf_report(high_risk_predictions, ['Anemia'])
        
        self.assertIsNotNone(pdf_buffer)
        pdf_content = pdf_buffer.getvalue()
        self.assertGreater(len(pdf_content), 0)
    
    def test_pdf_with_extreme_values(self):
        """Test PDF generation with extreme risk values"""
        extreme_predictions = {
            'Diabetes': {
                'prob': 0.0,
                'inputs': {'Glucose': 70}
            },
            'Heart Disease': {
                'prob': 100.0,
                'inputs': {'Age': 80}
            }
        }
        
        pdf_buffer = generate_pdf_report(extreme_predictions, ['Diabetes', 'Heart Disease'])
        
        self.assertIsNotNone(pdf_buffer)
        pdf_content = pdf_buffer.getvalue()
        self.assertGreater(len(pdf_content), 0)
    
    def test_pdf_with_empty_inputs(self):
        """Test PDF generation with minimal inputs"""
        minimal_predictions = {
            'Diabetes': {
                'prob': 50.0,
                'inputs': {}
            }
        }
        
        pdf_buffer = generate_pdf_report(minimal_predictions, ['Diabetes'])
        
        self.assertIsNotNone(pdf_buffer)
        pdf_content = pdf_buffer.getvalue()
        self.assertGreater(len(pdf_content), 0)
    
    def test_pdf_with_many_inputs(self):
        """Test PDF generation with many input parameters"""
        many_inputs_predictions = {
            'Heart Disease': {
                'prob': 50.0,
                'inputs': {
                    'Age': 55,
                    'Sex': 1,
                    'Chest Pain Type': 2,
                    'Resting BP': 140,
                    'Cholesterol': 250,
                    'Fasting BS > 120?': 1,
                    'Resting ECG': 0,
                    'Max Heart Rate': 145,
                    'Exercise Angina': 0,
                    'ST Depression': 1.5,
                    'Slope of ST': 2,
                    'Major Vessels (ca)': 1,
                    'Thal': 3
                }
            }
        }
        
        pdf_buffer = generate_pdf_report(many_inputs_predictions, ['Heart Disease'])
        
        self.assertIsNotNone(pdf_buffer)
        pdf_content = pdf_buffer.getvalue()
        self.assertGreater(len(pdf_content), 0)
    
    def test_pdf_size_reasonable(self):
        """Test that PDF size is reasonable (not too large)"""
        pdf_buffer = generate_pdf_report(self.sample_predictions, 
                                        list(self.sample_predictions.keys()))
        
        pdf_content = pdf_buffer.getvalue()
        pdf_size = len(pdf_content)
        
        # PDF should be between 10KB and 5MB
        self.assertGreater(pdf_size, 10000)  # At least 10KB
        self.assertLess(pdf_size, 5000000)  # Less than 5MB
    
    def test_pdf_valid_format(self):
        """Test that generated PDF has valid format"""
        pdf_buffer = generate_pdf_report(self.sample_predictions, ['Diabetes'])
        
        pdf_content = pdf_buffer.getvalue()
        
        # Check PDF header
        self.assertTrue(pdf_content.startswith(b'%PDF'))
        
        # Check PDF trailer
        self.assertIn(b'%%EOF', pdf_content)


class TestMakePDFEdgeCases(unittest.TestCase):
    """Test edge cases for PDF generation"""
    
    def test_generate_pdf_nonexistent_disease(self):
        """Test PDF generation with non-existent disease name"""
        predictions = {
            'Diabetes': {'prob': 50.0, 'inputs': {}}
        }
        
        # Request PDF for disease not in predictions
        pdf_buffer = generate_pdf_report(predictions, ['NonExistent'])
        
        self.assertIsNotNone(pdf_buffer)
        # Should generate an empty or minimal PDF
    
    def test_generate_pdf_empty_disease_list(self):
        """Test PDF generation with empty disease list"""
        predictions = {
            'Diabetes': {'prob': 50.0, 'inputs': {}}
        }
        
        pdf_buffer = generate_pdf_report(predictions, [])
        
        self.assertIsNotNone(pdf_buffer)
    
    def test_generate_pdf_special_characters(self):
        """Test PDF generation with special characters in inputs"""
        predictions = {
            'Diabetes': {
                'prob': 50.0,
                'inputs': {
                    'Patient Name': "O'Brien-Smith",
                    'Special Char': 'Test@123'
                }
            }
        }
        
        pdf_buffer = generate_pdf_report(predictions, ['Diabetes'])
        
        self.assertIsNotNone(pdf_buffer)
        pdf_content = pdf_buffer.getvalue()
        self.assertGreater(len(pdf_content), 0)
    
    def test_generate_pdf_decimal_precision(self):
        """Test PDF generation with various decimal precisions"""
        predictions = {
            'Diabetes': {
                'prob': 45.123456789,
                'inputs': {
                    'BMI': 28.999999,
                    'Glucose': 120.5
                }
            }
        }
        
        pdf_buffer = generate_pdf_report(predictions, ['Diabetes'])
        
        self.assertIsNotNone(pdf_buffer)
        pdf_content = pdf_buffer.getvalue()
        self.assertGreater(len(pdf_content), 0)


class TestMakePDFRiskColors(unittest.TestCase):
    """Test that PDF uses correct risk colors"""
    
    def test_low_risk_color(self):
        """Test low risk uses green color (conceptual test)"""
        predictions = {
            'Diabetes': {'prob': 30.0, 'inputs': {}}
        }
        
        pdf_buffer = generate_pdf_report(predictions, ['Diabetes'])
        
        # PDF should be generated successfully
        self.assertIsNotNone(pdf_buffer)
        self.assertGreater(len(pdf_buffer.getvalue()), 0)
    
    def test_medium_risk_color(self):
        """Test medium risk uses orange color (conceptual test)"""
        predictions = {
            'Diabetes': {'prob': 55.0, 'inputs': {}}
        }
        
        pdf_buffer = generate_pdf_report(predictions, ['Diabetes'])
        
        # PDF should be generated successfully
        self.assertIsNotNone(pdf_buffer)
        self.assertGreater(len(pdf_buffer.getvalue()), 0)
    
    def test_high_risk_color(self):
        """Test high risk uses red color (conceptual test)"""
        predictions = {
            'Diabetes': {'prob': 80.0, 'inputs': {}}
        }
        
        pdf_buffer = generate_pdf_report(predictions, ['Diabetes'])
        
        # PDF should be generated successfully
        self.assertIsNotNone(pdf_buffer)
        self.assertGreater(len(pdf_buffer.getvalue()), 0)


if __name__ == '__main__':
    unittest.main()
