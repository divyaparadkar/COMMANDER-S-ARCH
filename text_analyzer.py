import os
import re
import json
# pyrefly: ignore [missing-import]
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer  # pyrefly: ignore [missing-import]
import google.generativeai as genai  # pyrefly: ignore [missing-import]

# Download safety for environments where it wasn't pre-downloaded
try:
    sia = SentimentIntensityAnalyzer()
except LookupError:
    nltk.download('vader_lexicon', quiet=True)
    sia = SentimentIntensityAnalyzer()

OLQ_KEYWORDS = {
    "Effective Intelligence": ["solve", "idea", "logic", "reason", "intellect", "understand", "learn", "find", "analyze"],
    "Reasoning Ability": ["because", "therefore", "reason", "conclude", "why", "cause", "logic", "due to"],
    "Organising Ability": ["plan", "organise", "prepare", "arrange", "manage", "resource", "gather", "coordinate"],
    "Power of Expression": ["speak", "explain", "express", "write", "present", "convince", "clear", "articulate"],
    "Social Adaptability": ["adapt", "adjust", "new", "culture", "village", "people", "community", "meet", "accept"],
    "Cooperation": ["team", "group", "cooperate", "together", "joint", "share", "help", "support", "collaborate"],
    "Sense of Responsibility": ["duty", "responsible", "obligation", "honest", "truth", "sincere", "care", "moral"],
    "Initiative": ["initiate", "lead", "start", "first", "forward", "volunteer", "step up", "begin"],
    "Self-Confidence": ["confident", "sure", "believe", "certain", "achieve", "trust", "capable"],
    "Speed of Decision": ["decide", "immediately", "quick", "fast", "prompt", "instant", "chose"],
    "Ability to Influence": ["convince", "influence", "motivate", "inspire", "persuade", "guide", "guide"],
    "Liveliness": ["cheerful", "lively", "happy", "smile", "enthusiastic", "energetic", "optimistic", "enjoy"],
    "Determination": ["determine", "persist", "try", "strive", "firm", "achieve", "fail", "win", "continue"],
    "Courage": ["brave", "courage", "fearless", "risk", "bold", "face", "danger", "rescue"],
    "Stamina": ["stamina", "endure", "persist", "long", "hardwork", "effort", "tireless", "strength"]
}

def local_analyze_text(text: str) -> dict:
    """
    Performs local text analysis using NLTK VADER and keyword matching.
    Does not require external APIs.
    """
    if not text.strip():
        return {
            "error": "Empty text provided.",
            "word_count": 0,
            "sentence_count": 0,
            "sentiment": 0.0,
            "confidence_score": 0.5,
            "olqs_demonstrated": {},
            "overall_evaluation": "Please write a response to get an analysis.",
            "actionable_feedback": []
        }

    # Basic stats
    words = [w for w in re.findall(r'\w+', text.lower())]
    word_count = len(words)
    
    try:
        sentences = nltk.sent_tokenize(text)
        sentence_count = len(sentences)
    except Exception:
        sentences = text.split('.')
        sentence_count = len([s for s in sentences if s.strip()])

    # Sentiment analysis (VADER)
    scores = sia.polarity_scores(text)
    sentiment = scores['compound']  # ranges from -1 to +1
    
    # Keyword-based OLQ detection
    olqs_demonstrated = {}
    for olq, keywords in OLQ_KEYWORDS.items():
        matched = []
        for kw in keywords:
            if re.search(r'\b' + re.escape(kw) + r'\b', text.lower()):
                matched.append(kw)
        if matched:
            olqs_demonstrated[olq] = f"Keywords detected: {', '.join(matched)}"

    # Determine confidence score based on sentiment, sentence structure and strong action verbs
    strong_action_verbs = ["resolved", "decided", "rescued", "planned", "led", "managed", "helped", "achieved", "completed", "acted"]
    action_verb_count = sum(1 for verb in strong_action_verbs if verb in words)
    
    # Base confidence on action-oriented words and sentiment
    confidence_score = min(1.0, 0.4 + (action_verb_count * 0.1) + (max(0, sentiment) * 0.2))

    # Construct feedback
    actionable_feedback = []
    if word_count < 10:
        actionable_feedback.append("Your response is very short. Try to write a complete story/action containing details.")
    if sentiment < -0.1:
        actionable_feedback.append("The sentiment of the response is somewhat negative. Try to focus on constructive actions and a positive outcome.")
    if action_verb_count == 0:
        actionable_feedback.append("Your response lacks strong action verbs. Use active verbs (e.g. 'organized', 'helped', 'reached') to show leadership and initiative.")
    if len(olqs_demonstrated) < 2:
        actionable_feedback.append("Try to demonstrate more Officer Like Qualities like cooperation, planning, or social responsibility in your response.")

    overall_evaluation = f"This is a local analysis. The response contains {word_count} words and {sentence_count} sentences. "
    if sentiment >= 0.1:
        overall_evaluation += "The tone of your writing is positive and constructive. "
    elif sentiment <= -0.1:
        overall_evaluation += "The tone of your writing shows some anxiety or negative outlook. "
    else:
        overall_evaluation += "The tone is neutral. "
        
    if action_verb_count > 0:
        overall_evaluation += "You have used active verbs to describe actions taken, demonstrating an active problem-solving mindset."
    else:
        overall_evaluation += "The story could be made more active by describing direct, constructive steps taken by the main character."

    return {
        "word_count": word_count,
        "sentence_count": sentence_count,
        "sentiment": sentiment,
        "confidence_score": round(confidence_score, 2),
        "olqs_demonstrated": olqs_demonstrated,
        "overall_evaluation": overall_evaluation,
        "actionable_feedback": actionable_feedback if actionable_feedback else ["Great job! Your response is structured well and active."]
    }

def gemini_analyze_text(text: str, api_key: str, test_type: str, context: str = None) -> dict:
    """
    Performs advanced psychological and OLQ evaluation of user response/story using Google Gemini.
    Returns a dict containing sentiment, confidence_score, olqs_demonstrated, overall_evaluation, and actionable_feedback.
    """
    if not api_key:
        return {"error": "API Key is missing. Falling back to local analysis."}
        
    try:
        genai.configure(api_key=api_key)
        # Using gemini-2.5-flash as default, fallback to gemini-1.5-flash if needed
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f"""
You are an expert Psychologist and SSB (Services Selection Board) Assessor.
Evaluate the candidate's response in the {test_type} test for officer-like qualities (OLQs).

=== Test Type Details ===
- TAT / PPDT: Candidate is shown an image and writes a complete story (past, present, future) about it.
- WAT (Word Association Test): Candidate is shown a word and must write a short sentence/association.
- SRT (Situation Reaction Test): Candidate is presented with a challenging situation and describes their reaction.

=== Candidate's Response ===
"{text}"
"""
        if context:
            prompt += f"\n=== Context/Prompt shown to candidate (e.g. Word or Situation or Image description) ===\n\"{context}\"\n"

        prompt += """
Perform a deep psychological analysis. You must output the analysis EXACTLY as a valid JSON object with the following keys. Do not include markdown code block formatting (like ```json), just output the raw JSON text.

Keys required in JSON:
1. "sentiment": A float value between -1.0 (very negative/defeatist) and 1.0 (highly positive/constructive).
2. "confidence_score": A float value between 0.0 (anxious/unsure) and 1.0 (very assertive/confident).
3. "olqs_demonstrated": A dictionary/object where keys are OLQs demonstrated (e.g., "Effective Intelligence", "Social Adaptability", "Initiative", "Determination", "Courage", "Sense of Responsibility", "Organising Ability") and values are brief explanations of how they were demonstrated in the text. List only the relevant OLQs (maximum 4-5).
4. "overall_evaluation": A brief paragraph summarizing the candidate's personality traits shown here, focusing on whether they have a constructive, active problem-solving mindset, or if they show escapism, passivity, or fear.
5. "actionable_feedback": A list of 2-3 specific, actionable points for improvement.

JSON Output:
"""
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json"
            )
        )
        
        # Parse JSON
        result = json.loads(response.text.strip())
        return result
        
    except Exception as e:
        return {
            "error": f"Failed to connect to Gemini API: {str(e)}. Using local analysis instead.",
            "local_fallback": True
        }

def generate_interview_questions(profile: str, api_key: str, piq_data: dict = None) -> list:
    """
    Generates 5 mock interview questions tailored to the selected profile.
    If no API key is provided or the API call fails, falls back to pre-defined questions.
    Can dynamically tailor questions based on filled PIQ data if provided.
    """
    import random
    from data_bank import INTERVIEW_QUESTIONS
    
    if not api_key:
        questions = INTERVIEW_QUESTIONS.get(profile, INTERVIEW_QUESTIONS["Personal & PIQ-based"])
        return random.sample(questions, min(5, len(questions)))
        
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f"""
You are an expert SSB Interviewing Officer (IO).
Generate exactly 5 realistic, challenging, and professional interview questions for a candidate under the category "{profile}".
The questions should evaluate officer-like qualities (OLQs) such as reasoning ability, power of expression, determination, and sense of responsibility.
"""
        if piq_data:
            prompt += f"""
Here is the candidate's Personal Information Questionnaire (PIQ) data:
{json.dumps(piq_data, indent=2)}

You MUST customize at least 3 of the 5 generated questions to specifically reference details from this PIQ (e.g., their name, achievements, hobbies, academic choices, family occupation, previous SSB attempts if any, or sports). Keep the tone professional but highly personalized, as a real SSB Interviewing Officer would do during the personal interview.
"""
        prompt += """
Output the questions strictly as a JSON array of strings (e.g., ["Question 1", "Question 2", ...]). Do not include markdown code block formatting (like ```json), just output the raw JSON text.
"""
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json"
            )
        )
        questions = json.loads(response.text.strip())
        if isinstance(questions, list) and len(questions) > 0:
            return questions
        raise ValueError("Invalid format returned")
    except Exception:
        questions = INTERVIEW_QUESTIONS.get(profile, INTERVIEW_QUESTIONS["Personal & PIQ-based"])
        return random.sample(questions, min(5, len(questions)))

def evaluate_interview_answer(question: str, answer: str, api_key: str) -> dict:
    """
    Evaluates the candidate's spoken/written answer to a mock interview question.
    """
    if not answer.strip():
        return {
            "error": "Empty response provided.",
            "sentiment": 0.0,
            "confidence_score": 0.5,
            "olqs_demonstrated": {},
            "overall_evaluation": "Please provide an answer to get feedback.",
            "actionable_feedback": []
        }

    if not api_key:
        return local_analyze_text(answer)
        
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"""
You are an expert SSB Interviewing Officer (IO) and Psychologist.
Evaluate the candidate's response to the following interview question.

=== Question ===
"{question}"

=== Candidate's Spoken Answer ===
"{answer}"

Perform a deep psychological and communication evaluation. You must output the analysis EXACTLY as a valid JSON object with the following keys. Do not include markdown code block formatting (like ```json), just output the raw JSON text.

Keys required in JSON:
1. "sentiment": A float value between -1.0 (very negative/defeatist) and 1.0 (highly positive/constructive).
2. "confidence_score": A float value between 0.0 (anxious/unsure) and 1.0 (very assertive/confident).
3. "olqs_demonstrated": A dictionary/object where keys are OLQs demonstrated and values are brief explanations of how they were demonstrated. List only the relevant OLQs (maximum 3-4).
4. "overall_evaluation": A brief paragraph summarizing the candidate's delivery, communication skills, confidence, and structure of the answer. Highlight whether they were clear, structured, and constructive.
5. "actionable_feedback": A list of 2-3 specific, actionable points for improving their spoken response (e.g. structure, content, vocabulary).

JSON Output:
"""
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json"
            )
        )
        result = json.loads(response.text.strip())
        return result
    except Exception as e:
        local_res = local_analyze_text(answer)
        local_res["error"] = f"Failed to connect to Gemini API: {str(e)}. Using local analysis instead."
        local_res["local_fallback"] = True
        return local_res

def analyze_piq_data(piq_data: dict, api_key: str) -> dict:
    """
    Evaluates the candidate's PIQ entries, identifying strong points, potential focus areas,
    and generating probable IO interview questions.
    """
    if not api_key:
        # Local analysis fallback
        strong = ["Filled out basic details systematically."]
        weaknesses = []
        recommendations = ["Consider using the Gemini API key to get personalized psychological profile analysis."]
        
        # Look for achievements or sports
        if piq_data.get("hobbies"):
            strong.append(f"Exhibited hobby/interest: {piq_data.get('hobbies')}")
        if piq_data.get("sports_raw") or piq_data.get("sports_editor"):
            strong.append("Indicated games and sports participation, displaying physical liveliness.")
        else:
            weaknesses.append("No active sports participation declared in the PIQ. Be prepared to explain physical fitness and team qualities.")
            recommendations.append("Develop a hobby or describe physical activities/workouts you routinely undertake to show energy and teamwork.")
            
        if piq_data.get("ncc_training") == "Yes":
            strong.append("NCC training provides structured discipline background.")
        
        prev_attempts = piq_data.get("previous_attempts_count", 0)
        try:
            prev_attempts = int(prev_attempts)
        except Exception:
            prev_attempts = 0
            
        if prev_attempts > 0:
            weaknesses.append(f"Candidate has {prev_attempts} previous attempts. The IO will probe deeply into why you were not recommended previously.")
            recommendations.append("Analyze your previous failures objectively. Clearly explain what improvements you have made since your last attempt.")
            
        return {
            "strong_points": strong,
            "potential_weaknesses": weaknesses,
            "recommended_focus_areas": recommendations,
            "probable_questions": [
                f"Introduce yourself and explain why you want to join the services.",
                f"Tell me about your hobby '{piq_data.get('hobbies', 'N/A')}' and how it helps you grow.",
                f"What did you do during your previous {prev_attempts} attempts, and how did you prepare differently this time?" if prev_attempts > 0 else "Why did you choose this type of commission?",
                "What is your father's occupation and how does he inspire you?",
                "Tell me about your educational path and why you chose your major/medium."
            ],
            "local_fallback": True
        }

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"""
You are an expert SSB Interviewing Officer (IO) and Psychologist.
Analyze the candidate's Personal Information Questionnaire (PIQ) data:

{json.dumps(piq_data, indent=2)}

Perform a comprehensive profile assessment. You must output the analysis EXACTLY as a valid JSON object with the following keys. Do not include markdown code block formatting (like ```json), just output the raw JSON text.

Keys required in JSON:
1. "strong_points": A list of 3-4 strings detailing the candidate's key strengths as shown in this PIQ (e.g. academic consistency, sports achievements, NCC background, hobbies, responsibilities held).
2. "potential_weaknesses": A list of 2-3 strings highlighting potential weak areas, vulnerabilities, or discrepancies the Interviewing Officer (IO) might probe (e.g., lack of sports/co-curriculars, low academic marks, multiple previous attempts, family dependencies, etc.).
3. "recommended_focus_areas": A list of 2-3 specific recommendations on how the candidate can defend their weak areas and project their strengths constructively during the interview.
4. "probable_questions": A list of 6-8 highly personalized, specific questions that a real SSB Interviewing Officer (IO) is likely to ask them based on this PIQ (e.g., asking about their specific hobbies, why they chose their qualification, why they failed in previous attempts, questions about their siblings or parents' occupation).

JSON Output:
"""
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json"
            )
        )
        result = json.loads(response.text.strip())
        return result
    except Exception as e:
        res = analyze_piq_data(piq_data, "")
        res["error"] = f"Failed to connect to Gemini API: {str(e)}. Using local analysis instead."
        return res


def evaluate_lecturette_speech(topic: str, speech_text: str, api_key: str) -> dict:
    """
    Evaluate the transcribed speech text for a GTO Lecturette topic.
    Returns details on content depth, structure, filler word usage, and OLQs.
    """
    # Local fallback logic first
    words = speech_text.split()
    word_count = len(words)
    
    # Simple filler words matching
    fillers = ["uh", "um", "ah", "basically", "like", "actually", "you know"]
    filler_count = 0
    for w in words:
        cleaned = w.lower().strip(",.?!:;")
        if cleaned in fillers:
            filler_count += 1
            
    # Simple OLQ keyword matching
    olq_matches = []
    olq_keywords = {
        "Effective Intelligence": ["logic", "solution", "strategic", "analysis", "system", "infrastructure"],
        "Reasoning Ability": ["because", "therefore", "consequently", "hence", "reason", "impact"],
        "Power of Expression": ["clearly", "specifically", "illustrate", "express", "demonstrate"],
        "Social Adaptability": ["cooperation", "community", "society", "collaboration", "integration"],
        "Sense of Responsibility": ["duty", "obligation", "responsibility", "governance", "security"]
    }
    for olq, keywords in olq_keywords.items():
        for kw in keywords:
            if kw in speech_text.lower():
                olq_matches.append(olq)
                break
                
    local_result = {
        "word_count": word_count,
        "filler_count": filler_count,
        "olqs_demonstrated": list(set(olq_matches)),
        "structure_feedback": "Ensure a clear structure of: Introduction (45s), Body (3.5m), and forward-looking Conclusion (45s).",
        "content_depth_feedback": "Try to incorporate more factual statistics, historical timeline points, and current events to build depth.",
        "delivery_feedback": f"Your text has {filler_count} common speech fillers (e.g. 'um', 'basically'). Work on pausing silently instead of using verbal filler sounds.",
        "overall_evaluation": "Practice delivery pacing. Aim for 120-150 words per minute to maintain steady transmission."
    }

    if not api_key:
        return local_result

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"""
You are an expert SSB GTO (Group Testing Officer) and psychologist.
Analyze the candidate's transcribed speech for the following GTO Lecturette topic:

Topic: {topic}
Speech Transcript:
\"\"\"
{speech_text}
\"\"\"

Evaluate the speech text and output the results EXACTLY as a valid JSON object with the following keys. Do not include markdown code block formatting (like ```json), just output the raw JSON text.

Keys required in JSON:
1. "structure_feedback": A string giving detailed feedback on the introduction, body division, and conclusion.
2. "content_depth_feedback": A string evaluating factual accuracy, data depth, and relevance.
3. "delivery_feedback": A string giving feedback on tone, filler words (if visible in transcript), and logical pacing.
4. "olqs_demonstrated": A list of strings listing which of the 15 SSB Officer Like Qualities (OLQs) were demonstrated in this speech content (e.g. "Reasoning Ability", "Effective Intelligence", "Power of Expression").
5. "overall_evaluation": A detailed summary paragraph of the speech quality and whether it meets SSB standards.

JSON Output:
"""
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json"
            )
        )
        result = json.loads(response.text.strip())
        # Preserve word/filler metrics
        result["word_count"] = word_count
        result["filler_count"] = filler_count
        return result
    except Exception as e:
        local_result["error"] = f"Failed to connect to Gemini API: {str(e)}. Using local heuristics instead."
        return local_result



