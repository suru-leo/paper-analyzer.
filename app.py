import streamlit as st
import google.generativeai as genai
import requests
import urllib.parse

st.set_page_config(page_title="My Research Analyzer", layout="wide")
st.title("Research Paper Analyzer 📚")

# Get the API key securely
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-pro')
except:
    st.error("API Key not found. Please add it to Streamlit Secrets.")

# Create a two-column layout
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. Draft & Discover")
    toc = st.text_area("Enter your Table of Contents or Section Topic:", height=250)
    
    if st.button("🔍 Find Related Papers"):
        if toc:
            with st.spinner("Scanning academic databases..."):
                kw_prompt = f"Extract a highly specific 3 to 5 word academic search query based on this text. Output ONLY the query string, no quotes: {toc}"
                kw_response = model.generate_content(kw_prompt)
                query = kw_response.text.strip()
                
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
                    st.warning("No papers found. Try adding more specific scientific terms to your TOC.")
        else:
            st.warning("Please enter a TOC first.")

with col2:
    st.subheader("2. Analyze & Write")
    uploaded_files = st.file_uploader("Upload your source PDFs", type="pdf", accept_multiple_files=True)
    
    if st.button("📝 Analyze and Write"):
        if uploaded_files and toc:
            with st.spinner("Reading papers, paraphrasing, and formatting citations..."):
                
                # Temporarily save and upload files to Gemini
                gemini_files = []
                for f in uploaded_files:
                    with open(f.name, "wb") as temp:
                        temp.write(f.read())
                    upload = genai.upload_file(f.name)
                    gemini_files.append(upload)
                
                # Enhanced system instruction for review-style rewriting and inline citations
                system_instruction = f"""
                You are an expert academic review writer. Analyze the provided research papers and write a comprehensive literature review section based strictly on the following Table of Contents (TOC) or instructions. 

                CRITICAL RULES:
                1. PARAPRASING & REVIEW STYLE: Do NOT copy sentences verbatim from the source papers. Completely rephrase and synthesize the information in your own academic voice suitable for a review article. Avoid plagiarism entirely while strictly preserving the original scientific meaning, data points, mechanisms, and conclusions.
                2. INLINE CITATIONS: For every sentence or factual claim you write, identify the title of the source paper (as found on its first page). Insert the article title in parentheses immediately before the final full stop of that sentence, formatted precisely like this: "...rephrased scientific statement here (Exact Article Title on First Page)."
                3. If the provided papers do not contain information for a specific TOC item, state 'Insufficient data' instead of guessing.
                
                User Instructions / TOC:
                {toc}
                """
                
                # Generate the text
                response = model.generate_content(gemini_files + [system_instruction])
                st.write(response.text)
        else:
            st.warning("Please upload at least one PDF and enter your TOC.")
