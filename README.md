# Resume AI - ATS Analyzer & Optimizer

A powerful AI-powered tool that helps you analyze and optimize your resume for Applicant Tracking Systems (ATS). This application provides detailed insights, ATS scoring, and AI-generated suggestions to improve your resume's effectiveness.

## 🚀 Features

- **PDF Resume Analysis**: Upload and analyze your PDF resume
- **ATS Score Calculation**: Get a comprehensive score based on:
  - Keyword optimization
  - Section structure
  - Formatting
- **AI-Powered Suggestions**: Receive intelligent recommendations for improving your resume
- **Interactive Chat**: Ask specific questions about your resume and get targeted improvements
- **Real-time Preview**: View your resume while making improvements
- **Keyword Extraction**: Identify important technical and soft skills

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **AI/ML**:
  - OpenAI GPT-4
  - spaCy (NLP)
- **PDF Processing**:
  - pdfplumber
  - PyMuPDF
- **Environment Management**: Conda

## 📋 Prerequisites

- Conda installed ([Miniconda](https://docs.conda.io/en/latest/miniconda.html) recommended)
- OpenAI API key
- Internet connection for AI features

## 🔧 Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/resume-ai.git
cd resume-ai
```

2. Create and activate a Conda environment:

```bash
conda create --name resume-ai-env python=3.9
conda activate resume-ai-env
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Download the spaCy model:

```bash
python -m spacy download en_core_web_sm
```

5. Create a `.env` file in the root directory and add your OpenAI API key:

```
OPENAI_API_KEY=your_api_key_here
```

## 🚀 Usage

1. Start the application:

```bash
streamlit run app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

3. Upload your PDF resume using the file uploader

4. Click "Analyze Resume" to get:

   - ATS score
   - Keyword analysis
   - AI-generated improvement suggestions

5. Use the chat interface to ask specific questions about improving your resume

## 📊 ATS Score Components

The ATS score (out of 100) is calculated based on:

- Keyword optimization (50 points)
- Section structure (30 points)
- Formatting (20 points)

## 🤖 AI Features

The application uses OpenAI's GPT-4 model to:

- Extract relevant keywords
- Generate improvement suggestions
- Provide specific answers to user queries
- Analyze resume content and structure

## 🔒 Security

- Your resume data is processed locally
- OpenAI API calls are made securely
- No resume data is stored permanently
