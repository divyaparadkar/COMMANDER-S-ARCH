import streamlit as st  # pyrefly: ignore [missing-import]
import time
import os
import random
from image_bank import get_random_ppdt, get_ppdt_logo, get_wat_logo, get_srt_logo, get_interview_logo, get_piq_logo, get_oir_logo, get_lecturette_logo, get_dashboard_logo, get_main_app_logo
from text_analyzer import local_analyze_text, gemini_analyze_text, generate_interview_questions, evaluate_interview_answer, analyze_piq_data, evaluate_lecturette_speech
from data_bank import WAT_WORDS, SRT_SITUATIONS, OIR_VERBAL_QUESTIONS, OIR_NON_VERBAL_QUESTIONS, LECTURETTE_TOPICS
from gtts import gTTS  # pyrefly: ignore [missing-import]
import speech_recognition as sr  # pyrefly: ignore [missing-import]
from streamlit_mic_recorder import mic_recorder  # pyrefly: ignore [missing-import]
import io

# Set page config
st.set_page_config(
    page_title="COMMANDER'S ARCH - FOR SSB PREPARATION",
    page_icon="🎖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Styling
st.markdown("""
<style>
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .stApp {
        background: linear-gradient(-45deg, #070a13, #0f172a, #150f2e, #0a0f1d) !important;
        background-size: 400% 400% !important;
        animation: gradientBG 20s ease infinite !important;
    }
    .block-container {
        max-width: 95% !important;
        padding-left: 2.5rem !important;
        padding-right: 2.5rem !important;
        padding-top: 1.5rem !important;
        padding-bottom: 1.5rem !important;
    }
    .main {
        background: transparent !important;
        color: #f8fafc;
    }
    
    /* Ensure high contrast readable text inside all views and modules */
    .stMarkdown, p, span, label, .stText, div[data-testid="stMarkdownContainer"] {
        color: #f1f5f9 !important;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    label[data-testid="stWidgetLabel"] p {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #1e293b !important;
        color: #ffffff !important;
    }
    input, textarea {
        color: #ffffff !important;
        background-color: #1e293b !important;
    }
    
    .stButton>button {
        background-color: #2563eb;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #1d4ed8;
        transform: translateY(-2px);
    }
    .card {
        background-color: #1e293b;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 1px solid #334155;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    }
    .olq-tag {
        display: inline-block;
        background-color: #1e3a8a;
        color: #93c5fd;
        border-radius: 16px;
        padding: 0.25rem 0.75rem;
        font-size: 0.85rem;
        margin: 0.25rem;
        font-weight: bold;
    }
    .feedback-item {
        background-color: #311c1c;
        border-left: 4px solid #ef4444;
        padding: 0.75rem;
        border-radius: 4px;
        margin-bottom: 0.5rem;
    }
    .success-item {
        background-color: #143021;
        border-left: 4px solid #22c55e;
        padding: 0.75rem;
        border-radius: 4px;
        margin-bottom: 0.5rem;
    }
    h1, h2, h3 {
        font-family: 'Outfit', 'Inter', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

def render_page_navigation(current_mode_name, key_prefix):
    modules = [
        "📋 PIQ Form Digitizer",
        "📐 OIR Practice Exam",
        "🖼️ PPDT / TAT Mode",
        "✍️ WAT (Word Association)",
        "🧠 SRT (Situation Reaction)",
        "🗣️ GTO Lecturette",
        "🎙️ Speech & Mock Interview",
        "📊 Performance Dashboard"
    ]
    try:
        idx = modules.index(current_mode_name)
    except ValueError:
        idx = -1
        
    col1, col2, col3 = st.columns([1.5, 1, 1.5])
    
    with col1:
        if idx > 0:
            prev_label = f"⬅️ {modules[idx-1]}"
            if st.button(prev_label, key=f"{key_prefix}_prev", use_container_width=True):
                st.session_state.current_mode = modules[idx-1]
                st.rerun()
        else:
            if st.button("⬅️ Main Dashboard", key=f"{key_prefix}_prev_home", use_container_width=True):
                st.session_state.current_mode = "None Selected"
                st.rerun()
                
    with col2:
        if st.button("🏠 Home", key=f"{key_prefix}_home", use_container_width=True):
            st.session_state.current_mode = "None Selected"
            st.rerun()
            
    with col3:
        if idx >= 0 and idx < len(modules) - 1:
            next_label = f"{modules[idx+1]} ➡️"
            if st.button(next_label, key=f"{key_prefix}_next", use_container_width=True):
                st.session_state.current_mode = modules[idx+1]
                st.rerun()
        else:
            if st.button("🏠 Main Dashboard ➡️", key=f"{key_prefix}_next_home", use_container_width=True):
                st.session_state.current_mode = "None Selected"
                st.rerun()
    st.markdown("---")

# Initialize Session State
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
if 'history' not in st.session_state:
    st.session_state.history = []
if 'wat_active' not in st.session_state:
    st.session_state.wat_active = False
if 'wat_session_words' not in st.session_state:
    st.session_state.wat_session_words = []
if 'wat_index' not in st.session_state:
    st.session_state.wat_index = 0
if 'wat_responses' not in st.session_state:
    st.session_state.wat_responses = []
if 'interview_active' not in st.session_state:
    st.session_state.interview_active = False
if 'interview_questions' not in st.session_state:
    st.session_state.interview_questions = []
if 'interview_index' not in st.session_state:
    st.session_state.interview_index = 0
if 'interview_responses' not in st.session_state:
    st.session_state.interview_responses = []
if 'piq_data' not in st.session_state:
    st.session_state.piq_data = {
        "board_no": "",
        "board_place": "",
        "batch_no": "",
        "chest_no": "",
        "upsc_roll": "",
        "name": "",
        "father_name": "",
        "max_residence": "",
        "present_address": "",
        "present_pop": "",
        "permanent_address": "",
        "permanent_pop": "",
        "is_dist_hq": "No",
        "state_district": "",
        "religion": "",
        "category": "General",
        "mother_tongue": "",
        "dob": None,
        "marital_status": "Single",
        "parents_alive": "Yes",
        "age_at_death": "",
        "parents_particulars": [
            {"Particulars": "Father", "Education": "", "Occupation": "", "Income per Month": ""},
            {"Particulars": "Mother", "Education": "", "Occupation": "", "Income per Month": ""},
            {"Particulars": "Guardian", "Education": "", "Occupation": "", "Income per Month": ""}
        ],
        "education_record": [
            {"S.No.": "(a)", "Qualification": "Matric / Hr. Sec.", "Institution": "", "Year": "", "Division & %": "", "Medium": "", "Boarder/Day Scholar": "Day Scholar", "Outstanding Achievement": ""},
            {"S.No.": "(b)", "Qualification": "10+2 Equivalent", "Institution": "", "Year": "", "Division & %": "", "Medium": "", "Boarder/Day Scholar": "Day Scholar", "Outstanding Achievement": ""},
            {"S.No.": "(c)", "Qualification": "B.A. / B.Sc. / B.com", "Institution": "", "Year": "", "Division & %": "", "Medium": "", "Boarder/Day Scholar": "Day Scholar", "Outstanding Achievement": ""},
            {"S.No.": "(d)", "Qualification": "Professional", "Institution": "", "Year": "", "Division & %": "", "Medium": "", "Boarder/Day Scholar": "Day Scholar", "Outstanding Achievement": ""}
        ],
        "brothers_sisters_count": "",
        "sibling_ranking": "",
        "sibling_info": "",
        "age_years": "",
        "age_months": "",
        "height_m": "",
        "weight_kg": "",
        "present_occupation_income": "",
        "ncc_training": "No",
        "ncc_details": [
            {"Total Training": "", "Wing": "", "Division": "", "Certificate Obtained": ""}
        ],
        "sports_participation": [
            {"Games / Sports": "", "Duration of Participation": "", "Represented School/College": "", "Outstanding Achievement": ""}
        ],
        "hobbies": "",
        "extracurricular": [
            {"Group Activity": "", "Duration": "", "Outstanding Achievement": ""}
        ],
        "responsibilities": "",
        "commission_type": "",
        "choice_of_service": "",
        "previous_attempts_count": "0",
        "previous_attempts_details": [
            {"S.No.": "1", "Type of Entry": "", "Place & SSB No.": "", "Date": "", "Batch & Chest No.": "", "Result": ""}
        ]
    }

if 'oir_state' not in st.session_state:
    st.session_state.oir_state = "configure"
if 'oir_verbal_answers' not in st.session_state:
    st.session_state.oir_verbal_answers = {}
if 'oir_non_verbal_answers' not in st.session_state:
    st.session_state.oir_non_verbal_answers = {}
if 'oir_verbal_start_time' not in st.session_state:
    st.session_state.oir_verbal_start_time = 0.0
if 'oir_non_verbal_start_time' not in st.session_state:
    st.session_state.oir_non_verbal_start_time = 0.0
if 'oir_break_start_time' not in st.session_state:
    st.session_state.oir_break_start_time = 0.0
if 'oir_verbal_questions' not in st.session_state:
    st.session_state.oir_verbal_questions = []
if 'oir_non_verbal_questions' not in st.session_state:
    st.session_state.oir_non_verbal_questions = []
if 'oir_verbal_index' not in st.session_state:
    st.session_state.oir_verbal_index = 0
if 'oir_non_verbal_index' not in st.session_state:
    st.session_state.oir_non_verbal_index = 0

if 'lecturette_state' not in st.session_state:
    st.session_state.lecturette_state = "configure"
if 'lecturette_topics_pool' not in st.session_state:
    st.session_state.lecturette_topics_pool = []
if 'lecturette_selected_topic' not in st.session_state:
    st.session_state.lecturette_selected_topic = ""
if 'lecturette_prep_start_time' not in st.session_state:
    st.session_state.lecturette_prep_start_time = 0.0
if 'lecturette_speak_start_time' not in st.session_state:
    st.session_state.lecturette_speak_start_time = 0.0
if 'lecturette_notes' not in st.session_state:
    st.session_state.lecturette_notes = ""
if 'lecturette_evaluation' not in st.session_state:
    st.session_state.lecturette_evaluation = {}

# Splash Screen
if 'splash_shown' not in st.session_state:
    st.session_state.splash_shown = False

if not st.session_state.splash_shown:
    st.markdown(
        """
        <style>
            [data-testid="stHeader"] { display: none !important; }
            [data-testid="stSidebar"] { display: none !important; }
            .block-container { padding: 0px !important; max-width: 100% !important; }
            iframe { height: 100vh !important; width: 100vw !important; border: none !important; }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.components.v1.html(
        """
        <div class="splash-container">
            <div class="military-crest">
                <svg width="120" height="120" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                    <defs>
                        <linearGradient id="shieldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stop-color="#3b82f6" />
                            <stop offset="100%" stop-color="#10b981" />
                        </linearGradient>
                        <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
                            <feGaussianBlur stdDeviation="4" result="blur" />
                            <feComposite in="SourceGraphic" in2="blur" operator="over" />
                        </filter>
                    </defs>
                    <path d="M 50 12 L 82 25 L 82 58 C 82 82 50 94 50 94 C 50 94 18 82 18 58 L 18 25 Z" 
                          fill="none" stroke="url(#shieldGrad)" stroke-width="4" filter="url(#glow)">
                        <animate attributeName="stroke-dasharray" values="0,300;300,0;0,300" dur="4s" repeatCount="indefinite"/>
                    </path>
                    <circle cx="50" cy="53" r="20" fill="none" stroke="#60a5fa" stroke-width="1" opacity="0.4" />
                    <circle cx="50" cy="53" r="10" fill="none" stroke="#60a5fa" stroke-width="1" opacity="0.2" />
                    <line x1="50" y1="53" x2="70" y2="53" stroke="#10b981" stroke-width="2" stroke-linecap="round">
                        <animateTransform attributeName="transform" type="rotate" from="0 50 53" to="360 50 53" dur="2s" repeatCount="indefinite"/>
                    </line>
                    <polygon points="50,43 53,50 60,53 53,56 50,63 47,56 40,53 47,50" fill="#facc15" />
                </svg>
            </div>
            <div class="app-title">COMMANDER'S ARCH</div>
            <div class="app-subtitle">FOR SSB PREPARATION</div>
            <div class="progress-bar-container">
                <div class="progress-bar-fill"></div>
            </div>
            <div class="status-text">Loading AI Cognitive Engines & Logic Models...</div>
        </div>

        <style>
            @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Inter:wght@400;500&display=swap');
            
            body {
                margin: 0;
                background-color: #0f172a;
                font-family: 'Inter', sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                width: 100vw;
                overflow: hidden;
            }
            .splash-container {
                text-align: center;
                background-color: #1e293b;
                padding: 40px 60px;
                border-radius: 16px;
                border: 1px solid #334155;
                box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3), 0 8px 10px -6px rgba(0, 0, 0, 0.3);
                max-width: 480px;
                width: 90%;
                box-sizing: border-box;
            }
            .military-crest {
                margin-bottom: 25px;
                display: inline-block;
            }
            .app-title {
                color: #ffffff;
                font-family: 'Outfit', sans-serif;
                font-size: 1.6rem;
                font-weight: 700;
                margin-bottom: 8px;
                letter-spacing: 0.5px;
            }
            .app-subtitle {
                color: #10b981;
                font-family: 'Outfit', sans-serif;
                font-size: 0.9rem;
                font-weight: 600;
                letter-spacing: 3px;
                margin-bottom: 30px;
            }
            .progress-bar-container {
                background-color: #334155;
                height: 6px;
                border-radius: 3px;
                width: 100%;
                overflow: hidden;
                margin-bottom: 15px;
            }
            .progress-bar-fill {
                background: linear-gradient(90deg, #3b82f6, #10b981);
                height: 100%;
                width: 0%;
                border-radius: 3px;
                animation: fill-progress 2.2s cubic-bezier(0.4, 0, 0.2, 1) forwards;
            }
            .status-text {
                color: #94a3b8;
                font-size: 0.85rem;
                font-weight: 400;
                animation: pulse 1.5s infinite ease-in-out;
            }
            
            @keyframes fill-progress {
                0% { width: 0%; }
                20% { width: 15%; }
                50% { width: 60%; }
                80% { width: 85%; }
                100% { width: 100%; }
            }
            @keyframes pulse {
                0%, 100% { opacity: 0.6; }
                50% { opacity: 1; }
            }
        </style>
        """,
        height=1000
    )
    time.sleep(2.5)
    st.session_state.splash_shown = True
    st.rerun()

# Sidebar Navigation & Settings
if 'current_mode' not in st.session_state:
    st.session_state.current_mode = "None Selected"

st.sidebar.markdown("<h1 style='text-align: center; color: #3b82f6; margin-bottom: 0px;'>🎖️ COMMANDER'S ARCH</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; color: #10b981; font-weight: bold; font-size: 0.85rem; letter-spacing: 2px; margin-top: 0px;'>FOR SSB PREPARATION</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")

test_mode_options = ["None Selected", "📋 PIQ Form Digitizer", "📐 OIR Practice Exam", "🖼️ PPDT / TAT Mode", "✍️ WAT (Word Association)", "🧠 SRT (Situation Reaction)", "🗣️ GTO Lecturette", "🎙️ Speech & Mock Interview", "📊 Performance Dashboard"]
selected_index = test_mode_options.index(st.session_state.current_mode) if st.session_state.current_mode in test_mode_options else 0

sidebar_mode = st.sidebar.selectbox(
    "Quick Navigation",
    test_mode_options,
    index=selected_index
)
if sidebar_mode != st.session_state.current_mode:
    st.session_state.current_mode = sidebar_mode
    st.rerun()

test_mode = st.session_state.current_mode

st.sidebar.markdown("---")
st.sidebar.subheader("Settings & API Config")
api_key_input = st.sidebar.text_input(
    "Google Gemini API Key",
    type="password",
    value=st.session_state.api_key,
    placeholder="Enter API Key for deep psychological analysis...",
    help="Using a Gemini API Key enables detailed AI evaluation of Officer Like Qualities (OLQs) and constructive personality feedback. Without it, the app uses local NLTK processing."
)
if api_key_input != st.session_state.api_key:
    st.session_state.api_key = api_key_input

# Helpers
def save_analysis(test_type, text, analysis, context=""):
    st.session_state.history.append({
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "test_type": test_type,
        "text": text,
        "context": context,
        "analysis": analysis
    })

def render_analysis_results(res):
    st.markdown("### 📊 Psychological Analysis Report")
    
    # Sentiment & Confidence columns
    col1, col2 = st.columns(2)
    with col1:
        sentiment = res.get("sentiment", 0.0)
        st.metric(
            label="Sentiment / Attitude Index",
            value=f"{sentiment:+.2f}",
            delta="Positive / Active Outlook" if sentiment >= 0.1 else ("Negative / Anxious Outlook" if sentiment <= -0.1 else "Neutral Outlook"),
            delta_color="normal" if sentiment >= 0.1 else ("inverse" if sentiment <= -0.1 else "off")
        )
    with col2:
        conf = res.get("confidence_score", 0.5)
        st.metric(
            label="Confidence / Resolve Score",
            value=f"{conf * 100:.0f}%",
            delta="High Resolve" if conf >= 0.7 else ("Low Resolve / Hesitant" if conf <= 0.4 else "Moderate Resolve")
        )
    
    # OLQs Demonstrated
    st.markdown("#### 🌟 Officer Like Qualities (OLQs) Highlighted")
    olqs = res.get("olqs_demonstrated", {})
    if olqs:
        for olq, explanation in olqs.items():
            st.markdown(f"<span class='olq-tag'>{olq}</span> ➔ {explanation}", unsafe_allow_html=True)
    else:
        st.info("No explicit OLQs detected. Try using more active, problem-solving, and team-oriented descriptions.")

    # Overall Psych Evaluation
    st.markdown("#### 🧠 Psychological Profiling")
    st.info(res.get("overall_evaluation", "N/A"))

    # Actionable Feedback
    st.markdown("#### 💡 Actionable Improvement Points")
    feedback = res.get("actionable_feedback", [])
    for fb in feedback:
        if "great" in fb.lower() or "good" in fb.lower() or "excellent" in fb.lower():
            st.markdown(f"<div class='success-item'>✔️ {fb}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='feedback-item'>⚠️ {fb}</div>", unsafe_allow_html=True)

# -----------------
# 1. PPDT / TAT Mode
# -----------------
if test_mode == "🖼️ PPDT / TAT Mode":
    st.components.v1.html(get_ppdt_logo(), height=130)
    render_page_navigation("🖼️ PPDT / TAT Mode", "ppdt")


    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("Generate Random Picture", key="tat_gen"):
            st.session_state.tat_image = get_random_ppdt()
            st.session_state.tat_start_time = time.time()
            st.session_state.tat_state = "observe"
        
        if 'tat_image' in st.session_state and st.session_state.tat_image:
            # Check file presence
            if os.path.exists(st.session_state.tat_image):
                st.image(st.session_state.tat_image, caption="Observe this image", width="stretch")
            else:
                st.warning("No custom PPDT images found. Please add JPEGs to the 'ppdt images' folder.")
                # Fallback to a placeholder
                st.image("https://picsum.photos/600/400", caption="Mock PPDT Image (Scenic placeholder)", width="stretch")
        else:
            st.info("Click 'Generate Random Picture' above to start your practice session.")

    with col2:
        if 'tat_state' in st.session_state:
            # Observation Countdown
            if st.session_state.tat_state == "observe":
                elapsed = time.time() - st.session_state.tat_start_time
                remaining = int(30 - elapsed)
                if remaining > 0:
                    st.subheader(f"⏱️ Observing Image... {remaining}s remaining")
                    st.progress(max(0, min(1.0, elapsed / 30.0)))
                    time.sleep(1)
                    st.rerun()
                else:
                    st.session_state.tat_state = "write"
                    st.session_state.tat_write_start = time.time()
                    st.rerun()

            # Writing Countdown
            elif st.session_state.tat_state == "write":
                elapsed = time.time() - st.session_state.tat_write_start
                remaining = int(240 - elapsed)
                if remaining > 0:
                    st.subheader(f"✍️ Writing Story... {remaining // 60}m {remaining % 60}s remaining")
                    st.progress(max(0, min(1.0, elapsed / 240.0)))
                    # Let the user write
                    story_text = st.text_area("Write your story here:", height=300, key="tat_story_area")
                    
                    if st.button("Submit Story Now"):
                        st.session_state.tat_state = "analyze"
                        st.session_state.tat_story_final = story_text
                        st.rerun()
                        
                    # Auto-refresh timer details
                    time.sleep(2)
                    st.rerun()
                else:
                    st.warning("⏰ Time is up! Submitting your story automatically.")
                    st.session_state.tat_state = "analyze"
                    st.session_state.tat_story_final = st.session_state.get("tat_story_area", "")
                    st.rerun()

            # Analysis Output
            elif st.session_state.tat_state == "analyze":
                story = st.session_state.get("tat_story_final", "")
                st.subheader("Your Submitted Story")
                st.write(story if story else "*No text entered.*")
                
                with st.spinner("Analyzing psychological traits & OLQs..."):
                    if st.session_state.api_key:
                        analysis = gemini_analyze_text(story, st.session_state.api_key, "TAT/PPDT")
                    else:
                        analysis = local_analyze_text(story)
                        
                    if "error" in analysis and not analysis.get("local_fallback"):
                        st.error(analysis["error"])
                    else:
                        render_analysis_results(analysis)
                        if st.button("Save & Start New Test"):
                            save_analysis("TAT/PPDT", story, analysis)
                            del st.session_state.tat_state
                            del st.session_state.tat_image
                            st.rerun()

# -----------------
# 2. WAT Mode
# -----------------
elif test_mode == "✍️ WAT (Word Association)":
    st.components.v1.html(get_wat_logo(), height=130)
    render_page_navigation("✍️ WAT (Word Association)", "wat")


    if not st.session_state.wat_active:
        if st.button("Start WAT Practice Session"):
            st.session_state.wat_session_words = random.sample(WAT_WORDS, min(15, len(WAT_WORDS)))
            st.session_state.wat_index = 0
            st.session_state.wat_responses = []
            st.session_state.wat_active = True
            st.session_state.wat_word_start = time.time()
            st.rerun()
            
        st.info("Click 'Start WAT Practice Session' to begin.")
    else:
        # Active WAT session
        idx = st.session_state.wat_index
        words_list = st.session_state.wat_session_words
        
        if idx < len(words_list):
            current_word = words_list[idx]
            
            st.subheader(f"Word {idx + 1} of {len(words_list)}")
            st.markdown(f"<h1 style='text-align: center; font-size: 80px; color: #3b82f6;'>{current_word}</h1>", unsafe_allow_html=True)
            
            # Simple form to handle response entry
            with st.form(key=f"wat_form_{idx}"):
                user_sentence = st.text_input("Your Response sentence:", placeholder="Write your immediate association...", autocomplete=None)
                submitted = st.form_submit_button("Next Word ➔")
                
                # Check timer
                elapsed = time.time() - st.session_state.wat_word_start
                remaining = int(15 - elapsed)
                
                if remaining > 0:
                    st.progress(max(0.0, min(1.0, elapsed / 15.0)))
                    st.write(f"⏱️ Time remaining: {remaining} seconds")
                else:
                    # Time ran out
                    st.warning("⏰ Time out! Press the button to proceed to the next word.")
                
                if submitted or remaining <= 0:
                    st.session_state.wat_responses.append({
                        "word": current_word,
                        "response": user_sentence if user_sentence else "[No Response]"
                    })
                    st.session_state.wat_index += 1
                    st.session_state.wat_word_start = time.time()
                    st.rerun()
            
            # Refresh to update timer
            time.sleep(1)
            st.rerun()
        else:
            # WAT finished, show list of responses and run analysis
            st.session_state.wat_active = False
            st.success("🎉 WAT Session Completed!")
            st.subheader("Your Responses")
            
            # Put responses in a nice table
            for r in st.session_state.wat_responses:
                st.markdown(f"**Word:** `{r['word']}` ➔ *{r['response']}*")
                
            # Batch Analysis
            if st.button("Evaluate All WAT Responses"):
                with st.spinner("Analyzing responses for psychological traits..."):
                    combined_text = "\n".join([f"Word: {r['word']} -> Response: {r['response']}" for r in st.session_state.wat_responses])
                    
                    if st.session_state.api_key:
                        analysis = gemini_analyze_text(combined_text, st.session_state.api_key, "WAT")
                    else:
                        analysis = local_analyze_text(combined_text)
                    
                    st.session_state.wat_analysis = analysis
                    st.rerun()
            
            if 'wat_analysis' in st.session_state:
                render_analysis_results(st.session_state.wat_analysis)
                if st.button("Save & Complete Session"):
                    combined_text = "\n".join([f"{r['word']}: {r['response']}" for r in st.session_state.wat_responses])
                    save_analysis("WAT", combined_text, st.session_state.wat_analysis)
                    del st.session_state.wat_responses
                    del st.session_state.wat_analysis
                    st.rerun()

# -----------------
# 3. SRT Mode
# -----------------
elif test_mode == "🧠 SRT (Situation Reaction)":
    st.components.v1.html(get_srt_logo(), height=130)
    render_page_navigation("🧠 SRT (Situation Reaction)", "srt")

    
    if 'current_srt' not in st.session_state:
        st.session_state.current_srt = random.choice(SRT_SITUATIONS)
        
    srt = st.session_state.current_srt
    
    st.markdown(f"""
    <div class='card'>
        <h3>Situation {srt['id']}:</h3>
        <p style='font-size: 1.25rem; font-style: italic; color: #93c5fd;'>"{srt['situation']}"</p>
    </div>
    """, unsafe_allow_html=True)
    
    reaction = st.text_area("Your Reaction/Action:", placeholder="Type your reaction here...", height=150)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Submit Reaction for Analysis"):
            if not reaction.strip():
                st.warning("Please write a response first.")
            else:
                with st.spinner("Analyzing reaction..."):
                    if st.session_state.api_key:
                        analysis = gemini_analyze_text(reaction, st.session_state.api_key, "SRT", context=srt['situation'])
                    else:
                        analysis = local_analyze_text(reaction)
                    
                    st.session_state.srt_analysis = analysis
                    st.session_state.srt_text = reaction
                    st.rerun()
    with col2:
        if st.button("Skip / Next Situation"):
            st.session_state.current_srt = random.choice(SRT_SITUATIONS)
            if 'srt_analysis' in st.session_state:
                del st.session_state.srt_analysis
            st.rerun()
            
    if 'srt_analysis' in st.session_state:
        render_analysis_results(st.session_state.srt_analysis)
        if st.button("Save & Try Another"):
            save_analysis("SRT", st.session_state.srt_text, st.session_state.srt_analysis, context=srt['situation'])
            st.session_state.current_srt = random.choice(SRT_SITUATIONS)
            del st.session_state.srt_analysis
            st.rerun()

# -----------------
# 3.5 Speech & Mock Interview Mode
# -----------------
elif test_mode == "🎙️ Speech & Mock Interview":
    st.components.v1.html(get_interview_logo(), height=130)
    render_page_navigation("🎙️ Speech & Mock Interview", "mock")


    if not st.session_state.interview_active:
        # Settings Screen
        st.subheader("Setup Your Interview Session")
        
        col1, col2 = st.columns(2)
        with col1:
            profile = st.selectbox(
                "Select Interview Profile",
                ["Personal & PIQ-based", "Situation & OLQ-based", "Current Affairs & General Knowledge"]
            )
            tts_enabled = st.checkbox("Enable voice question reading (AI Audio output)", value=True)
            
        with col2:
            st.info("💡 **Tips for practice:**\n"
                    "- Try to reply in 1 to 2 minutes per question.\n"
                    "- Describe structured experiences using the STAR method (Situation, Task, Action, Result).\n"
                    "- Ensure you are in a quiet room if using voice recording.")
            
        if st.button("Start Mock Interview Session ➔"):
                piq_data = None
                if 'piq_data' in st.session_state and st.session_state.piq_data.get("name"):
                    # Create a copy and make sure DOB is a string
                    piq_data = st.session_state.piq_data.copy()
                    if piq_data.get("dob"):
                        piq_data["dob"] = str(piq_data["dob"])
                st.session_state.interview_questions = generate_interview_questions(profile, st.session_state.api_key, piq_data)
                st.session_state.interview_index = 0
                st.session_state.interview_responses = []
                st.session_state.interview_active = True
                st.session_state.interview_profile = profile
                st.session_state.interview_tts_enabled = tts_enabled
                st.session_state.interview_tts_played = False
                if 'interview_evaluations' in st.session_state:
                    del st.session_state.interview_evaluations
                st.rerun()
    else:
        # Active Mock Interview
        idx = st.session_state.interview_index
        questions = st.session_state.interview_questions
        
        if idx < len(questions):
            current_q = questions[idx]
            st.subheader(f"Question {idx + 1} of {len(questions)}")
            
            # Question Card
            st.markdown(f"""
            <div class='card'>
                <h4 style='color: #3b82f6;'>Interviewing Officer asks:</h4>
                <p style='font-size: 1.3rem; font-weight: bold;'>"{current_q}"</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Text to Speech Audio
            if st.session_state.interview_tts_enabled:
                if not st.session_state.get('interview_tts_played') or st.session_state.get('interview_tts_q_idx') != idx:
                    with st.spinner("Generating speech..."):
                        try:
                            tts = gTTS(text=current_q, lang='en')
                            fp = io.BytesIO()
                            tts.write_to_fp(fp)
                            fp.seek(0)
                            st.session_state.current_audio_bytes = fp.read()
                            st.session_state.interview_tts_played = True
                            st.session_state.interview_tts_q_idx = idx
                        except Exception as e:
                            st.error(f"Could not generate text-to-speech audio: {str(e)}")
                
                if 'current_audio_bytes' in st.session_state:
                    st.audio(st.session_state.current_audio_bytes, format="audio/mp3", autoplay=True)
                    if st.button("🔊 Replay Question"):
                        st.rerun()

            st.markdown("---")
            st.markdown("### 🎙️ Record Your Answer")
            st.write("Click the button below and speak clearly into your microphone. Click stop when finished.")
            
            # Use streamlit-mic-recorder to record WAV bytes from browser
            audio_data = mic_recorder(
                start_prompt="🎙️ Start Recording",
                stop_prompt="🛑 Stop Recording",
                just_once=True,
                key=f"interview_mic_{idx}"
            )
            
            # Check if audio was recorded
            if audio_data and 'bytes' in audio_data:
                # We have new audio recorded! Let's transcribe it.
                if st.session_state.get(f"last_recorded_id_{idx}") != audio_data.get("id"):
                    st.session_state[f"last_recorded_id_{idx}"] = audio_data.get("id")
                    with st.spinner("Transcribing your speech to text..."):
                        try:
                            r = sr.Recognizer()
                            audio_file = io.BytesIO(audio_data["bytes"])
                            with sr.AudioFile(audio_file) as source:
                                audio = r.record(source)
                            transcript = r.recognize_google(audio)
                            st.session_state[f"temp_response_{idx}"] = transcript
                        except sr.UnknownValueError:
                            st.warning("Could not understand the audio. Please check your mic or type your answer manually.")
                        except sr.RequestError as e:
                            st.error(f"Speech recognition service error: {str(e)}")
                            
            # Answer input & modification
            saved_transcript = st.session_state.get(f"temp_response_{idx}", "")
            user_answer = st.text_area(
                "Edit / Review your transcribed response before submitting:",
                value=saved_transcript,
                placeholder="Your spoken response will appear here. You can also type/edit it manually...",
                height=150,
                key=f"answer_area_{idx}"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Submit Answer for Evaluation ➔"):
                    if not user_answer.strip():
                        st.warning("Please record or write an answer first.")
                    else:
                        with st.spinner("Analyzing answer and packaging evaluation..."):
                            analysis = evaluate_interview_answer(current_q, user_answer, st.session_state.api_key)
                            
                            # Append to session responses
                            st.session_state.interview_responses.append({
                                "question": current_q,
                                "answer": user_answer,
                                "analysis": analysis
                            })
                            # Clear temp values for current question
                            if f"temp_response_{idx}" in st.session_state:
                                del st.session_state[f"temp_response_{idx}"]
                            if 'current_audio_bytes' in st.session_state:
                                del st.session_state.current_audio_bytes
                                
                            st.session_state.interview_index += 1
                            st.session_state.interview_tts_played = False
                            st.success("Answer submitted successfully!")
                            time.sleep(1.5)
                            st.rerun()
            with col2:
                if st.button("Skip / Next Question"):
                    st.session_state.interview_responses.append({
                        "question": current_q,
                        "answer": "[Skipped]",
                        "analysis": {
                            "sentiment": 0.0,
                            "confidence_score": 0.0,
                            "olqs_demonstrated": {},
                            "overall_evaluation": "Question was skipped by candidate.",
                            "actionable_feedback": ["Try not to skip questions during interview practice."]
                        }
                    })
                    if f"temp_response_{idx}" in st.session_state:
                        del st.session_state[f"temp_response_{idx}"]
                    if 'current_audio_bytes' in st.session_state:
                        del st.session_state.current_audio_bytes
                    st.session_state.interview_index += 1
                    st.session_state.interview_tts_played = False
                    st.rerun()
        else:
            # Interview Finished!
            st.success("🎉 Mock Interview Session Completed!")
            st.session_state.interview_active = False
            
            # Show summary
            st.markdown("### 📋 Interview Summary & Feedbacks")
            
            total_sentiment = 0.0
            total_confidence = 0.0
            all_olqs = {}
            
            for i, r in enumerate(st.session_state.interview_responses):
                st.markdown(f"**Q{i+1}:** *{r['question']}*")
                st.markdown(f"**Your Answer:** *{r['answer']}*")
                
                eval_res = r['analysis']
                if "error" in eval_res and not eval_res.get("local_fallback"):
                    st.error(eval_res["error"])
                else:
                    total_sentiment += eval_res.get("sentiment", 0.0)
                    total_confidence += eval_res.get("confidence_score", 0.5)
                    
                    # Accumulate OLQs
                    for olq, desc in eval_res.get("olqs_demonstrated", {}).items():
                        all_olqs[olq] = desc
                    
                    with st.expander(f"View Q{i+1} Detailed Psych Assessment"):
                        render_analysis_results(eval_res)
                st.markdown("---")
            
            # Overall Session Analysis
            st.subheader("🏁 Overall Interview Scorecard")
            avg_sentiment = total_sentiment / len(st.session_state.interview_responses)
            avg_confidence = total_confidence / len(st.session_state.interview_responses)
            
            # Render scorecard
            c1, c2 = st.columns(2)
            c1.metric("Average Attitude Index", f"{avg_sentiment:+.2f}")
            c2.metric("Average Confidence Level", f"{avg_confidence * 100:.0f}%")
            
            # Save the entire session
            if st.button("Save Interview and Exit"):
                # Bundle the combined text for dashboard compatibility
                combined_interview_text = "\n\n".join([f"Q: {r['question']}\nA: {r['answer']}" for r in st.session_state.interview_responses])
                
                # Bundle overall analysis for dashboard compatibility
                overall_analysis = {
                    "sentiment": avg_sentiment,
                    "confidence_score": avg_confidence,
                    "olqs_demonstrated": all_olqs,
                    "overall_evaluation": f"Completed a mock interview on {st.session_state.interview_profile}. Demonstrated confidence level of {avg_confidence*100:.0f}%.",
                    "actionable_feedback": ["Review individual question feedback points for communication improvements."]
                }
                
                save_analysis(f"Mock Interview ({st.session_state.interview_profile})", combined_interview_text, overall_analysis)
                
                # Clean up session variables
                del st.session_state.interview_questions
                del st.session_state.interview_responses
                st.rerun()

# -----------------
# 3.8 PIQ Form Digitizer
# -----------------
elif test_mode == "📋 PIQ Form Digitizer":
    st.components.v1.html(get_piq_logo(), height=130)
    render_page_navigation("📋 PIQ Form Digitizer", "piq")


    import pandas as pd
    
    # Store local copy for session edits
    p = st.session_state.piq_data

    # Use tabs for a clean structured workflow
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "1. Board & Identity", 
        "2. Demographics & Family", 
        "3. Academic Record", 
        "4. Stats & NCC", 
        "5. Sports & Hobbies", 
        "6. Service Attempts", 
        "7. Export & AI Assessment"
    ])

    with tab1:
        st.subheader("1. Selection Board & Candidate Identity")
        
        col1, col2 = st.columns(2)
        with col1:
            p["board_no"] = st.text_input("Selection Board Number / Name", value=p["board_no"], placeholder="e.g. 24 SSB Bangalore")
            p["batch_no"] = st.text_input("Batch Number", value=p["batch_no"], placeholder="e.g. NCC(SPL)-54")
            p["name"] = st.text_input("Candidate's Full Name (in CAPITALS)", value=p["name"], placeholder="e.g. AMIT KUMAR SINGH")
            
        with col2:
            p["board_place"] = st.text_input("Selection Board Place", value=p["board_place"], placeholder="e.g. Bangalore")
            p["chest_no"] = st.text_input("Chest Number", value=p["chest_no"], placeholder="e.g. 14")
            p["upsc_roll"] = st.text_input("UPSC Roll Number", value=p["upsc_roll"], placeholder="e.g. 0846513")
            
        p["father_name"] = st.text_input("Father's Name", value=p["father_name"], placeholder="e.g. Late Shri R. K. Singh")

    with tab2:
        st.subheader("2. Demographics, Addresses & Family particulars")
        
        col1, col2 = st.columns(2)
        with col1:
            p["max_residence"] = st.text_input("Place of Maximum Residence", value=p["max_residence"], placeholder="e.g. Ranchi, Jharkhand")
            p["present_address"] = st.text_area("Present Address", value=p["present_address"], placeholder="Enter present correspondence address...", height=100)
            p["present_pop"] = st.text_input("Approx. Population of Present City/Town/Village", value=p["present_pop"], placeholder="e.g. 1.2 Million")
            p["is_dist_hq"] = st.selectbox("Whether District Headquarter or not?", ["Yes", "No"], index=0 if p["is_dist_hq"] == "Yes" else 1)
            
        with col2:
            p["state_district"] = st.text_input("State & District", value=p["state_district"], placeholder="e.g. Jharkhand, Ranchi")
            p["permanent_address"] = st.text_area("Permanent Address", value=p["permanent_address"], placeholder="Enter permanent address...", height=100)
            p["permanent_pop"] = st.text_input("Approx. Population of Permanent City/Town/Village", value=p["permanent_pop"], placeholder="e.g. 50,000")
            
        col3, col4 = st.columns(2)
        with col3:
            p["religion"] = st.text_input("Religion", value=p["religion"], placeholder="e.g. Hinduism")
            p["mother_tongue"] = st.text_input("Mother Tongue", value=p["mother_tongue"], placeholder="e.g. Hindi")
            p["dob"] = st.date_input("Date of Birth", value=p["dob"] if p["dob"] else None)
            
        with col4:
            p["category"] = st.selectbox("Whether SC/ST/OBC", ["SC", "ST", "OBC", "General"], index=["SC", "ST", "OBC", "General"].index(p["category"]))
            p["marital_status"] = st.selectbox("Marital Status", ["Single", "Married", "Widower"], index=["Single", "Married", "Widower"].index(p["marital_status"]))
            p["parents_alive"] = st.selectbox("Are Parents alive?", ["Yes", "No"], index=0 if p["parents_alive"] == "Yes" else 1)
            if p["parents_alive"] == "No":
                p["age_at_death"] = st.text_input("Your age at the time of father's / mother's death", value=p["age_at_death"])

        st.markdown("#### Parents / Guardian Occupation & Income Particulars")
        st.write("Edit the table below to reflect your parents' education and income details:")
        
        # Data Editor for Parents particulars
        df_parents = pd.DataFrame(p["parents_particulars"])
        edited_parents = st.data_editor(df_parents, num_rows="fixed", hide_index=True, key="parents_editor")
        p["parents_particulars"] = edited_parents.to_dict('records')

    with tab3:
        st.subheader("3. Educational Record & Sibling Details")
        st.write("Edit your qualifications table (Matriculation commencing onwards):")
        
        # Data Editor for Educational records
        df_edu = pd.DataFrame(p["education_record"])
        edited_edu = st.data_editor(df_edu, num_rows="dynamic", hide_index=True, key="edu_editor")
        p["education_record"] = edited_edu.to_dict('records')

        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            p["brothers_sisters_count"] = st.text_input("No. of brothers and sisters", value=p["brothers_sisters_count"], placeholder="e.g. 1 brother, 1 sister")
            p["sibling_ranking"] = st.text_input("Your ranking amongst brothers/sisters", value=p["sibling_ranking"], placeholder="e.g. 2nd (eldest is brother)")
        with col2:
            p["sibling_info"] = st.text_area("Education and Occupation of brothers/sisters", value=p["sibling_info"], placeholder="e.g. Brother is doing B.Tech; Sister is in School...")

    with tab4:
        st.subheader("4. Physical Stats, Occupation & NCC details")
        
        col1, col2 = st.columns(2)
        with col1:
            p["age_years"] = st.text_input("Age (Years)", value=p["age_years"], placeholder="e.g. 21")
            p["height_m"] = st.text_input("Height (in Meters)", value=p["height_m"], placeholder="e.g. 1.75")
            p["present_occupation_income"] = st.text_area("Present Occupation & Personal Monthly Income (if any)", value=p["present_occupation_income"], placeholder="e.g. Student (No income)")
            
        with col2:
            p["age_months"] = st.text_input("Age (Months)", value=p["age_months"], placeholder="e.g. 8")
            p["weight_kg"] = st.text_input("Weight (in Kgs.)", value=p["weight_kg"], placeholder="e.g. 68")
            p["ncc_training"] = st.selectbox("NCC Training availed?", ["Yes", "No"], index=0 if p["ncc_training"] == "Yes" else 1)
            
        if p["ncc_training"] == "Yes":
            st.markdown("#### NCC Details")
            df_ncc = pd.DataFrame(p["ncc_details"])
            edited_ncc = st.data_editor(df_ncc, num_rows="dynamic", hide_index=True, key="ncc_editor")
            p["ncc_details"] = edited_ncc.to_dict('records')

    with tab5:
        st.subheader("5. Sports, Hobbies, Co-Curriculars & Leadership Roles")
        
        st.markdown("#### (a) Games and Sports Participation")
        df_sports = pd.DataFrame(p["sports_participation"])
        edited_sports = st.data_editor(df_sports, num_rows="dynamic", hide_index=True, key="sports_editor")
        p["sports_participation"] = edited_sports.to_dict('records')
        
        col1, col2 = st.columns(2)
        with col1:
            p["hobbies"] = st.text_area("(b) Hobbies / Interests", value=p["hobbies"], placeholder="e.g. Reading historical biographies, trekking, sketching...")
        with col2:
            p["responsibilities"] = st.text_area("(d) Position of Responsibility / Offices held in NCC / Scouting / Sports Team / Extra-Curricular Group", value=p["responsibilities"], placeholder="e.g. School Captain, Captain of football team, NCC Platoon Commander...")
            
        st.markdown("#### (c) Extra-Curricular Activities")
        df_extra = pd.DataFrame(p["extracurricular"])
        edited_extra = st.data_editor(df_extra, num_rows="dynamic", hide_index=True, key="extra_editor")
        p["extracurricular"] = edited_extra.to_dict('records')

    with tab6:
        st.subheader("6. Choice of Commission & Previous SSB Attempts")
        
        col1, col2 = st.columns(2)
        with col1:
            p["commission_type"] = st.text_input("Type of Commission", value=p["commission_type"], placeholder="e.g. Permanent Commission (PC) / Short Service Commission (SSC)")
            p["previous_attempts_count"] = st.text_input("Number of chances availed in all three services", value=p["previous_attempts_count"])
            
        with col2:
            p["choice_of_service"] = st.selectbox("Choice of Service", ["Army", "Navy", "Air Force", "Common Entry (CDSE/AFCAT)"], index=["Army", "Navy", "Air Force", "Common Entry (CDSE/AFCAT)"].index(p["choice_of_service"]) if p["choice_of_service"] in ["Army", "Navy", "Air Force", "Common Entry (CDSE/AFCAT)"] else 0)
            
        try:
            prev_count = int(p["previous_attempts_count"])
        except ValueError:
            prev_count = 0
            
        if prev_count > 0:
            st.markdown("#### Details of Previous SSB Interviews")
            df_prev = pd.DataFrame(p["previous_attempts_details"])
            edited_prev = st.data_editor(df_prev, num_rows="dynamic", hide_index=True, key="prev_editor")
            p["previous_attempts_details"] = edited_prev.to_dict('records')

    with tab7:
        st.subheader("📋 Export & AI Profile Assessment")
        
        # Save updated data back to session state
        st.session_state.piq_data = p
        
        # Generate clean Markdown string
        dob_str = str(p["dob"]) if p["dob"] else "Not entered"
        
        piq_markdown = f"""
# PERSONAL INFORMATION QUESTIONNAIRE (PIQ) SUMMARY

### 1. Selection Board & Identity Details
- **Board Name / Place:** {p['board_no']} at {p['board_place']}
- **Batch No:** {p['batch_no']} | **Chest No:** {p['chest_no']}
- **UPSC Roll No:** {p['upsc_roll']}
- **Candidate Name:** {p['name']}
- **Father's Name:** {p['father_name']}

### 2. Demographic & Family particulars
- **Place of Max Residence:** {p['max_residence']}
- **District HQ:** {p['is_dist_hq']}
- **Present Address:** {p['present_address']} (Approx. Pop: {p['present_pop']})
- **Permanent Address:** {p['permanent_address']} (Approx. Pop: {p['permanent_pop']})
- **State & District:** {p['state_district']}
- **Religion:** {p['religion']} | **Mother Tongue:** {p['mother_tongue']}
- **Category:** {p['category']} | **Date of Birth:** {dob_str} | **Marital Status:** {p['marital_status']}
- **Parents Alive:** {p['parents_alive']} (Age at death: {p['age_at_death'] if p['parents_alive'] == 'No' else 'N/A'})

#### Parents Particulars:
"""
        for prnt in p['parents_particulars']:
            piq_markdown += f"- **{prnt.get('Particulars')}:** Education: {prnt.get('Education')} | Occupation: {prnt.get('Occupation')} | Income: {prnt.get('Income per Month')}/mo\n"
            
        piq_markdown += "\n### 3. Academic Record\n"
        for edu in p['education_record']:
            piq_markdown += f"- **{edu.get('Qualification', 'N/A')}:** Inst: {edu.get('Institution')} | Year: {edu.get('Year')} | Div/%: {edu.get('Division & %')} | Med: {edu.get('Medium')} | Boarder: {edu.get('Boarder/Day Scholar')} | Achievements: {edu.get('Outstanding Achievement')}\n"
            
        piq_markdown += f"""
- **Brothers/Sisters Count:** {p['brothers_sisters_count']}
- **Ranking among Siblings:** {p['sibling_ranking']}
- **Sibling Info:** {p['sibling_info']}

### 4. Stats, Occupation & NCC
- **Age:** {p['age_years']} Y, {p['age_months']} M
- **Height:** {p['height_m']} meters | **Weight:** {p['weight_kg']} kg
- **Occupation & Income:** {p['present_occupation_income']}
- **NCC Training:** {p['ncc_training']}
"""
        if p['ncc_training'] == 'Yes':
            for ncc in p['ncc_details']:
                piq_markdown += f"  - Wing: {ncc.get('Wing')} | Div: {ncc.get('Division')} | Cert: {ncc.get('Certificate Obtained')} | Training: {ncc.get('Total Training')}\n"

        piq_markdown += "\n### 5. Sports, Hobbies, Co-Curriculars & Leadership Roles\n"
        piq_markdown += f"- **Hobbies & Interests:** {p['hobbies']}\n"
        piq_markdown += f"- **Leadership/Positions of Responsibility:** {p['responsibilities']}\n"
        
        piq_markdown += "\n#### Games & Sports:\n"
        for spt in p['sports_participation']:
            piq_markdown += f"- **{spt.get('Games / Sports')}:** Duration: {spt.get('Duration of Participation')} | Level: {spt.get('Represented School/College')} | Achvt: {spt.get('Outstanding Achievement')}\n"
            
        piq_markdown += "\n#### Extra-Curricular Activities:\n"
        for ex in p['extracurricular']:
            piq_markdown += f"- **{ex.get('Group Activity')}:** Duration: {ex.get('Duration')} | Achvt: {ex.get('Outstanding Achievement')}\n"
            
        piq_markdown += f"""
### 6. Commission & Attempts Details
- **Type of Commission:** {p['commission_type']} | **Choice of Service:** {p['choice_of_service']}
- **SSB Chances Availed:** {p['previous_attempts_count']}
"""
        if prev_count > 0:
            piq_markdown += "\n#### Previous SSB Attempts:\n"
            for att in p['previous_attempts_details']:
                piq_markdown += f"- **Entry:** {att.get('Type of Entry')} | Board: {att.get('Place & SSB No.')} | Date: {att.get('Date')} | Batch/Chest: {att.get('Batch & Chest No.')} | Result: {att.get('Result')}\n"

        st.info("ℹ️ Your PIQ details are automatically saved in this browser session. You can copy the raw summary or run the AI Psychological assessment below.")
        
        with st.expander("📄 View Fully Formatted Summary"):
            st.markdown(piq_markdown)
            st.download_button("💾 Download PIQ Summary (Markdown)", data=piq_markdown, file_name="SSB_PIQ_Summary.md")

        # Run AI Assessment button
        st.markdown("---")
        st.markdown("### 🤖 AI Psychological PIQ Assessor")
        st.write("Generate a mock assessment of your PIQ to identify strengths, weaknesses, and probable questions you will face in the actual interview.")
        
        if st.button("Generate AI Assessment Profile"):
            with st.spinner("Analyzing your PIQ details..."):
                # Clean DOB date to string for JSON serialization
                piq_to_send = p.copy()
                if piq_to_send.get("dob"):
                    piq_to_send["dob"] = str(piq_to_send["dob"])
                assessment = analyze_piq_data(piq_to_send, st.session_state.api_key)
                
                # Show results
                st.subheader("🎖️ Psychological Profile Assessment")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("#### 🌟 Candidate Strong Points")
                    for strong in assessment.get("strong_points", []):
                        st.success(strong)
                        
                with col2:
                    st.markdown("#### ⚠️ Potential Vulnerabilities / Focus Areas")
                    for weak in assessment.get("potential_weaknesses", []):
                        st.warning(weak)
                        
                st.markdown("#### 💡 Actionable Improvement Strategies")
                for strategy in assessment.get("recommended_focus_areas", []):
                    st.info(strategy)
                    
                st.markdown("#### 🎯 Probable Interview Officer Questions (Based on your PIQ)")
                for q_num, question in enumerate(assessment.get("probable_questions", [])):
                    st.markdown(f"**{q_num + 1}.** {question}")

# -----------------
# 3.9 OIR Practice Exam
# -----------------
elif test_mode == "📐 OIR Practice Exam":
    st.components.v1.html(get_oir_logo(), height=130)
    render_page_navigation("📐 OIR Practice Exam", "oir")


    # 1. CONFIGURE STATE
    if st.session_state.oir_state == "configure":
        st.subheader("⚙️ Configure your Practice Session")
        
        session_type = st.radio(
            "Select Session Length & Type",
            ["Quick Practice (6 Verbal, 4 Non-Verbal questions | 3 mins each booklet)", 
             "Standard Session (12 Verbal, 6 Non-Verbal questions | 6 mins each booklet)", 
             "Full Exam Simulation (40 Verbal, 40 Non-Verbal questions | 15 mins each booklet)"]
        )
        
        st.markdown("""
        ### OIR Exam Guidelines:
        - **Speed is everything**: You have less than 30 seconds per question.
        - **No Negative Marking**: Guessing quickly is better than leaving questions blank.
        - **Structured Gap**: A 2-minute transition break will occur between Booklet 1 and Booklet 2.
        - **Digital OMR**: Choose your options using the interface. Your progress is automatically recorded.
        """)
        
        if st.button("Start OIR Practice Session ➔", use_container_width=True):
            # Parse limits and times
            if "Quick Practice" in session_type:
                verbal_count = 6
                non_verbal_count = 4
                dur_verbal = 3 * 60
                dur_non_verbal = 3 * 60
            elif "Standard Session" in session_type:
                verbal_count = 12
                non_verbal_count = 6
                dur_verbal = 6 * 60
                dur_non_verbal = 6 * 60
            else:
                verbal_count = 40
                non_verbal_count = 40
                dur_verbal = 15 * 60
                dur_non_verbal = 15 * 60
                
            # Random selection (with replacement if we request 40)
            if verbal_count <= len(OIR_VERBAL_QUESTIONS):
                st.session_state.oir_verbal_questions = random.sample(OIR_VERBAL_QUESTIONS, verbal_count)
            else:
                st.session_state.oir_verbal_questions = random.choices(OIR_VERBAL_QUESTIONS, k=verbal_count)
                
            if non_verbal_count <= len(OIR_NON_VERBAL_QUESTIONS):
                st.session_state.oir_non_verbal_questions = random.sample(OIR_NON_VERBAL_QUESTIONS, non_verbal_count)
            else:
                st.session_state.oir_non_verbal_questions = random.choices(OIR_NON_VERBAL_QUESTIONS, k=non_verbal_count)
                
            st.session_state.oir_verbal_duration = dur_verbal
            st.session_state.oir_non_verbal_duration = dur_non_verbal
            
            st.session_state.oir_verbal_answers = {}
            st.session_state.oir_non_verbal_answers = {}
            st.session_state.oir_verbal_index = 0
            st.session_state.oir_non_verbal_index = 0
            st.session_state.oir_session_type = session_type
            
            st.session_state.oir_verbal_start_time = time.time()
            st.session_state.oir_state = "verbal"
            st.rerun()

    # 2. VERBAL BOOKLET SPRINT
    elif st.session_state.oir_state == "verbal":
        st.subheader("📝 OIR Booklet 1: Verbal Reasoning Test")
        
        elapsed = time.time() - st.session_state.oir_verbal_start_time
        remaining = int(st.session_state.oir_verbal_duration - elapsed)
        
        if remaining <= 0:
            st.warning("⏰ Time is up for Booklet 1! Automatically saving and transferring to transition break.")
            time.sleep(1.5)
            st.session_state.oir_break_start_time = time.time()
            st.session_state.oir_state = "break"
            st.rerun()
            
        mins, secs = divmod(remaining, 60)
        
        # Header columns
        col_t, col_s = st.columns([2, 1])
        with col_t:
            st.markdown(f"⏱️ **Time Remaining:** `<span style='color:#ef4444; font-size:1.3rem; font-weight:bold;'>{mins:02d}:{secs:02d}</span>`", unsafe_allow_html=True)
        with col_s:
            if st.button("Submit Booklet 1 ➔", type="primary", use_container_width=True):
                st.session_state.oir_break_start_time = time.time()
                st.session_state.oir_state = "break"
                st.rerun()
                
        # Main content
        idx = st.session_state.oir_verbal_index
        q = st.session_state.oir_verbal_questions[idx]
        
        st.markdown(f"### Question {idx + 1} of {len(st.session_state.oir_verbal_questions)}")
        st.info(f"**Category:** {q['type']}")
        
        st.markdown(f"<div class='card'><p style='font-size: 1.2rem; color: #f8fafc;'>{q['question']}</p></div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Selected option persistence
        current_ans = st.session_state.oir_verbal_answers.get(q['id'], None)
        selected_option = st.radio(
            "Choose the correct option:",
            q['options'],
            index=q['options'].index(current_ans) if current_ans in q['options'] else None,
            key=f"verbal_opt_{idx}"
        )
        
        # Save selection
        if selected_option:
            st.session_state.oir_verbal_answers[q['id']] = selected_option
            
        # Navigation
        st.markdown("---")
        col_prev, col_nav, col_next = st.columns([1, 2, 1])
        with col_prev:
            if st.button("◀ Previous", disabled=(idx == 0), use_container_width=True):
                st.session_state.oir_verbal_index -= 1
                st.rerun()
        with col_nav:
            # Short auto-refresh timer button
            if st.button("🔄 Sync/Refresh Timer", use_container_width=True):
                st.rerun()
        with col_next:
            if idx < len(st.session_state.oir_verbal_questions) - 1:
                if st.button("Next ▶", use_container_width=True):
                    st.session_state.oir_verbal_index += 1
                    st.rerun()
            else:
                st.button("Next ▶", disabled=True, use_container_width=True)

        # Question Navigator Grid
        st.markdown("#### Question Grid Navigator")
        grid_cols = st.columns(min(10, len(st.session_state.oir_verbal_questions)))
        for grid_idx, grid_col in enumerate(grid_cols):
            grid_q = st.session_state.oir_verbal_questions[grid_idx]
            is_active = (grid_idx == idx)
            is_answered = (grid_q['id'] in st.session_state.oir_verbal_answers)
            
            button_label = f"{grid_idx + 1}"
            
            if is_active:
                btn_type = "primary"
            else:
                btn_type = "secondary"
                
            if grid_col.button(f"{'📍' if is_active else ''} {button_label}", key=f"grid_v_{grid_idx}", type=btn_type, use_container_width=True):
                st.session_state.oir_verbal_index = grid_idx
                st.rerun()

    # 3. BREAK TRANSITION STATE
    elif st.session_state.oir_state == "break":
        st.subheader("⏸️ Booklet Exchange & Transition Break")
        st.write("In the actual SSB, invigilators collect the Verbal booklet and distribute the Non-Verbal booklet. Use this 2-minute break to clear your mind.")
        
        elapsed = time.time() - st.session_state.oir_break_start_time
        remaining = int(120 - elapsed)
        
        if remaining <= 0:
            st.info("Break finished! Starting Booklet 2.")
            time.sleep(1.5)
            st.session_state.oir_non_verbal_start_time = time.time()
            st.session_state.oir_state = "non_verbal"
            st.rerun()
            
        mins, secs = divmod(remaining, 60)
        st.markdown(f"⏱️ **Break Time Left:** `<span style='color:#3b82f6; font-size:1.5rem; font-weight:bold;'>{mins:02d}:{secs:02d}</span>`", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Skip Break & Start Booklet 2 ➔", type="primary", use_container_width=True):
                st.session_state.oir_non_verbal_start_time = time.time()
                st.session_state.oir_state = "non_verbal"
                st.rerun()
        with col2:
            if st.button("🔄 Sync Timer", use_container_width=True):
                st.rerun()

    # 4. NON-VERBAL BOOKLET SPRINT
    elif st.session_state.oir_state == "non_verbal":
        st.subheader("🖼️ OIR Booklet 2: Non-Verbal Reasoning Test")
        
        elapsed = time.time() - st.session_state.oir_non_verbal_start_time
        remaining = int(st.session_state.oir_non_verbal_duration - elapsed)
        
        if remaining <= 0:
            st.warning("⏰ Time is up for Booklet 2! Automatically submitting exam.")
            time.sleep(1.5)
            st.session_state.oir_state = "scorecard"
            st.rerun()
            
        mins, secs = divmod(remaining, 60)
        
        # Header columns
        col_t, col_s = st.columns([2, 1])
        with col_t:
            st.markdown(f"⏱️ **Time Remaining:** `<span style='color:#ef4444; font-size:1.3rem; font-weight:bold;'>{mins:02d}:{secs:02d}</span>`", unsafe_allow_html=True)
        with col_s:
            if st.button("Finish Exam & Submit ➔", type="primary", use_container_width=True):
                st.session_state.oir_state = "scorecard"
                st.rerun()
                
        # Main content
        idx = st.session_state.oir_non_verbal_index
        q = st.session_state.oir_non_verbal_questions[idx]
        
        st.markdown(f"### Question {idx + 1} of {len(st.session_state.oir_non_verbal_questions)}")
        st.info(f"**Category:** {q['type']}")
        
        # Display SVG Figure
        st.components.v1.html(q['svg'], height=220)
        
        st.markdown(f"<div class='card'><p style='font-size: 1.1rem; color: #f8fafc;'>{q['question']}</p></div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Selected option persistence
        current_ans = st.session_state.oir_non_verbal_answers.get(q['id'], None)
        selected_option = st.radio(
            "Choose the correct option:",
            q['options'],
            index=q['options'].index(current_ans) if current_ans in q['options'] else None,
            key=f"non_verbal_opt_{idx}"
        )
        
        # Save selection
        if selected_option:
            st.session_state.oir_non_verbal_answers[q['id']] = selected_option
            
        # Navigation
        st.markdown("---")
        col_prev, col_nav, col_next = st.columns([1, 2, 1])
        with col_prev:
            if st.button("◀ Previous", disabled=(idx == 0), use_container_width=True):
                st.session_state.oir_non_verbal_index -= 1
                st.rerun()
        with col_nav:
            if st.button("🔄 Sync/Refresh Timer", use_container_width=True):
                st.rerun()
        with col_next:
            if idx < len(st.session_state.oir_non_verbal_questions) - 1:
                if st.button("Next ▶", use_container_width=True):
                    st.session_state.oir_non_verbal_index += 1
                    st.rerun()
            else:
                st.button("Next ▶", disabled=True, use_container_width=True)

        # Question Navigator Grid
        st.markdown("#### Question Grid Navigator")
        grid_cols = st.columns(min(10, len(st.session_state.oir_non_verbal_questions)))
        for grid_idx, grid_col in enumerate(grid_cols):
            grid_q = st.session_state.oir_non_verbal_questions[grid_idx]
            is_active = (grid_idx == idx)
            is_answered = (grid_q['id'] in st.session_state.oir_non_verbal_answers)
            
            button_label = f"{grid_idx + 1}"
            
            if is_active:
                btn_type = "primary"
            else:
                btn_type = "secondary"
                
            if grid_col.button(f"{'📍' if is_active else ''} {button_label}", key=f"grid_nv_{grid_idx}", type=btn_type, use_container_width=True):
                st.session_state.oir_non_verbal_index = grid_idx
                st.rerun()

    # 5. SCORECARD & EVALUATION STATE
    elif st.session_state.oir_state == "scorecard":
        st.subheader("🏆 OIR Performance Scorecard")
        
        # Calculate scores
        correct_v = 0
        total_v = len(st.session_state.oir_verbal_questions)
        for q in st.session_state.oir_verbal_questions:
            ans = st.session_state.oir_verbal_answers.get(q['id'], None)
            if ans == q['answer']:
                correct_v += 1
                
        correct_nv = 0
        total_nv = len(st.session_state.oir_non_verbal_questions)
        for q in st.session_state.oir_non_verbal_questions:
            ans = st.session_state.oir_non_verbal_answers.get(q['id'], None)
            if ans == q['answer']:
                correct_nv += 1
                
        correct_total = correct_v + correct_nv
        total_questions = total_v + total_nv
        accuracy = (correct_total / total_questions) * 100 if total_questions > 0 else 0.0
        
        # Determine Rating
        if accuracy >= 90.0:
            oir_rating = "OIR Rating 1 (Outstanding)"
            rating_color = "#10b981"
        elif accuracy >= 80.0:
            oir_rating = "OIR Rating 2 (Very Good)"
            rating_color = "#3b82f6"
        elif accuracy >= 70.0:
            oir_rating = "OIR Rating 3 (Good)"
            rating_color = "#f59e0b"
        elif accuracy >= 60.0:
            oir_rating = "OIR Rating 4 (Average)"
            rating_color = "#ef4444"
        else:
            oir_rating = "OIR Rating 5 (Below Average)"
            rating_color = "#6b7280"
            
        # Display rating card
        st.markdown(f"""
        <div style='background-color:#1e293b; border-left: 6px solid {rating_color}; padding: 20px; border-radius: 8px; margin-bottom: 20px;'>
            <h2 style='margin:0; color:#ffffff;'>Overall Rating: <span style='color:{rating_color};'>{oir_rating}</span></h2>
            <p style='font-size:1.1rem; color:#94a3b8; margin: 8px 0 0 0;'>You solved <b>{correct_total}</b> out of <b>{total_questions}</b> questions correctly with an accuracy of <b>{accuracy:.1f}%</b>.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        col1.metric("Verbal Score (Booklet 1)", f"{correct_v} / {total_v}", f"{correct_v/total_v*100:.0f}% Accuracy")
        col2.metric("Non-Verbal Score (Booklet 2)", f"{correct_nv} / {total_nv}", f"{correct_nv/total_nv*100:.0f}% Accuracy")
        
        # Save to Dashboard History once
        history_key = f"oir_saved_{st.session_state.oir_verbal_start_time}"
        if history_key not in st.session_state:
            st.session_state[history_key] = True
            
            # Save to global history list
            oir_history_entry = {
                "test": f"OIR Exam ({st.session_state.oir_session_type.split('(')[0].strip()})",
                "response": f"Accuracy: {accuracy:.1f}%. Score: {correct_total}/{total_questions}",
                "analysis": {
                    "sentiment": 0.8 if accuracy >= 80 else (0.5 if accuracy >= 60 else 0.2),
                    "confidence_score": accuracy / 100.0,
                    "olqs_demonstrated": {
                        "Reasoning Ability": "High OIR accuracy shows strong logical capacity.",
                        "Effective Intelligence": "Fast and accurate abstract figure categorization under strict time constraints."
                    } if accuracy >= 70 else {
                        "Reasoning Ability": "Needs further practice to build structured speed logic."
                    },
                    "overall_evaluation": f"Completed OIR practice session. Scored {correct_total}/{total_questions} with {accuracy:.1f}% accuracy, achieving {oir_rating}.",
                    "actionable_feedback": ["Work on Non-Verbal patterns to optimize spatial rotation reasoning.", "Build speed by avoiding spending more than 20 seconds on a single question."]
                }
            }
            # Append to history
            st.session_state.history.append(oir_history_entry)
            
        st.markdown("---")
        
        # Show Detailed Review
        with st.expander("🔍 Review Detailed Solutions & Explanations"):
            st.markdown("### 📝 Booklet 1: Verbal Solutions")
            for idx, q in enumerate(st.session_state.oir_verbal_questions):
                user_ans = st.session_state.oir_verbal_answers.get(q['id'], "No Answer")
                is_correct = (user_ans == q['answer'])
                
                status_symbol = "✅" if is_correct else "❌"
                st.markdown(f"**Q{idx+1}. {q['question']}** ({q['type']})")
                st.write(f"- Your Answer: `{user_ans}` {status_symbol}")
                st.write(f"- Correct Answer: `{q['answer']}`")
                st.info(f"💡 **Explanation:** {q['explanation']}")
                st.markdown("---")
                
            st.markdown("### 🖼️ Booklet 2: Non-Verbal Solutions")
            for idx, q in enumerate(st.session_state.oir_non_verbal_questions):
                user_ans = st.session_state.oir_non_verbal_answers.get(q['id'], "No Answer")
                is_correct = (user_ans == q['answer'])
                
                status_symbol = "✅" if is_correct else "❌"
                st.markdown(f"**Q{idx+1}. {q['question']}** ({q['type']})")
                st.components.v1.html(q['svg'], height=200)
                st.write(f"- Your Answer: `{user_ans}` {status_symbol}")
                st.write(f"- Correct Answer: `{q['answer']}`")
                st.info(f"💡 **Explanation:** {q['explanation']}")
                st.markdown("---")
                
        if st.button("Retake OIR Practice Session ↺", use_container_width=True):
            st.session_state.oir_state = "configure"
            st.rerun()

# -----------------
# 3.95 GTO Lecturette
# -----------------
elif test_mode == "🗣️ GTO Lecturette":
    st.components.v1.html(get_lecturette_logo(), height=130)
    render_page_navigation("🗣️ GTO Lecturette", "gto")


    # Generate pool of topics automatically if empty
    if not st.session_state.lecturette_topics_pool:
        st.session_state.lecturette_topics_pool = [
            random.choice(LECTURETTE_TOPICS["High / National Affairs"]),
            random.choice(LECTURETTE_TOPICS["Medium / International Relations"]),
            random.choice(LECTURETTE_TOPICS["Low / Technology & Innovation"]),
            random.choice(LECTURETTE_TOPICS["General / Object-based"])
        ]

    # 1. CONFIGURE STATE
    if st.session_state.lecturette_state == "configure":
        st.subheader("📋 Select your Chit Topic")
        st.write("In a real SSB GTO, you draw a chit containing 4 topics. You must choose one instantly.")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div style='background-color:#1e293b; padding:15px; border-radius:8px; border-left:4px solid #ef4444; margin-bottom:15px; min-height:140px;'>
                <span style='color:#ef4444; font-weight:bold; font-size:0.9rem;'>TOPIC 1: HIGH / NATIONAL</span>
                <p style='color:#ffffff; font-size:1.0rem; margin-top:8px;'>{st.session_state.lecturette_topics_pool[0]}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style='background-color:#1e293b; padding:15px; border-radius:8px; border-left:4px solid #3b82f6; margin-bottom:15px; min-height:140px;'>
                <span style='color:#3b82f6; font-weight:bold; font-size:0.9rem;'>TOPIC 2: MEDIUM / INTERNATIONAL</span>
                <p style='color:#ffffff; font-size:1.0rem; margin-top:8px;'>{st.session_state.lecturette_topics_pool[1]}</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div style='background-color:#1e293b; padding:15px; border-radius:8px; border-left:4px solid #f59e0b; margin-bottom:15px; min-height:140px;'>
                <span style='color:#f59e0b; font-weight:bold; font-size:0.9rem;'>TOPIC 3: LOW / TECHNOLOGY</span>
                <p style='color:#ffffff; font-size:1.0rem; margin-top:8px;'>{st.session_state.lecturette_topics_pool[2]}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style='background-color:#1e293b; padding:15px; border-radius:8px; border-left:4px solid #10b981; margin-bottom:15px; min-height:140px;'>
                <span style='color:#10b981; font-weight:bold; font-size:0.9rem;'>TOPIC 4: GENERAL / OBJECT-BASED</span>
                <p style='color:#ffffff; font-size:1.0rem; margin-top:8px;'>{st.session_state.lecturette_topics_pool[3]}</p>
            </div>
            """, unsafe_allow_html=True)

        # Select topic radio
        chosen_topic = st.radio(
            "Select one topic to speak on:",
            [
                f"1. High: {st.session_state.lecturette_topics_pool[0]}",
                f"2. Medium: {st.session_state.lecturette_topics_pool[1]}",
                f"3. Low: {st.session_state.lecturette_topics_pool[2]}",
                f"4. General: {st.session_state.lecturette_topics_pool[3]}"
            ]
        )

        st.markdown("---")
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("Generate New Topic Chits 🔄", use_container_width=True):
                st.session_state.lecturette_topics_pool = [
                    random.choice(LECTURETTE_TOPICS["High / National Affairs"]),
                    random.choice(LECTURETTE_TOPICS["Medium / International Relations"]),
                    random.choice(LECTURETTE_TOPICS["Low / Technology & Innovation"]),
                    random.choice(LECTURETTE_TOPICS["General / Object-based"])
                ]
                st.rerun()
        with col_btn2:
            if st.button("Proceed to Preparation (3 Mins) ➔", type="primary", use_container_width=True):
                # Clean choice string
                st.session_state.lecturette_selected_topic = chosen_topic.split(":", 1)[1].strip()
                st.session_state.lecturette_notes = ""
                st.session_state.lecturette_prep_start_time = time.time()
                st.session_state.lecturette_state = "prepare"
                st.rerun()

    # 2. PREPARING STATE
    elif st.session_state.lecturette_state == "prepare":
        st.subheader("📝 Preparation Phase (3 Minutes)")
        st.markdown(f"**Selected Topic:** `{st.session_state.lecturette_selected_topic}`")
        
        elapsed = time.time() - st.session_state.lecturette_prep_start_time
        remaining = int(180 - elapsed)
        
        if remaining <= 0:
            st.warning("⏰ Preparation time is up! Automatically proceeding to the Delivery Phase.")
            time.sleep(1.5)
            st.session_state.lecturette_speak_start_time = time.time()
            st.session_state.lecturette_state = "speak"
            st.rerun()
            
        mins, secs = divmod(remaining, 60)
        
        col_t, col_s = st.columns([3, 1])
        with col_t:
            st.markdown(f"⏱️ **Preparation Time Left:** `<span style='color:#f59e0b; font-size:1.4rem; font-weight:bold;'>{mins:02d}:{secs:02d}</span>`", unsafe_allow_html=True)
        with col_s:
            if st.button("Start Speaking Now ➔", type="primary", use_container_width=True):
                st.session_state.lecturette_speak_start_time = time.time()
                st.session_state.lecturette_state = "speak"
                st.rerun()
                
        st.markdown("""
        > [!TIP]
        > Jot down keywords, facts, and structure logic only. Avoid writing out full sentences!
        """)

        # Notes text area
        notes = st.text_area(
            "Scratchpad / Structural Skeleton Notes:",
            value=st.session_state.lecturette_notes,
            placeholder="Introduction:\n- Define the topic\n\nBody:\n- Aspect 1 (Causes/Pros)\n- Aspect 2 (Effects/Cons)\n\nConclusion:\n- Forward-looking solution",
            height=280
        )
        st.session_state.lecturette_notes = notes

        if st.button("🔄 Sync Timer", use_container_width=True):
            st.rerun()

    # 3. SPEAKING STATE
    elif st.session_state.lecturette_state == "speak":
        st.subheader("🗣️ Delivery Phase (5 Minutes)")
        st.markdown(f"**Topic:** `{st.session_state.lecturette_selected_topic}`")
        
        elapsed = time.time() - st.session_state.lecturette_speak_start_time
        remaining = int(300 - elapsed)
        
        if remaining <= 0:
            st.warning("⏰ Speaking time is up! Proceeding to the Evaluation phase.")
            time.sleep(1.5)
            st.session_state.lecturette_state = "evaluate"
            st.rerun()
            
        mins, secs = divmod(remaining, 60)
        
        col_t, col_s = st.columns([3, 1])
        with col_t:
            st.markdown(f"⏱️ **Delivery Time Remaining:** `<span style='color:#ef4444; font-size:1.4rem; font-weight:bold;'>{mins:02d}:{secs:02d}</span>`", unsafe_allow_html=True)
        with col_s:
            if st.button("Proceed to Evaluation ➔", type="primary", use_container_width=True):
                st.session_state.lecturette_state = "evaluate"
                st.rerun()
                
        col_notes, col_rec = st.columns([1, 1])
        with col_notes:
            st.markdown("#### 📝 Your Preparation Notes")
            if st.session_state.lecturette_notes.strip():
                st.info(st.session_state.lecturette_notes)
            else:
                st.info("No skeleton notes jotted down during preparation.")
                
        with col_rec:
            st.markdown("#### 🎙️ Record your Lecturette Speech")
            st.write("Stand up straight, keep your hands relaxed, maintain eye contact, and record your speech:")
            
            # Mic recorder
            audio = mic_recorder(
                start_prompt="Start Recording 🎙️",
                stop_prompt="Stop Recording 🛑",
                key="lecturette_mic"
            )
            
            if audio:
                st.success("Audio recorded successfully! You can listen back during the evaluation phase.")
                st.audio(audio['bytes'])
                st.session_state.lecturette_audio_bytes = audio['bytes']
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔄 Sync Timer", use_container_width=True):
                st.rerun()

    # 4. EVALUATION STATE
    elif st.session_state.lecturette_state == "evaluate":
        st.subheader("📊 Self-Evaluation & AI Psychological Analysis")
        st.markdown(f"**Topic:** `{st.session_state.lecturette_selected_topic}`")
        
        # Audio Playback
        if hasattr(st.session_state, "lecturette_audio_bytes") and st.session_state.lecturette_audio_bytes:
            st.write("🎙️ **Review your speech recording:**")
            st.audio(st.session_state.lecturette_audio_bytes)
            
        st.markdown("### 1. Self-Grading Rubric")
        st.write("Score your performance honestly based on the 4 key parameters (0 to 5):")
        
        col1, col2 = st.columns(2)
        with col1:
            g_structure = st.slider("Structure & Content (Intro, Body, Conclusion)", 0, 5, 3)
            g_accuracy = st.slider("Technical & Factual Accuracy (Data, Relevance)", 0, 5, 3)
        with col2:
            g_delivery = st.slider("Delivery & Body Language (Confidence, posture)", 0, 5, 3)
            g_time = st.slider("Time Management & Pacing (5-Minute stretch)", 0, 5, 3)
            
        total_score = g_structure + g_accuracy + g_delivery + g_time
        
        # Selectable evaluation
        is_selectable = (total_score >= 14) and (min(g_structure, g_accuracy, g_delivery, g_time) >= 3)
        
        if is_selectable:
            rating_text = "SELECTABLE RATING"
            rating_color = "#10b981"
            rating_desc = "Excellent! You meet the standards for SSB Lecturette. Your structure, facts, and delivery are consistent."
        else:
            rating_text = "DEVELOPMENT NEEDED"
            rating_color = "#ef4444"
            rating_desc = "Needs improvement. To achieve a selectable benchmark, you need a total score of 14+ with no single parameter scoring below 3."

        st.markdown(f"""
        <div style='background-color:#1e293b; border-left: 6px solid {rating_color}; padding: 20px; border-radius: 8px; margin-bottom: 20px;'>
            <h3 style='margin:0; color:#ffffff;'>Self Score: <span style='color:{rating_color};'>{total_score} / 20</span></h3>
            <h4 style='margin:6px 0 0 0; color:{rating_color};'>{rating_text}</h4>
            <p style='font-size:0.95rem; color:#94a3b8; margin: 8px 0 0 0;'>{rating_desc}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 2. Speech Analysis")
        st.write("Type or paste your spoken speech points or transcript below to run AI psychological profiling:")
        
        speech_text_input = st.text_area(
            "Paste your speech transcription here:",
            placeholder="Type what you spoke or paste your lecturette bullet points..."
        )
        
        if st.button("Evaluate Speech & Save to Dashboard ➔", type="primary", use_container_width=True):
            if not speech_text_input.strip():
                st.warning("Please enter your speech text to perform the analysis.")
            else:
                with st.spinner("Analyzing speech content and traits..."):
                    assessment = evaluate_lecturette_speech(
                        st.session_state.lecturette_selected_topic,
                        speech_text_input,
                        st.session_state.api_key
                    )
                    
                    st.session_state.lecturette_evaluation = assessment
                    
                    # Save to Performance Dashboard history list
                    history_key = f"lect_saved_{st.session_state.lecturette_speak_start_time}"
                    if history_key not in st.session_state:
                        st.session_state[history_key] = True
                        
                        # Generate demonstrated OLQs
                        olq_list = assessment.get("olqs_demonstrated", [])
                        olq_dict = {}
                        for o in olq_list:
                            olq_dict[o] = "Demonstrated clear command, facts, and structure for this GTO Lecturette topic."
                            
                        lec_history_entry = {
                            "test": f"GTO Lecturette ({st.session_state.lecturette_selected_topic[:30]}...)",
                            "response": f"Self-Score: {total_score}/20. Word Count: {assessment.get('word_count', 0)}",
                            "analysis": {
                                "sentiment": 0.8 if is_selectable else 0.4,
                                "confidence_score": total_score / 20.0,
                                "olqs_demonstrated": olq_dict,
                                "overall_evaluation": f"GTO Lecturette: {assessment.get('overall_evaluation', '')}",
                                "actionable_feedback": [
                                    assessment.get("structure_feedback", ""),
                                    assessment.get("content_depth_feedback", ""),
                                    assessment.get("delivery_feedback", "")
                                ]
                            }
                        }
                        st.session_state.history.append(lec_history_entry)

        # Show evaluation result
        if st.session_state.lecturette_evaluation:
            eval_res = st.session_state.lecturette_evaluation
            
            st.markdown("---")
            st.subheader("🎖️ AI GTO Lecturette Evaluation Report")
            
            if eval_res.get("error"):
                st.warning(eval_res["error"])
                
            st.markdown(f"**Total Words:** `{eval_res.get('word_count', 0)}` | **Filler Words Detected:** `{eval_res.get('filler_count', 0)}`")
            
            col_eval1, col_eval2 = st.columns(2)
            with col_eval1:
                st.markdown("#### 📝 Structure Feedback")
                st.info(eval_res.get("structure_feedback", ""))
                
                st.markdown("#### 🎙️ Delivery & Filler Feedback")
                st.info(eval_res.get("delivery_feedback", ""))
                
            with col_eval2:
                st.markdown("#### 💡 Content Depth & Facts")
                st.info(eval_res.get("content_depth_feedback", ""))
                
                st.markdown("#### 🌟 Demonstrated OLQs")
                for o in eval_res.get("olqs_demonstrated", []):
                    st.success(f"✔️ {o}")
                    
            st.markdown("#### 📋 Overall Evaluation")
            st.write(eval_res.get("overall_evaluation", ""))

        st.markdown("---")
        if st.button("Practice Another GTO Lecturette ↺", use_container_width=True):
            st.session_state.lecturette_state = "configure"
            st.session_state.lecturette_topics_pool = []
            st.session_state.lecturette_evaluation = {}
            st.rerun()

# -----------------
# 4. Performance Dashboard
# -----------------
elif test_mode == "📊 Performance Dashboard":
    st.components.v1.html(get_dashboard_logo(), height=130)
    render_page_navigation("📊 Performance Dashboard", "dashboard")

    
    if not st.session_state.history:
        st.info("No practice history found yet. Complete a TAT, WAT, or SRT test to view your dashboard analytics!")
    else:
        # Display history summary metrics
        total_tests = len(st.session_state.history)
        avg_sentiment = sum(h["analysis"].get("sentiment", 0.0) for h in st.session_state.history) / total_tests
        avg_confidence = sum(h["analysis"].get("confidence_score", 0.5) for h in st.session_state.history) / total_tests
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Tests Evaluated", total_tests)
        col2.metric("Average Attitude Index", f"{avg_sentiment:+.2f}")
        col3.metric("Average Confidence / Resolve", f"{avg_confidence * 100:.0f}%")
        
        st.markdown("---")
        
        # Aggregate OLQ data
        olq_counts = {}
        for h in st.session_state.history:
            olqs = h["analysis"].get("olqs_demonstrated", {})
            for olq in olqs:
                olq_counts[olq] = olq_counts.get(olq, 0) + 1
                
        # Show OLQ progress/demonstrated count
        st.subheader("🌟 Officer Like Qualities (OLQ) Distribution")
        if olq_counts:
            # Render a custom horizontal bar chart using HTML/CSS
            max_val = max(olq_counts.values())
            for olq, count in sorted(olq_counts.items(), key=lambda x: x[1], reverse=True):
                pct = int((count / max_val) * 100)
                st.markdown(f"""
                <div style='margin-bottom: 0.75rem;'>
                    <div style='display: flex; justify-content: space-between; font-weight: bold;'>
                        <span>{olq}</span>
                        <span>{count} time(s)</span>
                    </div>
                    <div style='background-color: #334155; width: 100%; height: 12px; border-radius: 6px; overflow: hidden;'>
                        <div style='background-color: #3b82f6; width: {pct}%; height: 100%; border-radius: 6px;'></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No OLQs have been registered in your history yet.")
            
        st.markdown("---")
        st.subheader("📜 Detailed Attempt History")
        for i, h in enumerate(reversed(st.session_state.history)):
            with st.expander(f"Attempt {total_tests - i}: {h['test_type']} ({h['timestamp']})"):
                if h['context']:
                    st.markdown(f"**Context/Prompt:** *{h['context']}*")
                st.markdown(f"**Your Response:**\n> {h['text']}")
                st.markdown("---")
                
                # Summary details in columns
                c1, c2 = st.columns(2)
                c1.write(f"**Attitude Index:** `{h['analysis'].get('sentiment', 0.0):+.2f}`")
                c2.write(f"**Confidence:** `{h['analysis'].get('confidence_score', 0.5) * 100:.0f}%`")
                
                st.write("**OLQs Identified:**")
                for olq, exp in h["analysis"].get("olqs_demonstrated", {}).items():
                    st.markdown(f"- **{olq}**: *{exp}*")
                
                st.write("**Evaluation summary:**")
                st.info(h["analysis"].get("overall_evaluation", "N/A"))

else:
    # Inject Custom CSS specifically for the Big Grid Buttons on Dashboard Menu
    st.markdown(
        """
        <style>
            /* App Title Styling */
            .main-title {
                font-family: 'Outfit', 'Inter', sans-serif !important;
                font-size: 4rem !important;
                font-weight: 900 !important;
                background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 50%, #10b981 100%) !important;
                -webkit-background-clip: text !important;
                -webkit-text-fill-color: transparent !important;
                text-align: center !important;
                margin-bottom: 5px !important;
                letter-spacing: -1px !important;
                text-transform: uppercase !important;
                filter: drop-shadow(0 2px 8px rgba(59, 130, 246, 0.3)) !important;
            }
            .subtitle {
                font-family: 'Inter', sans-serif !important;
                font-size: 1.25rem !important;
                color: #10B981 !important;
                text-align: center !important;
                font-weight: 700 !important;
                margin-top: 0px !important;
                margin-bottom: 3.5rem !important;
                letter-spacing: 4px !important;
                text-transform: uppercase !important;
                opacity: 0.9 !important;
            }
            
            /* Section Heading */
            .section-title {
                font-family: 'Outfit', sans-serif !important;
                font-size: 1.8rem !important;
                font-weight: 700 !important;
                color: #f1f5f9 !important;
                margin-top: 2rem !important;
                margin-bottom: 1.5rem !important;
                border-left: 5px solid #3b82f6 !important;
                padding-left: 15px !important;
                letter-spacing: 0.5px !important;
            }
            
            /* Big Custom Card Styling for Test Modes */
            div.stButton > button {
                width: 100% !important;
                height: 160px !important;
                font-family: 'Inter', sans-serif !important;
                font-size: 1.1rem !important;
                font-weight: 700 !important;
                color: #ffffff !important;
                background: linear-gradient(145deg, #1e293b 0%, #0f172a 100%) !important;
                border: 1px solid rgba(255, 255, 255, 0.08) !important;
                border-radius: 16px !important;
                box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3) !important;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
                white-space: pre-wrap !important;
                line-height: 1.5 !important;
                padding: 15px !important;
            }
            
            /* Hover effects like a true portfolio dashboard */
            div.stButton > button:hover {
                border-color: #3b82f6 !important;
                color: #60a5fa !important;
                background: linear-gradient(145deg, #1e293b 0%, #1e1b4b 100%) !important;
                transform: translateY(-5px) !important;
                box-shadow: 0 15px 30px rgba(59, 130, 246, 0.25) !important;
            }
            
            /* Subtle line separator */
            .separator {
                border-bottom: 2px solid #334155;
                margin-top: 3rem;
                margin-bottom: 3rem;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Header Section
    st.components.v1.html(get_main_app_logo(), height=155)
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("<p class='section-title'>⚡ Choose Your Training Module</p>", unsafe_allow_html=True)
    
    # Designing a clean 4-Column Grid Layout for big, readable components
    row1_col1, row1_col2, row1_col3, row1_col4 = st.columns(4)
    row2_col1, row2_col2, row2_col3, row2_col4 = st.columns(4)
    
    # Row 1 Grid Buttons
    with row1_col1:
        if st.button("📋\n\nPIQ Digitizer\n(Profile Analyzer)", key="piq"):
            st.session_state.current_mode = "📋 PIQ Form Digitizer"
            st.rerun()
            
    with row1_col2:
        if st.button("📐\n\nOIR Practice\n(Officer Intelligence)", key="oir"):
            st.session_state.current_mode = "📐 OIR Practice Exam"
            st.rerun()
            
    with row1_col3:
        if st.button("🖼️\n\nPPDT / TAT\n(Picture Perception)", key="ppdt"):
            st.session_state.current_mode = "🖼️ PPDT / TAT Mode"
            st.rerun()
            
    with row1_col4:
        if st.button("✍️\n\nWAT Module\n(Word Association)", key="wat"):
            st.session_state.current_mode = "✍️ WAT (Word Association)"
            st.rerun()
            
    # Row 2 Grid Buttons
    with row2_col1:
        if st.button("🧠\n\nSRT Module\n(Situation Reaction)", key="srt"):
            st.session_state.current_mode = "🧠 SRT (Situation Reaction)"
            st.rerun()
            
    with row2_col2:
        if st.button("🗣️\n\nGTO Lecturette\n(Speaking Sprint)", key="gto"):
            st.session_state.current_mode = "🗣️ GTO Lecturette"
            st.rerun()
            
    with row2_col3:
        if st.button("🎙️\n\nSpeech & Mock\n(Voice Interview)", key="mock"):
            st.session_state.current_mode = "🎙️ Speech & Mock Interview"
            st.rerun()
            
    with row2_col4:
        if st.button("📊\n\nPerformance\n(Analytics Hub)", key="perf"):
            st.session_state.current_mode = "📊 Performance Dashboard"
            st.rerun()

    # Decorative separator line
    st.markdown("<div class='separator'></div>", unsafe_allow_html=True)
    
    # Settings and configuration moved elegantly to a lower full-width block or expander
    st.markdown("<p class='section-title'>⚙️ System Configuration</p>", unsafe_allow_html=True)
    
    config_col1, config_col2 = st.columns([2, 1])
    with config_col1:
        gemini_key = st.text_input(
            "Google Gemini API Key", 
            type="password", 
            value=st.session_state.api_key,
            placeholder="Enter your API Key to activate deep psychological insights analytics...",
            help="Your key remains secured locally on your session deployment."
        )
        if gemini_key != st.session_state.api_key:
            st.session_state.api_key = gemini_key
            st.rerun()
    with config_col2:
        # Dynamic active module presentation box
        st.markdown(f"""
            <div style='background-color: #1e293b; border-left: 6px solid #3b82f6; padding: 16px; border-radius: 8px; margin-top: 4px; border: 1px solid #334155; border-left-width: 6px;'>
                <span style='color: #3b82f6; font-weight: 700; font-size: 1.1rem;'>ACTIVE FOCUS:</span><br>
                <span style='color: #ffffff; font-weight: 600; font-size: 1.3rem;'>{st.session_state.current_mode}</span>
            </div>
        """, unsafe_allow_html=True)