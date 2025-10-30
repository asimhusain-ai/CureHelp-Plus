import streamlit as st
import pandas as pd
import numpy as np
import re
from zipfile import ZipFile
import io
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import warnings
warnings.filterwarnings('ignore')

@st.cache_data
def load_datasets(zip_path='chatdata.zip'):
    """Load all required datasets from a compressed zip folder with robust error handling"""
    try:
        with ZipFile(zip_path) as z:
            # CSVs are inside chatbot/ folder within the zip
            precautions_df = load_csv_flexible_from_zip(z, 'chatdata/Disease precaution.csv')
            symptoms_df = load_csv_flexible_from_zip(z, 'chatdata/DiseaseAndSymptoms.csv')
            faq_df = load_csv_flexible_from_zip(z, 'chatdata/medquad.csv')
            augmented_df = load_csv_flexible_from_zip(z, 'chatdata/Final_Augmented_dataset_Diseases_and_Symptoms.csv')
        
        return precautions_df, symptoms_df, faq_df, augmented_df
    
    except Exception as e:
        st.error(f"❌ Error loading datasets from zip: {e}")
        return None, None, None, None


def load_csv_flexible_from_zip(zip_file: ZipFile, file_name: str):
    """Load CSV from ZipFile with flexible column handling"""
    try:
        with zip_file.open(file_name) as f:
            try:
                df = pd.read_csv(f, encoding='utf-8', on_bad_lines='skip')
            except:
                try:
                    df = pd.read_csv(f, encoding='latin-1', on_bad_lines='skip')
                except:
                    # For older pandas versions
                    df = pd.read_csv(f, encoding='utf-8', error_bad_lines=False, warn_bad_lines=False)

        df = clean_dataframe(df)
        return df

    except Exception as e:
        st.warning(f"⚠️ Could not load {file_name} from zip: {e}")
        return None


def clean_dataframe(df):
    """Clean dataframe by handling missing values and inconsistent data"""
    if df is None:
        return None
    
    # Remove completely empty rows and columns
    df = df.dropna(how='all')
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    # Fill NaN values with empty strings for string columns
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].fillna('')
    
    return df

def preprocess_datasets(precautions_df, symptoms_df, faq_df, augmented_df):
    """Preprocess datasets for better matching"""
    try:
        # Clean disease names across all datasets
        for df in [precautions_df, symptoms_df, faq_df]:
            if df is not None and 'Disease' in df.columns:
                df['Disease_clean'] = df['Disease'].str.lower().str.strip()
        
        if augmented_df is not None and 'diseases' in augmented_df.columns:
            augmented_df['diseases_clean'] = augmented_df['diseases'].str.lower().str.strip()
        
        if faq_df is not None and 'question' in faq_df.columns:
            faq_df['question_clean'] = faq_df['question'].str.lower().str.strip()
        
        return precautions_df, symptoms_df, faq_df, augmented_df
    except Exception as e:
        st.warning(f"Error in preprocessing: {e}")
        return precautions_df, symptoms_df, faq_df, augmented_df

def find_question_answer(question, faq_df):
    """Find the best matching question in FAQ dataset - Optimized with early exit"""
    if faq_df is None or faq_df.empty:
        return None
    
    question_clean = question.lower().strip()
    
    # Improved question matching
    best_match = None
    best_score = 0
    threshold = 0.4
    
    # Common question patterns
    question_patterns = [
        r'what (are|is) (the )?(symptoms|signs) of',
        r'what (are|is) (the )?(causes|reason) of',
        r'what (are|is) (the )?(treatment|remedy) for',
        r'how (to|do) (treat|handle|manage)',
        r'what (is|are)'
    ]
    
    # Check if it's a symptom question
    is_symptom_question = any(re.search(pattern, question_clean) for pattern in question_patterns)
    
    # Pre-compute question words once (OPTIMIZATION)
    question_words = set(question_clean.split())
    disease_terms = [term for term in re.findall(r'[a-zA-Z]+', question_clean) if len(term) > 4]
    
    for idx, row in faq_df.iterrows():
        faq_question = str(row['question']).lower() if pd.notna(row['question']) else ""
        
        # Skip empty questions early (OPTIMIZATION)
        if not faq_question:
            continue
        
        score = 0
        
        # For symptom questions, prioritize answers that actually list symptoms
        if is_symptom_question and ('symptom' in faq_question or 'sign' in faq_question):
            score += 0.3
        
        # Word overlap scoring
        faq_words = set(faq_question.split())
        
        if question_words and faq_words:
            overlap = len(question_words.intersection(faq_words))
            score += overlap / len(question_words)
        
        # Boost score for exact disease matches
        for term in disease_terms:
            if term in faq_question:
                score += 0.2
        
        if score > best_score:
            best_score = score
            best_match = row
            
            # Early exit if we find a very good match (OPTIMIZATION)
            if best_score > 0.9:
                break
    
    return best_match if best_score > threshold else None

def predict_disease_from_symptoms(symptoms_list, augmented_df):
    """Predict disease based on symptoms using cosine similarity - Optimized with vectorization"""
    if augmented_df is None:
        return None
    
    try:
        # Get symptom columns (all columns except diseases and diseases_clean)
        symptom_columns = [col for col in augmented_df.columns if col not in ['diseases', 'diseases_clean']]
        
        # Build query vector
        query_vector = np.zeros(len(symptom_columns))
        for symptom in symptoms_list:
            symptom_clean = symptom.lower().strip().replace(' ', '_')
            if symptom_clean in symptom_columns:
                idx = symptom_columns.index(symptom_clean)
                query_vector[idx] = 1
        
        # Vectorized cosine similarity calculation (OPTIMIZED)
        # Extract all disease vectors at once instead of iterating
        disease_matrix = augmented_df[symptom_columns].values.astype(float)
        
        # Calculate similarities for all diseases at once
        similarities_scores = cosine_similarity([query_vector], disease_matrix)[0]
        
        # Find the best match
        if len(similarities_scores) > 0:
            best_idx = np.argmax(similarities_scores)
            best_disease = augmented_df.iloc[best_idx]['diseases']
            best_score = similarities_scores[best_idx]
            best_vector = disease_matrix[best_idx]
            return (best_disease, best_score, best_vector)
        
        return None
    except Exception as e:
        st.warning(f"Error in disease prediction: {e}")
        return None

def get_disease_symptoms(disease_name, symptoms_df, augmented_df):
    """Get all symptoms for a given disease"""
    if not disease_name:
        return []
    
    disease_clean = disease_name.lower().strip()
    
    symptoms = []
    
    # Try augmented dataset first
    if augmented_df is not None and 'diseases_clean' in augmented_df.columns:
        try:
            aug_match = augmented_df[augmented_df['diseases_clean'] == disease_clean]
            if not aug_match.empty:
                symptom_columns = [col for col in augmented_df.columns if col not in ['diseases', 'diseases_clean']]
                for col in symptom_columns:
                    if col in aug_match.columns and not aug_match.empty and aug_match[col].values[0] == 1:
                        symptoms.append(col.replace('_', ' '))
        except:
            pass
    
    # Fallback to symptoms dataset
    if not symptoms and symptoms_df is not None and 'Disease_clean' in symptoms_df.columns:
        try:
            symptom_match = symptoms_df[symptoms_df['Disease_clean'] == disease_clean]
            if not symptom_match.empty:
                for col in symptom_match.columns:
                    if col.startswith('Symptom_') and pd.notna(symptom_match[col].values[0]):
                        symptom = str(symptom_match[col].values[0]).strip()
                        if symptom and symptom != 'nan':
                            symptoms.append(symptom)
        except:
            pass
    
    return symptoms

def get_disease_precautions(disease_name, precautions_df):
    """Get precautions for a given disease"""
    if precautions_df is None or not disease_name:
        return []
    
    disease_clean = disease_name.lower().strip()
    precautions = []
    
    try:
        if 'Disease_clean' in precautions_df.columns:
            prec_match = precautions_df[precautions_df['Disease_clean'] == disease_clean]
            
            if not prec_match.empty:
                for col in ['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']:
                    if col in prec_match.columns and pd.notna(prec_match[col].values[0]):
                        precaution = str(prec_match[col].values[0]).strip()
                        if precaution and precaution != 'nan':
                            precautions.append(precaution)
    except Exception as e:
        st.warning(f"Error getting precautions: {e}")
    
    return precautions

def get_disease_description(disease_name, faq_df):
    """Get description for a disease from FAQ dataset"""
    if faq_df is None or not disease_name:
        return None
    
    disease_clean = disease_name.lower().strip()
    
    try:
        # Look for questions about this disease
        if 'question_clean' in faq_df.columns:
            relevant_qa = faq_df[faq_df['question_clean'].str.contains(disease_clean, na=False)]
            if not relevant_qa.empty:
                return relevant_qa.iloc[0]['answer']
    except:
        pass
    
    return None

def classify_input_type(user_input):
    """Improved input type classification"""
    if not user_input:
        return 'question'
    
    user_input_lower = user_input.lower().strip()
    
    # Check for question patterns (with or without question mark)
    question_patterns = [
        r'what (are|is)',
        r'how (to|do|can)',
        r'why (is|are)',
        r'when (should|do)',
        r'where (can|do)',
        r'who (should|can)',
        r'can you',
        r'could you',
        r'would you',
        r'explain',
        r'tell me about'
    ]
    
    is_question = any(re.search(pattern, user_input_lower) for pattern in question_patterns)
    has_question_mark = '?' in user_input
    
    # Check for symptom list (comma-separated and doesn't look like a question)
    has_commas = ',' in user_input
    is_short_phrase = len(user_input.split()) <= 5 and not is_question
    
    if has_question_mark or is_question:
        return 'question'
    elif has_commas and is_short_phrase:
        return 'symptoms'
    else:
        # Check if it's likely a disease name (not a question phrase)
        if not is_question and len(user_input.split()) <= 3:
            return 'disease'
        else:
            # Default to question for ambiguous cases
            return 'question'

def process_user_input(user_input, precautions_df, symptoms_df, faq_df, augmented_df):
    """Process user input and generate appropriate response"""
    
    # Initialize response components
    response = {
        'type': None,
        'disease': None,
        'confidence': 0,
        'symptoms': [],
        'precautions': [],
        'description': None,
        'faq_question': None,
        'faq_answer': None
    }
    
    if not user_input:
        return response
    
    # Classify input type
    input_type = classify_input_type(user_input)
    response['type'] = input_type
    
    try:
        if input_type == 'question':
            # Extract potential disease name from question
            disease_match = re.search(r'(?:symptoms|signs|causes|treatment|of|for)\s+([^?]+)', user_input.lower())
            if disease_match:
                potential_disease = disease_match.group(1).strip()
                # Try to get symptoms directly for symptom questions
                if 'symptom' in user_input.lower() or 'sign' in user_input.lower():
                    symptoms = get_disease_symptoms(potential_disease, symptoms_df, augmented_df)
                    if symptoms:
                        response['type'] = 'disease'
                        response['disease'] = potential_disease
                        response['confidence'] = 0.95
                        response['symptoms'] = symptoms
                        response['precautions'] = get_disease_precautions(potential_disease, precautions_df)
                        response['description'] = get_disease_description(potential_disease, faq_df)
                        return response
            
            # Fallback to FAQ search
            faq_match = find_question_answer(user_input, faq_df)
            if faq_match is not None:
                response['faq_question'] = faq_match['question']
                response['faq_answer'] = faq_match['answer']
            
        elif input_type == 'symptoms':
            symptoms_list = [symptom.strip() for symptom in user_input.split(',')]
            
            # Predict disease
            prediction = predict_disease_from_symptoms(symptoms_list, augmented_df)
            if prediction:
                disease_name, confidence, disease_vector = prediction
                response['disease'] = disease_name
                response['confidence'] = confidence
                
                # Get additional information
                response['symptoms'] = get_disease_symptoms(disease_name, symptoms_df, augmented_df)
                response['precautions'] = get_disease_precautions(disease_name, precautions_df)
                response['description'] = get_disease_description(disease_name, faq_df)
            
        elif input_type == 'disease':
            response['disease'] = user_input
            response['confidence'] = 0.95
            
            # Get disease information
            response['symptoms'] = get_disease_symptoms(user_input, symptoms_df, augmented_df)
            response['precautions'] = get_disease_precautions(user_input, precautions_df)
            response['description'] = get_disease_description(user_input, faq_df)
    
    except Exception as e:
        st.warning(f"Error processing user input: {e}")
    
    return response

def display_chat_message(role, content, response=None):
    """Display a chat message in the appropriate style"""
    if role == 'user':
        st.markdown(f"""
        <div class="user-message">
            <div class="message-header">You</div>
            {content}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="bot-message">
            <div class="message-header">CureHelp+ Assistant 🤖</div>
        """, unsafe_allow_html=True)
        
        if response['type'] == 'question':
            if response['faq_answer']:
                st.markdown("**📘 FAQ Answer**")
                st.markdown(f"**Q:** {response['faq_question']}")
                st.markdown(f"**A:** {response['faq_answer']}")
            else:
                st.markdown("I couldn't find a specific answer to your question in my knowledge base. Please try rephrasing or ask about specific symptoms or diseases.")
        
        elif response['type'] in ['symptoms', 'disease']:
            if response['disease']:
                # Disease prediction section
                st.markdown(f"**🤖 Predicted Disease:** {response['disease']} <span class='confidence-badge'>{response['confidence']:.2f}</span>", unsafe_allow_html=True)
                
                # Associated Symptoms - FIXED: Show ALL symptoms
                if response['symptoms']:
                    st.markdown("**🩺 Associated Symptoms:**")
                    symptoms_text = ""
                    for i, symptom in enumerate(response['symptoms'], 1):  
                        symptoms_text += f"{i}. {symptom}<br>"
                    st.markdown(f'<div class="symptom-list">{symptoms_text}</div>', unsafe_allow_html=True)
                
                # Precautions
                if response['precautions']:
                    st.markdown("**🩹 Precautions / Advice:**")
                    precautions_text = ""
                    for i, precaution in enumerate(response['precautions'], 1):
                        precautions_text += f"{i}. {precaution}<br>"
                    st.markdown(f'<div class="precaution-list">{precautions_text}</div>', unsafe_allow_html=True)

                # Description
                if response['description']:
                    st.markdown("**📘 Description:**")
                    description = response['description']
                    if len(description) > 400:
                        description = description[:400] + "..."
                    st.markdown(description)
            else:
                st.markdown("I couldn't identify a specific disease from those symptoms. Please try being more specific or check your spelling.")
        
        st.markdown("</div>", unsafe_allow_html=True)
def render_chatbot_tab():
    """Render the chatbot interface as a tab in the main app"""
    
    # Load datasets with robust error handling
    with st.spinner("Loading medical databases..."):
        precautions_df, symptoms_df, faq_df, augmented_df = load_datasets()
        if precautions_df is not None:
            precautions_df, symptoms_df, faq_df, augmented_df = preprocess_datasets(
                precautions_df, symptoms_df, faq_df, augmented_df
            )
    
    # Main chat container
    st.markdown("""
    <div class="chat-header">
        <h3 style="margin:0; font-size: 20px;"> CureHelp+ Assistant</h3>
        <p style="margin:5px 0 0 0; font-size: 13px; opacity: 0.9;">Ask questions, describe symptoms, or inquire about diseases</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize chat history - only keep last conversation
    if 'chatbot_history' not in st.session_state:
        st.session_state.chatbot_history = []
    
    # Display chat history
    st.markdown('<div class="chat-history">', unsafe_allow_html=True)
    for message in st.session_state.chatbot_history:
        display_chat_message(message['role'], message['content'], message.get('response'))
    st.markdown('</div>', unsafe_allow_html=True)
    
    
    # Use a form to prevent multiple submissions
    with st.form(key='chat_form', clear_on_submit=True):
        col1, col2 = st.columns([4, 1])
        with col1:
            user_input = st.text_input(
                "Type your message...",
                placeholder="Ask a question or describe symptoms...",
                key="chat_input",
                label_visibility="collapsed"
            )
        with col2:
            submitted = st.form_submit_button("Send", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Process user input 
    if submitted and user_input:
        st.session_state.chatbot_history = []
        
        st.session_state.chatbot_history.append({'role': 'user', 'content': user_input})
        
        with st.spinner("🤔 Analyzing..."):
            response = process_user_input(user_input, precautions_df, symptoms_df, faq_df, augmented_df)
        
        st.session_state.chatbot_history.append({'role': 'bot', 'content': user_input, 'response': response})
        
        st.rerun()