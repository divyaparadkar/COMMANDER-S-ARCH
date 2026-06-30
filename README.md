# 🎖️ COMMANDER'S ARCH - Services Selection Board (SSB) Preparation Portal

**Commander's Arch** is a comprehensive, AI-powered preparation portal designed to help candidates prepare for the Services Selection Board (SSB) interviews for the Indian Armed Forces. The platform simulates various screening and psychological tests, analyzes candidate performance, and provides detailed feedback to help build Officer Like Qualities (OLQs).

[![Streamlit App](https://static.streamlit.io/badge-streamlit.svg)](https://commander-s-arch-ajundgxe6nb8j986cpgvbj.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🚀 Live Demo

Access the hosted application on Streamlit Community Cloud:  
👉 **[Commander's Arch Live Portal](https://commander-s-arch-ajundgxe6nb8j986cpgvbj.streamlit.app/)**

---

## 🌟 Key Features

The application simulates the complete SSB selection process through 10 dedicated modules:

1. **📋 PIQ Form Digitizer**: Digitizes and stores the Personal Information Questionnaire (PIQ). It uses AI to analyze your PIQ and predict potential questions that the Interviewing Officer (IO) might ask.
2. **📐 OIR Practice Exam**: Timed practice tests for Officer Intelligence Rating (Verbal and Non-Verbal reasoning) to clear the Stage-1 screening.
3. **🖼️ PPDT / TAT Mode**: Simulates Picture Perception & Description Test (Stage-1) and Thematic Apperception Test (Stage-2 Psych). View images on a timer and write stories.
4. **✍️ WAT (Word Association Test)**: Rapid-fire word association module with auto-advancing slides on a 15-second timer.
5. **🧠 SRT (Situation Reaction Test)**: React to 60 real-life situations under a strict time limit to evaluate decision-making.
6. **🗣️ GTO Lecturette**: Choose from curated topics, prepare for 3 minutes, record your speech, and get AI-powered evaluation of your communication, content, and delivery.
7. **🎙️ Speech & Mock Interview**: Simulate the personal interview round. Respond to AI-generated questions based on your PIQ using voice/text and receive assessment.
8. **📊 Performance Dashboard**: Detailed historical analysis of all your attempts with performance metrics, feedback logs, and progress tracking.
9. **📚 Daily Newspaper Vocab**: Daily vocab builder with definitions, usage examples, and antonyms/synonyms to boost expression.
10. **🤝 Get Free Guidance**: Connect with recommended resources, mentorship channels, and study materials.

---

## 🛠️ Tech Stack

- **Frontend/Interactive UI**: [Streamlit](https://streamlit.io/) (with customized glassmorphism styling, responsive navigation, and embedded HTML/CSS components).
- **Core Logic**: Python 3.9+
- **AI Integration**: Google Gemini API (via `google-generativeai`) for real-time text analysis, feedback generation, and interview generation.
- **Database**: SQLite3 (stores credentials, attempt history, PIQ records, and session keys).
- **Text-to-Speech & Speech-to-Text**: `gTTS` (Google Text-to-Speech) & `SpeechRecognition` / `streamlit-mic-recorder` for speech input/output.
- **Data Manipulation**: `pandas`, `pillow` (PIL).

---

## 📁 Project Structure

```bash
SSB_prep/
├── streamlit_app.py     # Main Streamlit application and page router
├── database.py          # SQLite database initialization and helper functions
├── data_bank.py         # Static datasets for WAT, SRT, OIR, and Lecturettes
├── image_bank.py        # Curated URLs, local image pointers, and logos
├── text_analyzer.py     # Gemini AI prompt engineering and local text processing
├── requirements.txt     # Python package dependencies
├── ssb_prep.db          # SQLite Database (Auto-created)
├── ppdt images/         # Local assets for PPDT / TAT pictures
└── README.md            # Project documentation
```

---

## ⚙️ Installation & Local Setup

To run Commander's Arch locally on your system, follow these steps:

### 1. Clone the Repository
```bash
git clone https://github.com/divyaparadkar/COMMANDER-S-ARCH.git
cd COMMANDER-S-ARCH
```

### 2. Set Up a Virtual Environment
**On Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```
**On macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit Application
```bash
streamlit run streamlit_app.py
```

---

## ☁️ Hosted Deployment

The application is deployed on **Streamlit Community Cloud**. Continuous integration is configured so that any changes pushed to the `main` branch of the GitHub repository are automatically deployed to the production server.

### Deploying Updates:
Simply commit and push changes:
```bash
git add .
git commit -m "Update portal features"
git push origin main
```

---

## 🎖️ About the Project
Commander's Arch was built with the goal of providing high-quality, accessible SSB preparation resources to defence aspirants, leveraging modern AI to simulate the rigorous screening and psychological testing standard of the Armed Forces.
