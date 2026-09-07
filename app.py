import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="My Research Analyzer", layout="wide")
st.title("Research Paper Analyzer 📚")

# Get the API key securely from Streamlit
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except:
    st.error("API Key not found. Please add it to Streamlit Secrets.")

uploaded_files = st.file_uploader("1. Upload your PDF papers", type="pdf", accept_multiple_files=True)
toc = st.text_area("2. Enter your Table of Contents or Paragraph Instructions:", height=200)

if st.button("Analyze and Write"):
    if uploaded_files and toc:
        with st.spinner("Reading papers and writing... this might take a minute."):
            
            # Temporarily save and upload files to Gemini
            gemini_files = []
            for f in uploaded_files:
                with open(f.name, "wb") as temp:
                    temp.write(f.read())
                upload = genai.upload_file(f.name)
                gemini_files.append(upload)
            
            # The strict instructions for the AI
            system_instruction = f"""
            You are an expert academic writer. Analyze the provided research papers and write a section based strictly on the following Table of Contents (TOC) or instructions. 
            Extract factual data and findings. Rephrase to avoid plagiarism, but DO NOT alter the scientific meaning, parameters, or conclusions. 
            If the papers do not contain information for a specific point, state 'Insufficient data' instead of making it up.
            
            User Instructions / TOC:
            {toc}
            """
            
            # Call the model
            model = genai.GenerativeModel('gemini-1.5-pro')
            response = model.generate_content(gemini_files + [system_instruction])
            
            st.success("Done!")
            st.write(response.text)
    else:
        st.warning("Please upload at least one PDF and enter your instructions.")
