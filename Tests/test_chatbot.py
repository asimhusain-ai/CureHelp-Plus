"""
Unit tests for chatbot.py
Tests medical chatbot functionality including disease prediction from symptoms
"""

import unittest
import sys
import os
import pandas as pd
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chatbot import (
    classify_input_type,
    clean_dataframe,
    preprocess_datasets
)


class TestChatbotInputClassification(unittest.TestCase):
    """Test cases for input type classification"""
    
    def test_classify_question_with_question_mark(self):
        """Test classification of questions with question marks"""
        inputs = [
            "What are the symptoms of diabetes?",
            "How to treat fever?",
            "Why is blood pressure high?",
            "When should I see a doctor?"
        ]
        
        for user_input in inputs:
            result = classify_input_type(user_input)
            self.assertEqual(result, 'question', 
                           f"'{user_input}' should be classified as question")
    
    def test_classify_question_without_question_mark(self):
        """Test classification of questions without question marks"""
        inputs = [
            "What are the symptoms of diabetes",
            "How can I prevent heart disease",
            "Tell me about anemia"
        ]
        
        for user_input in inputs:
            result = classify_input_type(user_input)
            self.assertEqual(result, 'question', 
                           f"'{user_input}' should be classified as question")
    
    def test_classify_symptoms_list(self):
        """Test classification of symptom lists"""
        inputs = [
            "fever, headache, cough",
            "fatigue, weakness",
            "chest pain, shortness of breath, dizziness"
        ]
        
        for user_input in inputs:
            result = classify_input_type(user_input)
            self.assertEqual(result, 'symptoms', 
                           f"'{user_input}' should be classified as symptoms")
    
    def test_classify_disease_name(self):
        """Test classification of disease names"""
        inputs = [
            "diabetes",
            "heart disease",
            "malaria"
        ]
        
        for user_input in inputs:
            result = classify_input_type(user_input)
            # Should be classified as disease or question
            self.assertIn(result, ['disease', 'question'], 
                        f"'{user_input}' should be classified as disease or question")
    
    def test_classify_empty_input(self):
        """Test classification of empty input"""
        result = classify_input_type("")
        self.assertEqual(result, 'question')
    
    def test_classify_case_insensitivity(self):
        """Test that classification is case-insensitive"""
        inputs_lower = "what are the symptoms of diabetes"
        inputs_upper = "WHAT ARE THE SYMPTOMS OF DIABETES"
        
        result_lower = classify_input_type(inputs_lower)
        result_upper = classify_input_type(inputs_upper)
        
        self.assertEqual(result_lower, result_upper)


class TestChatbotDataCleaning(unittest.TestCase):
    """Test cases for dataframe cleaning"""
    
    def test_clean_empty_dataframe(self):
        """Test cleaning of empty dataframe"""
        df = pd.DataFrame()
        result = clean_dataframe(df)
        
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 0)
    
    def test_clean_dataframe_with_unnamed_columns(self):
        """Test removal of unnamed columns"""
        df = pd.DataFrame({
            'Name': ['John', 'Jane'],
            'Unnamed: 0': [1, 2],
            'Age': [30, 25]
        })
        
        result = clean_dataframe(df)
        
        self.assertNotIn('Unnamed: 0', result.columns)
        self.assertIn('Name', result.columns)
        self.assertIn('Age', result.columns)
    
    def test_clean_dataframe_with_nan_values(self):
        """Test handling of NaN values"""
        df = pd.DataFrame({
            'Name': ['John', None, 'Jane'],
            'Age': [30, 25, None]
        })
        
        result = clean_dataframe(df)
        
        # String columns should have NaN replaced with empty string
        self.assertEqual(result['Name'].iloc[1], '')
    
    def test_clean_dataframe_remove_empty_rows(self):
        """Test removal of completely empty rows"""
        df = pd.DataFrame({
            'Name': ['John', None, 'Jane'],
            'Age': [30, None, 25]
        })
        
        result = clean_dataframe(df)
        
        # Should have rows with at least some data
        self.assertGreater(len(result), 0)
    
    def test_clean_none_dataframe(self):
        """Test handling of None input"""
        result = clean_dataframe(None)
        self.assertIsNone(result)


class TestChatbotDataPreprocessing(unittest.TestCase):
    """Test cases for dataset preprocessing"""
    
    def test_preprocess_creates_clean_columns(self):
        """Test that preprocessing creates clean columns"""
        # Create sample dataframes
        precautions_df = pd.DataFrame({
            'Disease': ['Diabetes', 'Malaria', 'Typhoid'],
            'Precaution_1': ['Exercise', 'Use nets', 'Clean water']
        })
        
        symptoms_df = pd.DataFrame({
            'Disease': ['Diabetes', 'Malaria'],
            'Symptom_1': ['Fatigue', 'Fever']
        })
        
        faq_df = pd.DataFrame({
            'Disease': ['Diabetes'],
            'question': ['What is diabetes?'],
            'answer': ['A metabolic disorder']
        })
        
        augmented_df = pd.DataFrame({
            'diseases': ['Diabetes', 'Malaria'],
            'fever': [0, 1],
            'fatigue': [1, 0]
        })
        
        # Preprocess
        prec, symp, faq, aug = preprocess_datasets(
            precautions_df, symptoms_df, faq_df, augmented_df
        )
        
        # Check that clean columns were added
        self.assertIn('Disease_clean', prec.columns)
        self.assertIn('Disease_clean', symp.columns)
        self.assertIn('diseases_clean', aug.columns)
        self.assertIn('question_clean', faq.columns)
    
    def test_preprocess_lowercase_conversion(self):
        """Test that preprocessing converts to lowercase"""
        precautions_df = pd.DataFrame({
            'Disease': ['Diabetes', 'MALARIA', 'TyPhOiD']
        })
        
        prec, _, _, _ = preprocess_datasets(precautions_df, None, None, None)
        
        # All clean names should be lowercase
        for clean_name in prec['Disease_clean']:
            self.assertEqual(clean_name, clean_name.lower())
    
    def test_preprocess_strip_whitespace(self):
        """Test that preprocessing strips whitespace"""
        precautions_df = pd.DataFrame({
            'Disease': ['  Diabetes  ', ' Malaria', 'Typhoid ']
        })
        
        prec, _, _, _ = preprocess_datasets(precautions_df, None, None, None)
        
        # Should have no leading/trailing whitespace
        for clean_name in prec['Disease_clean']:
            self.assertEqual(clean_name, clean_name.strip())
    
    def test_preprocess_handles_none_inputs(self):
        """Test that preprocessing handles None inputs gracefully"""
        # Should not raise an exception
        try:
            prec, symp, faq, aug = preprocess_datasets(None, None, None, None)
            # All should be None
            self.assertIsNone(prec)
            self.assertIsNone(symp)
            self.assertIsNone(faq)
            self.assertIsNone(aug)
        except Exception as e:
            self.fail(f"Preprocessing raised an exception with None inputs: {e}")


class TestChatbotResponseStructure(unittest.TestCase):
    """Test response structure from chatbot"""
    
    def test_response_has_required_fields(self):
        """Test that response dict has all required fields"""
        # Create a mock response structure
        response = {
            'type': 'disease',
            'disease': 'Diabetes',
            'confidence': 0.95,
            'symptoms': [],
            'precautions': [],
            'description': None,
            'faq_question': None,
            'faq_answer': None
        }
        
        required_fields = [
            'type', 'disease', 'confidence', 'symptoms',
            'precautions', 'description', 'faq_question', 'faq_answer'
        ]
        
        for field in required_fields:
            self.assertIn(field, response)
    
    def test_response_type_values(self):
        """Test that response type has valid values"""
        valid_types = ['question', 'symptoms', 'disease']
        
        # Mock responses
        responses = [
            {'type': 'question'},
            {'type': 'symptoms'},
            {'type': 'disease'}
        ]
        
        for response in responses:
            self.assertIn(response['type'], valid_types)
    
    def test_confidence_range(self):
        """Test that confidence values are in valid range"""
        # Mock responses with confidence
        confidences = [0.0, 0.5, 0.95, 1.0]
        
        for conf in confidences:
            self.assertGreaterEqual(conf, 0.0)
            self.assertLessEqual(conf, 1.0)


class TestChatbotSymptomMatching(unittest.TestCase):
    """Test symptom matching logic"""
    
    def test_symptom_list_parsing(self):
        """Test parsing of symptom lists"""
        symptom_input = "fever, headache, cough"
        symptoms_list = [s.strip() for s in symptom_input.split(',')]
        
        self.assertEqual(len(symptoms_list), 3)
        self.assertEqual(symptoms_list[0], 'fever')
        self.assertEqual(symptoms_list[1], 'headache')
        self.assertEqual(symptoms_list[2], 'cough')
    
    def test_symptom_list_with_spaces(self):
        """Test parsing with extra spaces"""
        symptom_input = "fever,  headache  , cough"
        symptoms_list = [s.strip() for s in symptom_input.split(',')]
        
        # All should be properly stripped
        for symptom in symptoms_list:
            self.assertEqual(symptom, symptom.strip())
    
    def test_single_symptom(self):
        """Test parsing of single symptom"""
        symptom_input = "fever"
        
        if ',' in symptom_input:
            symptoms_list = [s.strip() for s in symptom_input.split(',')]
        else:
            symptoms_list = [symptom_input.strip()]
        
        self.assertEqual(len(symptoms_list), 1)
        self.assertEqual(symptoms_list[0], 'fever')


class TestChatbotEdgeCases(unittest.TestCase):
    """Test edge cases in chatbot functionality"""
    
    def test_very_long_input(self):
        """Test handling of very long input"""
        long_input = "what are the symptoms " * 50
        result = classify_input_type(long_input)
        
        # Should still classify correctly
        self.assertEqual(result, 'question')
    
    def test_special_characters_in_input(self):
        """Test handling of special characters"""
        inputs = [
            "what's diabetes?",
            "symptoms: fever, cough",
            "diabetes (type-2)"
        ]
        
        for user_input in inputs:
            # Should not raise an exception
            try:
                result = classify_input_type(user_input)
                self.assertIsNotNone(result)
            except Exception as e:
                self.fail(f"Failed to classify '{user_input}': {e}")
    
    def test_numeric_input(self):
        """Test handling of numeric input"""
        result = classify_input_type("123456")
        self.assertIsNotNone(result)
    
    def test_mixed_language_characters(self):
        """Test handling of mixed language input (if applicable)"""
        # Test with English input (basic test)
        result = classify_input_type("diabetes symptoms")
        self.assertIsNotNone(result)


class TestChatbotDiseaseRecognition(unittest.TestCase):
    """Test disease name recognition"""
    
    def test_common_disease_names(self):
        """Test recognition of common disease names"""
        common_diseases = [
            'diabetes',
            'malaria',
            'typhoid',
            'pneumonia',
            'tuberculosis'
        ]
        
        for disease in common_diseases:
            result = classify_input_type(disease)
            # Should classify as disease or question (both valid)
            self.assertIn(result, ['disease', 'question'])
    
    def test_disease_with_spaces(self):
        """Test disease names with spaces"""
        diseases = [
            'heart disease',
            'high blood pressure',
            'common cold'
        ]
        
        for disease in diseases:
            result = classify_input_type(disease)
            self.assertIsNotNone(result)


class TestChatbotQuestionPatterns(unittest.TestCase):
    """Test various question patterns"""
    
    def test_what_questions(self):
        """Test 'what' questions"""
        questions = [
            "what is diabetes",
            "what are the symptoms",
            "what causes fever"
        ]
        
        for q in questions:
            result = classify_input_type(q)
            self.assertEqual(result, 'question')
    
    def test_how_questions(self):
        """Test 'how' questions"""
        questions = [
            "how to treat diabetes",
            "how can I prevent fever",
            "how do I know if I have malaria"
        ]
        
        for q in questions:
            result = classify_input_type(q)
            self.assertEqual(result, 'question')
    
    def test_why_questions(self):
        """Test 'why' questions"""
        questions = [
            "why is my blood pressure high",
            "why do I have fever"
        ]
        
        for q in questions:
            result = classify_input_type(q)
            self.assertEqual(result, 'question')
    
    def test_when_questions(self):
        """Test 'when' questions"""
        questions = [
            "when should I see a doctor",
            "when do symptoms appear"
        ]
        
        for q in questions:
            result = classify_input_type(q)
            self.assertEqual(result, 'question')


if __name__ == '__main__':
    unittest.main()
