"""
Unit tests for consultant.py
Tests healthcare provider directory functionality
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from consultant import get_hospitals_data, get_doctors_data


class TestConsultantHospitals(unittest.TestCase):
    """Test cases for hospital data"""
    
    def test_hospitals_data_not_empty(self):
        """Test that hospital data is not empty"""
        hospitals = get_hospitals_data()
        self.assertIsNotNone(hospitals)
        self.assertGreater(len(hospitals), 0)
    
    def test_hospitals_data_structure(self):
        """Test that each hospital has required fields"""
        hospitals = get_hospitals_data()
        required_fields = ['name', 'address', 'contact', 'speciality', 
                          'distance', 'location_url', 'website_url']
        
        for hospital in hospitals:
            for field in required_fields:
                self.assertIn(field, hospital, 
                            f"Hospital {hospital.get('name', 'Unknown')} missing field: {field}")
    
    def test_hospital_name_not_empty(self):
        """Test that all hospitals have non-empty names"""
        hospitals = get_hospitals_data()
        
        for hospital in hospitals:
            self.assertIsNotNone(hospital['name'])
            self.assertGreater(len(hospital['name']), 0)
    
    def test_hospital_contact_format(self):
        """Test that hospital contact numbers are in expected format"""
        hospitals = get_hospitals_data()
        
        for hospital in hospitals:
            contact = hospital['contact']
            self.assertIsNotNone(contact)
            self.assertIn('+91', contact)  # Indian phone format
    
    def test_hospital_distance_format(self):
        """Test that distance is in proper format"""
        hospitals = get_hospitals_data()
        
        for hospital in hospitals:
            distance = hospital['distance']
            self.assertIsNotNone(distance)
            self.assertIn('km', distance.lower())
    
    def test_hospital_url_validity(self):
        """Test that URLs start with http/https"""
        hospitals = get_hospitals_data()
        
        for hospital in hospitals:
            location_url = hospital['location_url']
            website_url = hospital['website_url']
            
            self.assertTrue(location_url.startswith('http'), 
                          f"{hospital['name']} location_url should start with http")
            self.assertTrue(website_url.startswith('http'), 
                          f"{hospital['name']} website_url should start with http")
    
    def test_hospital_speciality_values(self):
        """Test that speciality field contains valid values"""
        hospitals = get_hospitals_data()
        
        valid_keywords = ['Multi-Speciality', 'Super Speciality', 'Government', 
                         'Speciality', 'Hospital']
        
        for hospital in hospitals:
            speciality = hospital['speciality']
            self.assertIsNotNone(speciality)
            # At least one keyword should be in speciality
            has_valid_keyword = any(keyword in speciality for keyword in valid_keywords)
            self.assertTrue(has_valid_keyword, 
                          f"{hospital['name']} has invalid speciality: {speciality}")
    
    def test_hospital_count(self):
        """Test that we have a reasonable number of hospitals"""
        hospitals = get_hospitals_data()
        self.assertGreaterEqual(len(hospitals), 10)
        self.assertLessEqual(len(hospitals), 50)  # Reasonable upper limit
    
    def test_hospital_unique_names(self):
        """Test that hospital names are unique"""
        hospitals = get_hospitals_data()
        names = [h['name'] for h in hospitals]
        unique_names = set(names)
        
        self.assertEqual(len(names), len(unique_names), 
                        "Hospital names should be unique")
    
    def test_hospital_unique_contacts(self):
        """Test that contact numbers are unique"""
        hospitals = get_hospitals_data()
        contacts = [h['contact'] for h in hospitals]
        unique_contacts = set(contacts)
        
        self.assertEqual(len(contacts), len(unique_contacts), 
                        "Contact numbers should be unique")


class TestConsultantDoctors(unittest.TestCase):
    """Test cases for doctor data"""
    
    def test_doctors_data_not_empty(self):
        """Test that doctor data is not empty"""
        doctors = get_doctors_data()
        self.assertIsNotNone(doctors)
        self.assertGreater(len(doctors), 0)
    
    def test_doctors_data_structure(self):
        """Test that each doctor has required fields"""
        doctors = get_doctors_data()
        required_fields = ['name', 'contact', 'address', 'qualification', 
                          'specialization', 'experience', 'rating', 
                          'location_url', 'website_url']
        
        for doctor in doctors:
            for field in required_fields:
                self.assertIn(field, doctor, 
                            f"Doctor {doctor.get('name', 'Unknown')} missing field: {field}")
    
    def test_doctor_name_format(self):
        """Test that doctor names start with 'Dr.'"""
        doctors = get_doctors_data()
        
        for doctor in doctors:
            name = doctor['name']
            self.assertTrue(name.startswith('Dr.'), 
                          f"Doctor name should start with 'Dr.': {name}")
    
    def test_doctor_contact_format(self):
        """Test that doctor contact numbers are in expected format"""
        doctors = get_doctors_data()
        
        for doctor in doctors:
            contact = doctor['contact']
            self.assertIsNotNone(contact)
            self.assertIn('+91', contact)  # Indian phone format
    
    def test_doctor_qualification_not_empty(self):
        """Test that all doctors have qualifications"""
        doctors = get_doctors_data()
        
        for doctor in doctors:
            qualification = doctor['qualification']
            self.assertIsNotNone(qualification)
            self.assertGreater(len(qualification), 0)
            # Should contain at least one medical degree
            medical_degrees = ['MBBS', 'MD', 'MS', 'DM']
            has_degree = any(degree in qualification for degree in medical_degrees)
            self.assertTrue(has_degree, 
                          f"{doctor['name']} should have a medical degree")
    
    def test_doctor_specialization_values(self):
        """Test that specializations are valid medical specialties"""
        doctors = get_doctors_data()
        
        valid_specializations = [
            'Cardiologist', 'Pediatrician', 'Orthopedic', 'Gynecologist',
            'Neurologist', 'Dermatologist', 'Ophthalmologist', 'Psychiatrist',
            'General Physician', 'ENT', 'Gastroenterologist', 'Endocrinologist',
            'Urologist', 'Rheumatologist'
        ]
        
        for doctor in doctors:
            specialization = doctor['specialization']
            self.assertIsNotNone(specialization)
            # Should match one of the valid specializations (at least partially)
            is_valid = any(spec in specialization for spec in valid_specializations)
            self.assertTrue(is_valid, 
                          f"{doctor['name']} has invalid specialization: {specialization}")
    
    def test_doctor_experience_format(self):
        """Test that experience is in proper format"""
        doctors = get_doctors_data()
        
        for doctor in doctors:
            experience = doctor['experience']
            self.assertIsNotNone(experience)
            self.assertIn('year', experience.lower())
    
    def test_doctor_experience_values(self):
        """Test that experience values are reasonable"""
        doctors = get_doctors_data()
        
        for doctor in doctors:
            experience = doctor['experience']
            # Extract number from experience string (e.g., "15 years" -> 15)
            years = int(''.join(filter(str.isdigit, experience)))
            self.assertGreaterEqual(years, 5)  # At least 5 years
            self.assertLessEqual(years, 50)  # At most 50 years
    
    def test_doctor_rating_format(self):
        """Test that rating is in proper format"""
        doctors = get_doctors_data()
        
        for doctor in doctors:
            rating = doctor['rating']
            self.assertIsNotNone(rating)
            # Convert to float and check range
            rating_value = float(rating)
            self.assertGreaterEqual(rating_value, 0.0)
            self.assertLessEqual(rating_value, 5.0)
    
    def test_doctor_rating_quality(self):
        """Test that ratings are reasonable (not too low)"""
        doctors = get_doctors_data()
        
        for doctor in doctors:
            rating_value = float(doctor['rating'])
            # Doctors in directory should have decent ratings
            self.assertGreaterEqual(rating_value, 4.0, 
                                  f"{doctor['name']} rating seems too low: {rating_value}")
    
    def test_doctor_url_validity(self):
        """Test that URLs start with http/https"""
        doctors = get_doctors_data()
        
        for doctor in doctors:
            location_url = doctor['location_url']
            website_url = doctor['website_url']
            
            self.assertTrue(location_url.startswith('http'), 
                          f"{doctor['name']} location_url should start with http")
            self.assertTrue(website_url.startswith('http'), 
                          f"{doctor['name']} website_url should start with http")
    
    def test_doctor_count(self):
        """Test that we have a reasonable number of doctors"""
        doctors = get_doctors_data()
        self.assertGreaterEqual(len(doctors), 10)
        self.assertLessEqual(len(doctors), 50)  # Reasonable upper limit
    
    def test_doctor_unique_names(self):
        """Test that doctor names are unique"""
        doctors = get_doctors_data()
        names = [d['name'] for d in doctors]
        unique_names = set(names)
        
        self.assertEqual(len(names), len(unique_names), 
                        "Doctor names should be unique")
    
    def test_doctor_unique_contacts(self):
        """Test that contact numbers are unique"""
        doctors = get_doctors_data()
        contacts = [d['contact'] for d in doctors]
        unique_contacts = set(contacts)
        
        self.assertEqual(len(contacts), len(unique_contacts), 
                        "Contact numbers should be unique")
    
    def test_diverse_specializations(self):
        """Test that we have doctors from diverse specializations"""
        doctors = get_doctors_data()
        specializations = set(d['specialization'] for d in doctors)
        
        # Should have at least 8 different specializations
        self.assertGreaterEqual(len(specializations), 8, 
                              "Should have diverse specializations")


class TestConsultantDataIntegrity(unittest.TestCase):
    """Test data integrity and consistency"""
    
    def test_no_placeholder_data(self):
        """Test that there are no placeholder values in data"""
        hospitals = get_hospitals_data()
        doctors = get_doctors_data()
        
        placeholder_terms = ['TODO', 'TBD', 'placeholder', 'test', 'example']
        
        for hospital in hospitals:
            for field, value in hospital.items():
                value_str = str(value).lower()
                for term in placeholder_terms:
                    self.assertNotIn(term, value_str, 
                                   f"Placeholder found in hospital {hospital['name']}: {field}")
        
        for doctor in doctors:
            for field, value in doctor.items():
                value_str = str(value).lower()
                for term in placeholder_terms:
                    self.assertNotIn(term, value_str, 
                                   f"Placeholder found in doctor {doctor['name']}: {field}")
    
    def test_data_consistency(self):
        """Test that data format is consistent across all entries"""
        hospitals = get_hospitals_data()
        
        # All hospitals should have same field count
        field_counts = [len(h) for h in hospitals]
        self.assertEqual(len(set(field_counts)), 1, 
                        "All hospitals should have same number of fields")
        
        doctors = get_doctors_data()
        field_counts = [len(d) for d in doctors]
        self.assertEqual(len(set(field_counts)), 1, 
                        "All doctors should have same number of fields")


if __name__ == '__main__':
    unittest.main()
