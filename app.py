import string
import streamlit as st
import pickle
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()

# Load model and vectorizer
feature_extraction = pickle.load(open('vectorizer.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))

# Custom CSS
st.markdown("""
    <style>
    body, .stApp {
        background-color: #001f3f !important;
        color: #FFFF00 !important;
    }
    .neon-text {
        color: #FFFF00 !important;
        font-size: 32px !important;
        font-weight: bold;
        font-family: 'Segoe UI', sans-serif;
        margin-bottom: 10px;
        text-align: left;
    }
    .predict-button {
        background-color: white;
        color: #f4a261;
        border: none;
        padding: 0.4em 2em;
        border-radius: 8px;
        font-size: 18px;
        cursor: pointer;
        margin-top: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        transition: transform 0.2s, background-color 0.3s;
    }
    .predict-button:hover {
        background-color: #f4f4f4;
        transform: scale(1.05);
    }
    textarea {
        background-color: #f1f2f6 !important;
        color: #000000 !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    </style>
""", unsafe_allow_html=True)

st.title("📩 Real‑Time Spam Guard")

input_sms = st.text_area("Enter the message")

def transform_text(text):
    text = text.lower()
    text = ''.join([char for char in text if char not in string.punctuation])
    text = text.split()
    text = [ps.stem(word) for word in text if word not in stopwords.words('english')]
    return " ".join(text)

if st.button('Predict'):
    if input_sms.strip():
        transformed_sms = transform_text(input_sms)
        vector_input = feature_extraction.transform([transformed_sms])
        prediction = model.predict(vector_input)[0]
        if prediction == 1:
            st.error("🚨 The message is classified as: **Spam**")
        else:
            st.success("✅ The message is classified as: **Ham (Not Spam)**")
    else:
        st.warning("⚠️ Please enter a valid message to classify.")
