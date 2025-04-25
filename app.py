import streamlit as st
import os
from dotenv import load_dotenv
from PIL import Image
import google.generativeai as genai

# Load API Key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# Streamlit page config
st.set_page_config(page_title="Gemini Email Generator", layout="centered", page_icon="assets/favicon.ico")

# Apply full-screen background image
st.markdown("""
    <style>
    body {
        background-image: url('th.jpeg');  /* Correct relative path */
        background-size: cover;
        background-position: center center;
        background-repeat: no-repeat;
        color: #fff;
        font-family: 'Helvetica', sans-serif;
        height: 100vh;  /* Full height */
    }
    .stButton>button {
        background-color: #6366f1;
        border-radius: 12px;
        color: white;
        font-weight: bold;
        transition: transform 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.1);
        background-color: #5a3bdb;
    }
    .stTextArea textarea {
        border-radius: 8px;
        padding: 12px;
    }
    .stFileUploader {
        padding: 20px;
        border-radius: 10px;
        border: 2px dashed #6366f1;
        background-color: rgba(99, 102, 241, 0.1);
        transition: background-color 0.3s ease;
    }
    .stFileUploader:hover {
        background-color: rgba(99, 102, 241, 0.2);
    }
    .stMarkdown {
        color: #e1e1e1;
    }
    .stDownloadButton>button {
        background-color: #34d399;
        border-radius: 12px;
        color: white;
        font-weight: bold;
        transition: transform 0.3s ease;
    }
    .stDownloadButton>button:hover {
        transform: scale(1.1);
        background-color: #10b981;
    }
    </style>
""", unsafe_allow_html=True)

# Streamlit UI
st.title("📧 Gemini Pro Email Generator")
st.caption("Generate contextual emails by uploading a screenshot and entering your request.")

# UI for file upload and query
uploaded_img = st.file_uploader("📤 Upload a Screenshot", type=["png", "jpg", "jpeg"])
query = st.text_area("📝 Your Query", placeholder="e.g., Write a follow-up email for this message...")

# Button to generate the email
generate_btn = st.button("🚀 Generate Email")

# Display uploaded image
if uploaded_img:
    image = Image.open(uploaded_img)
    st.image(image, caption="Uploaded Screenshot", use_container_width=True)

# Generate email and display results
if generate_btn and uploaded_img and query:
    with st.spinner("Generating email using Gemini Pro..."):
        response = model.generate_content([query, image])
        email = response.text

        # Display the generated email
        st.success("✅ Email Generated!")
        st.markdown("### 📬 Result:")
        st.markdown(f'<div class="stMarkdown">{email}</div>', unsafe_allow_html=True)

        # Fancy Download Button
        st.download_button("⬇️ Download Email", email, file_name="generated_email.txt", use_container_width=True)

elif generate_btn:
    st.warning("Please upload a screenshot and enter your query.")
