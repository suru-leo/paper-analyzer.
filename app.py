import streamlit as st
from google import genai
import requests
import urllib.parse

st.set_page_config(page_title="My Research Analyzer", layout="wide")
st.title("Research Paper Analyzer 📚")

# Initialize the modern Gemini client securely using the API key
try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("API Key not found or invalid. Please check your Streamlit Secrets.")

# Create a two-column layout
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. Draft & Discover")
    toc = st.text_area("Enter your Table of Contents or Section Topic:", height=250)
    
    if st.button("🔍 Find Related Papers"):
        if toc:
            with st.spinner("Scanning academic databases..."):
                # Use Gemini 2.5 Flash to extract search keywords
                kw_res = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=f"Extract a highly specific 3 to 5 word academic search query based on this text. Output ONLY the query string, no quotes: {toc}"
                )
                query = kw_res.text.strip()
                
                url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={urllib.parse.quote(query)}&limit=5&fields=title,authors,year,url"
                res = requests.get(url).json()
                
                st.success(f"Found papers for: **{query}**")
                if 'data' in res and len(res['data']) > 0:
                    for paper in res['data']:
                        authors = ", ".join([a['name'] for a in paper.get('authors', [])][:3])
                        year = paper.get('year', 'N/A')
                        title = paper.get('title', 'Unknown Title')
                        link = paper.get('url', '#')
                        
                        st.markdown(f"- **[{title}]({link})** ({year}) by {authors} et al.")
                else:
                    st.warning("No papers found. Try adding more specific terms to your TOC.")
        else:
            st.warning("Please enter a TOC first experience.")

with col2:
    st.subheader("2. Analyze & Write")
    uploaded_files = st.file_uploader("Upload your source PDFs", type="pdf", accept_multiple_files=True)
    
    if st.button("📝 Analyze and Write"):
        if uploaded_files and toc:
            with st.spinner("Reading papers, paraphrasing, and formatting citations..."):
                
                # Pack the uploaded PDF bytes into the contents payload format for the new SDK
                contents_payload = []
                for f in uploaded_files:
                    contents_payload.append({
                        'mime_type': 'application/pdf',
                        'data': f.read()
                    })
                
                # Build the instruction text
                system_instruction = f"""
                You are an expert academic review writer. Analyze the provided research papers and write a comprehensive literature review section based strictly on the following Table of Contents (TOC) or instructions. 

                CRITICAL RULES:
                1. PARAPRASING & REVIEW STYLE: Do NOT copy sentences verbatim from the source papers. Completely rephrase and synthesize the information in your own academic voice suitable for a review article. Avoid plagiarism entirely while strictly preserving the original scientific meaning, data points, mechanisms, and conclusions.
                2. INLINE CITATIONS: For every sentence or factual claim you write, identify the title of the source paper (as found on its first page). Insert the article title in parentheses immediately before the final full stop of that sentence, formatted precisely like this: "...rephrased scientific statement here (Exact Article Title on First Page)."
                3. If the provided papers do not contain information for a specific TOC item, state 'Insufficient data' instead of guessing.
                
                User Instructions / TOC:
                {toc}
                """
                
                # Append the instruction text to the payload array
                contents_payload.append(system_instruction)
                
                # Generate content using the stable gemini-2.5-flash model
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=contents_payload
                )
                
                st.write(response.text)
        else:
            st.warning("Please upload at least one PDF and enter your TOC.")
