import streamlit as st
from functools import lru_cache

@lru_cache(maxsize=1)
def get_hospitals_data():
    """Returns a list of hospital data"""
    return [
        {
            "name": "Apollo Hospital",
            "address": "G-1, Block G, Sector 26, Noida, Uttar Pradesh 201301",
            "contact": "+91-120-255-9001",
            "speciality": "Multi-Speciality",
            "distance": "2.5 km",
            "location_url": "https://maps.google.com/?q=Apollo+Hospital+Sector+26+Noida",
            "website_url": "https://www.apollohospitals.com"
        },
        {
            "name": "Fortis Hospital",
            "address": "B-22, Sector 62, Noida, Uttar Pradesh 201301",
            "contact": "+91-120-240-2222",
            "speciality": "Multi-Speciality", 
            "distance": "3.2 km",
            "location_url": "https://maps.google.com/?q=Fortis+Hospital+Sector+62+Noida",
            "website_url": "https://www.fortishealthcare.com"
        },
        {
            "name": "Max Super Speciality Hospital",
            "address": "W-3, Sector 1, Vaishali, Ghaziabad, Uttar Pradesh 201010",
            "contact": "+91-120-429-4444",
            "speciality": "Super Speciality",
            "distance": "4.1 km",
            "location_url": "https://maps.google.com/?q=Max+Super+Speciality+Hospital+Vaishali",
            "website_url": "https://www.maxhealthcare.in"
        },
        {
            "name": "Artemis Hospital",
            "address": "Sector 51, Gurugram, Haryana 122001",
            "contact": "+91-124-451-1111",
            "speciality": "Multi-Speciality",
            "distance": "5.8 km",
            "location_url": "https://maps.google.com/?q=Artemis+Hospital+Sector+51+Gurugram",
            "website_url": "https://www.artemishospitals.com"
        },
        {
            "name": "Medanta The Medicity",
            "address": "Sector 38, Gurugram, Haryana 122001",
            "contact": "+91-124-414-1414",
            "speciality": "Multi-Speciality",
            "distance": "6.5 km",
            "location_url": "https://maps.google.com/?q=Medanta+The+Medicity+Gurugram",
            "website_url": "https://www.medanta.org"
        },
        {
            "name": "AIIMS Delhi",
            "address": "Ansari Nagar, New Delhi, Delhi 110029",
            "contact": "+91-11-265-8858",
            "speciality": "Government Multi-Speciality",
            "distance": "7.2 km",
            "location_url": "https://maps.google.com/?q=AIIMS+Delhi+Ansari+Nagar",
            "website_url": "https://www.aiims.edu"
        },
        {
            "name": "Sir Ganga Ram Hospital",
            "address": "Sir Ganga Ram Hospital Marg, New Delhi 110060",
            "contact": "+91-11-257-3520",
            "speciality": "Multi-Speciality",
            "distance": "8.1 km",
            "location_url": "https://maps.google.com/?q=Sir+Ganga+Ram+Hospital+Delhi",
            "website_url": "https://www.sgrh.com"
        },
        {
            "name": "BLK-Max Super Speciality Hospital",
            "address": "Pusa Road, New Delhi 110005",
            "contact": "+91-11-3040-3040",
            "speciality": "Super Speciality",
            "distance": "8.7 km",
            "location_url": "https://maps.google.com/?q=BLK+Max+Hospital+Pusa+Road",
            "website_url": "https://www.blkmaxhospital.com"
        },
        {
            "name": "Indraprastha Apollo Hospital",
            "address": "Sarita Vihar, Delhi Mathura Road, New Delhi 110076",
            "contact": "+91-11-2692-5801",
            "speciality": "Multi-Speciality",
            "distance": "9.3 km",
            "location_url": "https://maps.google.com/?q=Indraprastha+Apollo+Hospital+Delhi",
            "website_url": "https://delhi.apollohospitals.com"
        },
        {
            "name": "Safdarjung Hospital",
            "address": "Ansari Nagar West, New Delhi 110029",
            "contact": "+91-11-2670-7444",
            "speciality": "Government Hospital",
            "distance": "10.2 km",
            "location_url": "https://maps.google.com/?q=Safdarjung+Hospital+Delhi",
            "website_url": "https://www.safdarjunghospital.org"
        },
        {
            "name": "RML Hospital",
            "address": "Baba Kharak Singh Marg, New Delhi 110001",
            "contact": "+91-11-2340-4238",
            "speciality": "Government Multi-Speciality",
            "distance": "11.5 km",
            "location_url": "https://maps.google.com/?q=RML+Hospital+Delhi",
            "website_url": "https://www.rmlh.nic.in"
        },
        {
            "name": "Dharamshila Narayana Hospital",
            "address": "Dharamshila Marg, Vasundhara Enclave, Delhi 110096",
            "contact": "+91-11-4306-6358",
            "speciality": "Oncology Speciality",
            "distance": "12.1 km",
            "location_url": "https://maps.google.com/?q=Dharamshila+Narayana+Hospital+Delhi",
            "website_url": "https://www.dnarayanahealth.org"
        },
        {
            "name": "Columbia Asia Hospital",
            "address": "Sector 25, Palam Vihar, Gurugram 122017",
            "contact": "+91-124-398-9896",
            "speciality": "Multi-Speciality",
            "distance": "13.2 km",
            "location_url": "https://maps.google.com/?q=Columbia+Asia+Hospital+Gurugram",
            "website_url": "https://www.columbiaindiahospitals.com"
        },
        {
            "name": "Felix Hospital",
            "address": "Sector 137, Noida, Uttar Pradesh 201305",
            "contact": "+91-120-711-7000",
            "speciality": "Multi-Speciality",
            "distance": "20.3 km",
            "location_url": "https://maps.google.com/?q=Felix+Hospital+Noida",
            "website_url": "https://www.felixhospital.com"
        }
    ]

@lru_cache(maxsize=1)
def get_doctors_data():
    """Returns a list of doctor data with different specializations"""
    return [
        {
            "name": "Dr. Rajesh Sharma",
            "contact": "+91-98765-43210",
            "address": "E-45, Sector 27, Noida, UP - 201301",
            "qualification": "MD, DM Cardiology",
            "specialization": "Cardiologist",
            "experience": "15 years",
            "rating": "4.8",
            "location_url": "https://maps.google.com/?q=E-45+Sector+27+Noida",
            "website_url": "https://www.drrajeshsharma-cardio.com"
        },
        {
            "name": "Dr. Priya Singh",
            "contact": "+91-98765-43211", 
            "address": "F-12, Sector 18, Noida, UP - 201301",
            "qualification": "MBBS, MD Pediatrics",
            "specialization": "Pediatrician",
            "experience": "12 years",
            "rating": "4.7",
            "location_url": "https://maps.google.com/?q=F-12+Sector+18+Noida",
            "website_url": "https://www.drpriyasingh-pediatrics.com"
        },
        {
            "name": "Dr. Amit Kumar",
            "contact": "+91-98765-43212",
            "address": "B-25, Sector 34, Noida, UP - 201301",
            "qualification": "MBBS, MS Orthopedics",
            "specialization": "Orthopedic Surgeon",
            "experience": "18 years",
            "rating": "4.9",
            "location_url": "https://maps.google.com/?q=B-25+Sector+34+Noida",
            "website_url": "https://www.dramitkumar-ortho.com"
        },
        {
            "name": "Dr. Sunita Mehta",
            "contact": "+91-98765-43213",
            "address": "C-8, Sector 62, Noida, UP - 201301",
            "qualification": "MBBS, MD Gynecology",
            "specialization": "Gynecologist",
            "experience": "14 years",
            "rating": "4.8",
            "location_url": "https://maps.google.com/?q=C-8+Sector+62+Noida",
            "website_url": "https://www.drsunitamehta-gyno.com"
        },
        {
            "name": "Dr. Ravi Verma",
            "contact": "+91-98765-43214",
            "address": "D-14, Sector 15, Noida, UP - 201301",
            "qualification": "MBBS, MD Neurology",
            "specialization": "Neurologist",
            "experience": "16 years",
            "rating": "4.7",
            "location_url": "https://maps.google.com/?q=D-14+Sector+15+Noida",
            "website_url": "https://www.drraviverma-neuro.com"
        },
        {
            "name": "Dr. Anjali Gupta",
            "contact": "+91-98765-43215",
            "address": "G-7, Sector 29, Noida, UP - 201301",
            "qualification": "MBBS, MD Dermatology",
            "specialization": "Dermatologist",
            "experience": "10 years",
            "rating": "4.6",
            "location_url": "https://maps.google.com/?q=G-7+Sector+29+Noida",
            "website_url": "https://www.dranjaligupta-derma.com"
        },
        {
            "name": "Dr. Sanjay Malhotra",
            "contact": "+91-98765-43216",
            "address": "H-22, Sector 12, Noida, UP - 201301",
            "qualification": "MBBS, MS Ophthalmology",
            "specialization": "Ophthalmologist",
            "experience": "13 years",
            "rating": "4.8",
            "location_url": "https://maps.google.com/?q=H-22+Sector+12+Noida",
            "website_url": "https://www.drsanjaymalhotra-eye.com"
        },
        {
            "name": "Dr. Neha Joshi",
            "contact": "+91-98765-43217",
            "address": "A-5, Sector 33, Noida, UP - 201301",
            "qualification": "MBBS, MD Psychiatry",
            "specialization": "Psychiatrist",
            "experience": "11 years",
            "rating": "4.5",
            "location_url": "https://maps.google.com/?q=A-5+Sector+33+Noida",
            "website_url": "https://www.drnehaJoshi-psych.com"
        },
        {
            "name": "Dr. Vikram Singh",
            "contact": "+91-98765-43218",
            "address": "F-18, Sector 20, Noida, UP - 201301",
            "qualification": "MBBS, MD General Medicine",
            "specialization": "General Physician",
            "experience": "20 years",
            "rating": "4.9",
            "location_url": "https://maps.google.com/?q=F-18+Sector+20+Noida",
            "website_url": "https://www.drvikramsingh-gp.com"
        },
        {
            "name": "Dr. Meera Patel",
            "contact": "+91-98765-43219",
            "address": "E-33, Sector 25, Noida, UP - 201301",
            "qualification": "MBBS, MS ENT",
            "specialization": "ENT Specialist",
            "experience": "15 years",
            "rating": "4.7",
            "location_url": "https://maps.google.com/?q=E-33+Sector+25+Noida",
            "website_url": "https://www.drmeerapatel-ent.com"
        },
        {
            "name": "Dr. Arjun Reddy",
            "contact": "+91-98765-43220",
            "address": "B-11, Sector 40, Noida, UP - 201301",
            "qualification": "MBBS, MD Gastroenterology",
            "specialization": "Gastroenterologist",
            "experience": "17 years",
            "rating": "4.8",
            "location_url": "https://maps.google.com/?q=B-11+Sector+40+Noida",
            "website_url": "https://www.drarjunreddy-gastro.com"
        },
        {
            "name": "Dr. Pooja Khanna",
            "contact": "+91-98765-43221",
            "address": "C-22, Sector 8, Noida, UP - 201301",
            "qualification": "MBBS, MD Endocrinology",
            "specialization": "Endocrinologist",
            "experience": "12 years",
            "rating": "4.6",
            "location_url": "https://maps.google.com/?q=C-22+Sector+8+Noida",
            "website_url": "https://www.drpoojakhanna-endo.com"
        },
        {
            "name": "Dr. Rohit Choudhary",
            "contact": "+91-98765-43222",
            "address": "D-8, Sector 22, Noida, UP - 201301",
            "qualification": "MBBS, MS Urology",
            "specialization": "Urologist",
            "experience": "14 years",
            "rating": "4.7",
            "location_url": "https://maps.google.com/?q=D-8+Sector+22+Noida",
            "website_url": "https://www.drrohitchoudhary-uro.com"
        },
        {
            "name": "Dr. Sneha Kapoor",
            "contact": "+91-98765-43223",
            "address": "G-14, Sector 31, Noida, UP - 201301",
            "qualification": "MBBS, MD Rheumatology",
            "specialization": "Rheumatologist",
            "experience": "13 years",
            "rating": "4.5",
            "location_url": "https://maps.google.com/?q=G-14+Sector+31+Noida",
            "website_url": "https://www.drsnehakapoor-rheuma.com"
        }
    ]

def render_consultant_tab():
    """Renders the consultant tab with hospitals and doctors"""
    
    st.markdown("<h3 style='margin-bottom: 22px;'>Find Nearest Healthcare Providers</h3>", 
                unsafe_allow_html=True)
    
    st.markdown("---")
    
    hospitals_data = get_hospitals_data()
    doctors_data = get_doctors_data()
    
    for i in range(0, max(len(hospitals_data), len(doctors_data)), 2):
        if i < len(hospitals_data) or i < len(doctors_data):
            cols = st.columns(4)
            
            with cols[0]:
                if i == 0:  
                    st.markdown("### 🏨 Hospitals Nearby")
                if i < len(hospitals_data):
                    hospital1 = hospitals_data[i]
                    st.markdown(f"""
                    <div style='
                        border: 1px solid #e0e0e0; 
                        border-radius: 40px; 
                        padding: 15px; 
                        margin: 10px 0; 
                        background: white;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        height: 230px;
                        overflow: hidden;
                        width: 390px;
                    '>
                        <h4 style='margin:0; color: #1976d2; font-size: 18px;'>{hospital1['name']}</h4>
                        <p style='margin:8px 0; font-size:12px; color:#666; line-height: 1.4;'>
                            <strong>Speciality:</strong> {hospital1['speciality']}<br>
                            <strong>📍 Distance:</strong> {hospital1['distance']}<br>
                            <strong>📞 Contact:</strong> {hospital1['contact']}<br>
                            <strong>🏠 Address:</strong> {hospital1['address']}
                        </p>
                        <div style='display: flex; gap: 30px; margin-top: 10px;'>
                            <a href='{hospital1['website_url']}' target='_blank' style='
                                text-decoration: none;
                                margin-left: 18px;
                                color: #454545;
                                font-weight: bold;
                                font-size: 13px;
                            '>Website</a>
                            <a href='{hospital1['location_url']}' target='_blank' style='
                                text-decoration: none;
                                color: #454545;
                                font-weight: bold;
                                font-size: 13px;
                            '>Location</a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            with cols[1]:
                if i == 0:  
                    st.markdown("### &nbsp;")  
                if i + 1 < len(hospitals_data):
                    hospital2 = hospitals_data[i + 1]
                    st.markdown(f"""
                    <div style='
                        border: 1px solid #e0e0e0; 
                        border-radius: 40px; 
                        padding: 15px; 
                        margin: 10px 0; 
                        background: white;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        height: 230px;
                        overflow: hidden;
                        width: 390px;
                    '>
                        <h4 style='margin:0; color: #1976d2; font-size: 18px;'>{hospital2['name']}</h4>
                        <p style='margin:8px 0; font-size:12px; color:#666; line-height: 1.4;'>
                            <strong>Speciality:</strong> {hospital2['speciality']}<br>
                            <strong>📍 Distance:</strong> {hospital2['distance']}<br>
                            <strong>📞 Contact:</strong> {hospital2['contact']}<br>
                            <strong>🏠 Address:</strong> {hospital2['address']}
                        </p>
                        <div style='display: flex; gap: 20px; margin-top: 12px;'>
                            <a href='{hospital2['website_url']}' target='_blank' style='
                                text-decoration: none;
                                margin-left: 18px;
                                color: #454545;
                                font-weight: bold;
                                font-size: 13px;
                            '>Website</a>
                            <a href='{hospital2['location_url']}' target='_blank' style='
                                text-decoration: none;
                                color: #454545;
                                font-weight: bold;
                                font-size: 13px;
                            '>Location</a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            with cols[2]:
                if i == 0:  
                    st.markdown("### 👨‍⚕️ Doctors Nearby")
                if i < len(doctors_data):
                    doctor1 = doctors_data[i]
                    st.markdown(f"""
                    <div style='
                        border: 1px solid #e0e0e0; 
                        border-radius: 40px; 
                        padding: 15px; 
                        margin: 10px 0; 
                        background: white;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        height: 230px;
                        overflow: hidden;
                        width: 390px;
                    '>
                        <h4 style='margin:0; color: #1976d2; font-size: 18px;'>{doctor1['name']}</h4>
                        <p style='margin:8px 0; font-size:12px; color:#666; line-height: 1.4;'>
                            <strong>🎯 Specialization:</strong> {doctor1['specialization']}<br>
                            <strong>📜 Qualification:</strong> {doctor1['qualification']}<br>
                            <strong>⭐ Experience:</strong> {doctor1['experience']}<br>
                            <strong>📞 Contact:</strong> {doctor1['contact']}<br>
                            <strong>🏠 Clinic Address:</strong> {doctor1['address']}
                        </p>
                        <div style='display: flex; gap: 20px; margin-top: 12px;'>
                            <a href='{doctor1['website_url']}' target='_blank' style='
                                text-decoration: none;
                                margin-left: 18px;
                                color: #454545;
                                font-weight: bold;
                                font-size: 13px;
                            '>Website</a>
                            <a href='{doctor1['location_url']}' target='_blank' style='
                                text-decoration: none;
                                color: #454545;
                                font-weight: bold;
                                font-size: 13px;
                            '>Location</a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            with cols[3]:
                if i == 0: 
                    st.markdown("### &nbsp;")  
                if i + 1 < len(doctors_data):
                    doctor2 = doctors_data[i + 1]
                    st.markdown(f"""
                    <div style='
                        border: 1px solid #e0e0e0; 
                        border-radius: 40px; 
                        padding: 15px; 
                        margin: 10px 0; 
                        background: white;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        height: 230px;
                        overflow: hidden;
                        width: 390px;
                    '>
                        <h4 style='margin:0; color: #1976d2; font-size: 18px;'>{doctor2['name']}</h4>
                        <p style='margin:8px 0; font-size:12px; color:#666; line-height: 1.4;'>
                            <strong>🎯 Specialization:</strong> {doctor2['specialization']}<br>
                            <strong>📜 Qualification:</strong> {doctor2['qualification']}<br>
                            <strong>⭐ Experience:</strong> {doctor2['experience']}<br>
                            <strong>📞 Contact:</strong> {doctor2['contact']}<br>
                            <strong>🏠 Clinic Address:</strong> {doctor2['address']}
                        </p>
                        <div style='display: flex; gap: 20px; margin-top: 12px;'>
                            <a href='{doctor2['website_url']}' target='_blank' style='
                                text-decoration: none;
                                margin-left: 18px;
                                color: #454545;
                                font-weight: bold;
                                font-size: 13px;
                            '>Website</a>
                            <a href='{doctor2['location_url']}' target='_blank' style='
                                text-decoration: none;
                                color: #454545;
                                font-weight: bold;
                                font-size: 13px;
                            '>Location</a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    
