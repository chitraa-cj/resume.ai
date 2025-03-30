import streamlit as st
import os
import pdfplumber
import spacy
import openai
from openai import OpenAI
from dotenv import load_dotenv
import base64
from io import BytesIO

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Ensure Spacy Model is Available
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

class ResumeAnalyzer:
    def __init__(self):
        self.nlp = nlp

    def extract_text_from_pdf(self, file_bytes):
        """Extracts text from uploaded PDF resume."""
        try:
            with pdfplumber.open(BytesIO(file_bytes)) as pdf:
                text = "\n".join(page.extract_text() or "" for page in pdf.pages)
                return text if text.strip() else None
        except Exception as e:
            st.error(f"Error extracting PDF: {e}")
            return None

    def extract_keywords(self, resume_text):
        """Extracts important keywords from the resume."""
        prompt = f"Extract the most important technical and soft skills keywords from this resume:\n\n{resume_text[:3000]}"  
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "system", "content": "You are an expert in resume analysis."},
                          {"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content.split(", ")
        except Exception as e:
            return ["Error extracting keywords"]

    def analyze_ats_score(self, resume_text):
        """Calculates an estimated ATS score based on keyword presence and resume structure."""
        extracted_keywords = self.extract_keywords(resume_text)
        keyword_matches = {kw: resume_text.lower().count(kw.lower()) for kw in extracted_keywords}

        section_headers = ['education', 'experience', 'skills', 'projects', 'certifications']
        found_sections = sum(1 for section in section_headers if section in resume_text.lower())

        keyword_score = min(len(extracted_keywords) * 2, 50)
        section_score = (found_sections / len(section_headers)) * 30
        formatting_score = 20 if found_sections == len(section_headers) else 10

        return round(keyword_score + section_score + formatting_score, 2), keyword_matches, found_sections

    def generate_ai_suggestions(self, user_query, resume_text):
        """Provides AI-generated suggestions for improving the resume based on a user query."""
        if not resume_text or len(resume_text.strip()) == 0:
            return "Error: No valid resume text extracted."

        prompt = f"""
        Analyze the following resume and provide direct improvements based on the query.

        **Resume:**
        {resume_text[:4000]}

        **User Query:**
        {user_query}

        **Response Format:**
        - **Original:** [Existing content]  
        - **Suggested Replacement:** [Improved version]
        """

        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "system", "content": "You are an expert resume reviewer helping optimize for ATS systems."},
                          {"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"AI Suggestion Generation Error: {str(e)}"

def display_pdf(file_bytes):
    """Displays the uploaded PDF resume."""
    base64_pdf = base64.b64encode(file_bytes).decode("utf-8")
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600px"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def main():
    """Streamlit UI for resume analysis."""
    st.set_page_config(page_title="AI-Powered Resume ATS Optimizer", layout="wide")
    st.title("📄 Resume ATS Analyzer & AI Optimizer")

    analyzer = ResumeAnalyzer()

    # Initialize session state
    if "resume_text" not in st.session_state:
        st.session_state.resume_text = None
        st.session_state.file_bytes = None
        st.session_state.ats_score = None
        st.session_state.keyword_matches = None
        st.session_state.found_sections = None
        st.session_state.ai_suggestions = None
        st.session_state.chat_history = []

    # Upload resume
    uploaded_file = st.file_uploader("📤 Upload Resume (PDF)", type=["pdf"])
    
    if uploaded_file:
        file_bytes = uploaded_file.read()
        st.session_state.resume_text = analyzer.extract_text_from_pdf(file_bytes)
        st.session_state.file_bytes = file_bytes

    # Display extracted resume text
    if st.session_state.resume_text:
        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("📄 Extracted Resume Text")
            st.text_area("Resume Content", st.session_state.resume_text, height=400)

        with col2:
            st.subheader("📑 Resume Preview")
            display_pdf(st.session_state.file_bytes)

        # Analyze resume when button is clicked
        if st.button("🔍 Analyze Resume"):
            ats_score, keyword_matches, found_sections = analyzer.analyze_ats_score(st.session_state.resume_text)
            ai_suggestions = analyzer.generate_ai_suggestions("General resume improvement", st.session_state.resume_text)

            st.session_state.ats_score = ats_score
            st.session_state.keyword_matches = keyword_matches
            st.session_state.found_sections = found_sections
            st.session_state.ai_suggestions = ai_suggestions

        # Display ATS results
        if st.session_state.ats_score is not None:
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("📊 ATS Score & Insights")
                st.write(f"**Total Score:** {st.session_state.ats_score}/100")
                st.write(f"**Extracted Keywords:** {list(st.session_state.keyword_matches.keys())}")
                st.write(f"**Sections Found:** {st.session_state.found_sections}/5")

            with col2:
                st.subheader("💡 AI Resume Improvement Suggestions")
                st.markdown(st.session_state.ai_suggestions)

            # Allow user to ask AI for more resume improvements
            st.subheader("💬 Improve Further")
            user_query = st.text_input("Ask AI to refine your resume further:")

            if user_query:
                additional_suggestions = analyzer.generate_ai_suggestions(user_query, st.session_state.resume_text)
                st.session_state.chat_history.append({"user": user_query, "ai": additional_suggestions})
                st.markdown(additional_suggestions)

            # Display chat history
            st.subheader("📜 Chat History")
            for chat in st.session_state.chat_history:
                st.markdown(f"👤 **You:** {chat['user']}")
                st.markdown(f"🤖 **AI:** {chat['ai']}")

if __name__ == "__main__":
    main()
