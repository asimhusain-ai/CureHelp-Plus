import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import numpy as np
import time

class ProfileManager:
    def __init__(self):
        self.profiles_file = "user_profiles.json"
        self._last_save_time = 0
        self._save_debounce_seconds = 2  # Wait 2 seconds before saving (OPTIMIZATION)
    
    def ensure_session_state_initialized(self):
        """Ensure session state is properly initialized"""
        if 'user_profiles' not in st.session_state:
            st.session_state.user_profiles = []
            self.load_profiles()
    
    def load_profiles(self):
        """Load profiles from JSON file with caching"""
        if os.path.exists(self.profiles_file):
            try:
                with open(self.profiles_file, 'r') as f:
                    loaded_profiles = json.load(f)
                    if isinstance(loaded_profiles, list):
                        st.session_state.user_profiles = loaded_profiles
            except Exception as e:
                st.warning(f"Error loading profiles: {e}")
                st.session_state.user_profiles = []
        else:
            st.session_state.user_profiles = []
    
    def convert_numpy_types(self, obj):
        """Convert numpy data types to Python native types for JSON serialization - Optimized"""
        # Optimized type checking using isinstance with tuple for better performance
        if isinstance(obj, (np.integer, np.int32, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float32, np.float64)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {key: self.convert_numpy_types(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self.convert_numpy_types(item) for item in obj]
        else:
            return obj
    
    def save_profiles(self, force=False):
        """Save profiles to JSON file with debouncing to reduce I/O (OPTIMIZATION)"""
        try:
            current_time = time.time()
            
            # Debounce: Only save if enough time has passed or force is True
            if not force and (current_time - self._last_save_time) < self._save_debounce_seconds:
                return
            
            # Ensure session state is initialized
            self.ensure_session_state_initialized()
            
            profiles_to_save = self.convert_numpy_types(st.session_state.user_profiles)
            
            with open(self.profiles_file, 'w') as f:
                json.dump(profiles_to_save, f, indent=4)
            
            self._last_save_time = current_time
        except Exception as e:
            st.error(f"Error saving profiles: {e}")
    
    def add_profile(self, profile_data):
        """Add a new user profile"""
        try:
            # Ensure session state is initialized
            self.ensure_session_state_initialized()
            
            profile_id = f"user_{len(st.session_state.user_profiles) + 1:03d}"
            profile_data['id'] = profile_id
            profile_data['created_at'] = datetime.now().strftime("%d-%b-%Y %H:%M")
            
            profile_data = self.convert_numpy_types(profile_data)
            
            st.session_state.user_profiles.append(profile_data)
            self.save_profiles(force=True)  # Force immediate save for new profiles
            return profile_id
        except Exception as e:
            st.error(f"Error adding profile: {e}")
            return None
    
    def get_all_profiles(self):
        """Get all user profiles"""
        self.ensure_session_state_initialized()
        return st.session_state.user_profiles
    
    def render_patient_details_page(self):
        """Render the patient details input form"""
        st.markdown("<h1 style='text-align: center; margin-bottom: 30px;'>Enter Patient Details</h1>", 
                   unsafe_allow_html=True)
        
        # Create a centered container with reduced width
        with st.container():
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col2:
                with st.form("patient_details_form", clear_on_submit=False):
                    subcol1, subcol2 = st.columns(2)
                    
                    with subcol1:
                        name = st.text_input("Full Name*", placeholder="Enter full name")
                        age = st.number_input("Age*", min_value=1, max_value=120, value=25)
                    
                    with subcol2:
                        contact = st.text_input("Contact Number*", placeholder="Enter phone number")
                        address = st.text_area("Address*", placeholder="Enter complete address", height=80)
                    
                    gender_col, status_col = st.columns(2)
                    with gender_col:
                        gender = st.selectbox("Gender*", ["Select", "Male", "Female", "Other"])
                    with status_col:
                        marital_status = st.selectbox("Marital Status*", ["Select", "Single", "Married", "Divorced", "Widowed"])
                    
                    # Centered login button
                    st.markdown("<br>", unsafe_allow_html=True)
                    btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 1])
                    
                    with btn_col2:
                        submitted = st.form_submit_button("Login", type="primary", use_container_width=True)
                    
                    if submitted:
                        if not all([name.strip(), age, contact.strip(), address.strip(), 
                                   gender != "Select", marital_status != "Select"]):
                            st.error("Please fill in all required fields (*)")
                            return False
                        
                        # Validate contact number
                        if not contact.strip().isdigit() or len(contact.strip()) < 10:
                            st.error("Please enter a valid contact number (at least 10 digits)")
                            return False
                        
                        # Save profile and redirect
                        profile_data = {
                            "name": name.strip(),
                            "age": int(age),
                            "contact": contact.strip(),
                            "address": address.strip(),
                            "gender": gender,
                            "marital_status": marital_status,
                            "predictions": {} 
                        }
                        
                        profile_id = self.add_profile(profile_data)
                        if profile_id:
                            st.session_state.current_profile = profile_data
                            st.session_state.current_profile_id = profile_id
                            st.session_state.page = "input"
                            st.success(f"Profile created successfully! Welcome, {name}!")
                            st.rerun()
                        else:
                            st.error("Failed to create profile. Please try again.")
            
            return False
    
    def auto_save_profile(self):
        """Automatically save the current profile with predictions - Enhanced for all cases"""
        try:
            self.ensure_session_state_initialized()
            
            # Case 1: Save profile when user exits app (with or without predictions)
            # Case 2: Save profile when user visits Profile tab (with current predictions)
            if st.session_state.current_profile and st.session_state.current_profile_id:
                
                # Find the current profile
                for i, profile in enumerate(st.session_state.user_profiles):
                    if profile.get('id') == st.session_state.current_profile_id:
                        # Always update basic profile info
                        st.session_state.user_profiles[i].update({
                            'name': st.session_state.current_profile.get('name'),
                            'age': st.session_state.current_profile.get('age'),
                            'contact': st.session_state.current_profile.get('contact'),
                            'address': st.session_state.current_profile.get('address'),
                            'gender': st.session_state.current_profile.get('gender'),
                            'marital_status': st.session_state.current_profile.get('marital_status')
                        })
                        
                        # Update predictions if they exist
                        if st.session_state.predictions:
                            converted_predictions = self.convert_numpy_types(st.session_state.predictions)
                            st.session_state.user_profiles[i]['predictions'] = converted_predictions
                            st.session_state.current_profile['predictions'] = converted_predictions
                        
                        st.session_state.user_profiles[i]['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        self.save_profiles()  # Use debounced save here (non-critical update)
                        return True
                
                # If profile not found in list, add it (shouldn't happen normally)
                profile_data = st.session_state.current_profile.copy()
                if st.session_state.predictions:
                    profile_data['predictions'] = self.convert_numpy_types(st.session_state.predictions)
                
                profile_id = self.add_profile(profile_data)
                if profile_id:
                    st.session_state.current_profile_id = profile_id
                    return True
            
            return False
        except Exception as e:
            print(f"Auto-save error: {e}")
            return False
    
    def save_profile_with_predictions(self, profile_id, predictions):
        """Manual save profile with predictions (for explicit user action)"""
        try:
            self.ensure_session_state_initialized()
            
            for i, profile in enumerate(st.session_state.user_profiles):
                if profile.get('id') == profile_id:
                    converted_predictions = self.convert_numpy_types(predictions)
                    
                    st.session_state.user_profiles[i]['predictions'] = converted_predictions
                    st.session_state.user_profiles[i]['saved_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.save_profiles(force=True)  # Force immediate save for manual saves
                    return True
            return False
        except Exception as e:
            st.error(f"Error saving predictions: {e}")
            return False
    

    def render_profiles_tab(self):
        """Render the profiles tab with search and horizontal layout"""
        self.ensure_session_state_initialized()
        
        st.markdown("<h3 style='margin-bottom: 20px;'>Saved Patient Profiles</h3>", 
                unsafe_allow_html=True)
        
        # Auto-save current profile when entering Profiles tab
        if st.session_state.current_profile:
            self.auto_save_profile()
        
        profiles = self.get_all_profiles()
        
        if not profiles:
            st.info("No patient profiles saved yet. Profiles are automatically saved when you make predictions.")
            return
        
        # ✅ YEH LINE ADD KAREN: Latest profiles first (reverse the list)
        profiles = list(reversed(profiles))
        
        # Feature 1: Search Bar
        search_term = st.text_input("🔍 Search by name", placeholder="Enter patient name to search...")
        
        # Filter profiles based on search
        if search_term:
            filtered_profiles = [profile for profile in profiles 
                            if search_term.lower() in profile.get('name', '').lower()]
        else:
            filtered_profiles = profiles
        
        if not filtered_profiles:
            st.warning("No profiles found matching your search.")
            return
        
        # Feature 2: Horizontal layout - 3 profiles per row
        for i in range(0, len(filtered_profiles), 3):
            # Create a row with 3 columns
            cols = st.columns(3)
            
            for j in range(3):
                profile_index = i + j
                if profile_index < len(filtered_profiles):
                    profile = filtered_profiles[profile_index]
                    
                    with cols[j]:
                        self._render_profile_card(profile, profile_index)


    def _render_profile_card(self, profile, original_index):
        """Render a single profile card in horizontal layout"""
        # Create a container with relative positioning
        with st.container():
            # Convert profile ID to User1, User2 format
            profile_id = profile.get('id', '')
            if profile_id.startswith('user_'):
                try:
                    user_number = int(profile_id.split('_')[1])
                    display_id = f"Patient{user_number}"
                except:
                    display_id = f"Patient{original_index + 1}"
            else:
                display_id = f"Patient{original_index + 1}"
            
            # Build the card content as HTML
            card_content = f"""
            <div style='
                border: 1px solid #e0e0e0;
                border-radius: 10px;
                padding: 15px;
                margin: 8px 0;
                background: white;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                height: 300px;
                overflow-y: auto;
                position: relative;
            '>
                <h4 style='margin:0 0 10px 0; color: #1976d2;'>{profile.get('name', 'N/A')} ㅤ {profile.get('created_at', 'N/A')}</h4>
                <p style='margin:5px 0; font-size:14px;'>
                    <strong>ID:</strong> {display_id}<br>
                    <strong>Age:</strong> {profile.get('age', 'N/A')}<br>
                    <strong>Gender:</strong> {profile.get('gender', 'N/A')}<br>
                    <strong>Contact:</strong> {profile.get('contact', 'N/A')}<br>
                    <strong>Status:</strong> {profile.get('marital_status', 'N/A')}<br>
                    <strong>Address:</strong> {profile.get('address', 'N/A')}<br>
            """
            
            # Add predictions section with two-column layout
            predictions = profile.get('predictions', {})
            if predictions:
                card_content += "<div style='border-top: 1px solid #f0f0f0; padding-top: 10px;'>"
                card_content += "<strong style='font-size:14px;'>📊 Predictions:</strong><br>"
                
                prediction_parts = []
                for disease, data in predictions.items():
                    risk = data.get('prob', 0)
                    severity = data.get('severity', '')
                    severity_text = f" ({severity})" if severity else ""
                    prediction_parts.append(f"{disease}: {risk:.1f}%{severity_text}")
                
                # Join all predictions with " | " separator in a single line
                card_content += f"<span style='font-size:14px;'>{'   |   '.join(prediction_parts)}</span>"
                card_content += "</div>"
            else:
                card_content += "<div style='border-top: 1px solid #f0f0f0; padding-top: 10px;'>"
                card_content += "<strong style='font-size:14px;'>📊 Predictions:</strong> ❌ No predictions"
                card_content += "</div>"
            
            card_content += """
            </div>
            """
            
            # Render the card content
            st.markdown(card_content, unsafe_allow_html=True)

    
profile_manager = ProfileManager()