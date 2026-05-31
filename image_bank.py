import os
import random

def get_random_ppdt():
    # Get the directory of the current file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(base_dir, "ppdt images")
    
    if not os.path.exists(image_dir):
        return None
        
    # List all supported image formats
    valid_extensions = ('.png', '.jpg', '.jpeg', '.webp')
    images = [
        os.path.join(image_dir, f) 
        for f in os.listdir(image_dir) 
        if f.lower().endswith(valid_extensions)
    ]
    
    if not images:
        return None
        
    return random.choice(images)

def get_ppdt_logo():
    return """
    <svg width="100%" height="130" viewBox="0 0 600 130" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="ppdt-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#3b82f6" />
                <stop offset="100%" stop-color="#1d4ed8" />
            </linearGradient>
            <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="4" result="blur" />
                <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
        </defs>
        <rect width="100%" height="100%" fill="#0f172a" rx="12"/>
        <g transform="translate(30, 15)">
            <!-- Projector / Frame Icon -->
            <rect x="10" y="10" width="100" height="80" rx="8" fill="none" stroke="url(#ppdt-grad)" stroke-width="4" filter="url(#glow)"/>
            <line x1="30" y1="90" x2="10" y2="110" stroke="#3b82f6" stroke-width="4" stroke-linecap="round"/>
            <line x1="90" y1="90" x2="110" y2="110" stroke="#3b82f6" stroke-width="4" stroke-linecap="round"/>
            <!-- Inner Canvas Picture -->
            <polygon points="25,75 50,45 70,60 95,35 95,75" fill="#1e3a8a" opacity="0.7"/>
            <circle cx="45" cy="35" r="6" fill="#facc15"/>
            <!-- Pencil writing overlay -->
            <g transform="translate(80, 50) rotate(-45)">
                <rect x="0" y="0" width="10" height="40" rx="2" fill="#38bdf8"/>
                <polygon points="0,0 5,-10 10,0" fill="#facc15"/>
            </g>
        </g>
        <!-- Title Text -->
        <text x="170" y="60" font-family="'Outfit', 'Inter', sans-serif" font-size="28" font-weight="bold" fill="#ffffff">PPDT & TAT Practice</text>
        <text x="170" y="90" font-family="'Inter', sans-serif" font-size="14" fill="#94a3b8">Picture Perception & Thematic Apperception Test Mode</text>
    </svg>
    """

def get_wat_logo():
    return """
    <svg width="100%" height="130" viewBox="0 0 600 130" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="wat-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#10b981" />
                <stop offset="100%" stop-color="#047857" />
            </linearGradient>
            <filter id="glow-wat" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="4" result="blur" />
                <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
        </defs>
        <rect width="100%" height="100%" fill="#0f172a" rx="12"/>
        <g transform="translate(30, 15)">
            <!-- Word Bubble connection graphic -->
            <path d="M 20 50 A 35 35 0 0 1 90 50 A 35 35 0 0 1 20 50" fill="none" stroke="url(#wat-grad)" stroke-width="4" filter="url(#glow-wat)"/>
            <path d="M 80 75 L 95 90 L 85 65" fill="none" stroke="url(#wat-grad)" stroke-width="4" stroke-linejoin="round"/>
            <!-- Word / Lightning Spark inside bubble -->
            <path d="M 45 35 L 65 50 L 45 55 L 60 75" fill="none" stroke="#6ee7b7" stroke-width="3" stroke-linecap="round"/>
            <circle cx="45" cy="35" r="3" fill="#6ee7b7"/>
            <circle cx="60" cy="75" r="3" fill="#6ee7b7"/>
        </g>
        <!-- Title Text -->
        <text x="170" y="60" font-family="'Outfit', 'Inter', sans-serif" font-size="28" font-weight="bold" fill="#ffffff">Word Association Test (WAT)</text>
        <text x="170" y="90" font-family="'Inter', sans-serif" font-size="14" fill="#94a3b8">15-Second active word projection & response aggregation</text>
    </svg>
    """

def get_srt_logo():
    return """
    <svg width="100%" height="130" viewBox="0 0 600 130" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="srt-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#f59e0b" />
                <stop offset="100%" stop-color="#d97706" />
            </linearGradient>
            <filter id="glow-srt" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="4" result="blur" />
                <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
        </defs>
        <rect width="100%" height="100%" fill="#0f172a" rx="12"/>
        <g transform="translate(30, 15)">
            <!-- Shield structure -->
            <path d="M 60 10 L 100 25 L 100 65 C 100 95 60 110 60 110 C 60 110 20 95 20 65 L 20 25 Z" fill="none" stroke="url(#srt-grad)" stroke-width="4" filter="url(#glow-srt)"/>
            <!-- Reaction Exclamation -->
            <path d="M 60 35 L 60 65" stroke="#fef08a" stroke-width="6" stroke-linecap="round"/>
            <circle cx="60" cy="82" r="5.5" fill="#fef08a"/>
        </g>
        <!-- Title Text -->
        <text x="170" y="60" font-family="'Outfit', 'Inter', sans-serif" font-size="28" font-weight="bold" fill="#ffffff">Situation Reaction Test (SRT)</text>
        <text x="170" y="90" font-family="'Inter', sans-serif" font-size="14" fill="#94a3b8">Crisis simulation, problem solving & active decision speed</text>
    </svg>
    """

def get_interview_logo():
    return """
    <svg width="100%" height="130" viewBox="0 0 600 130" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="int-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#ec4899" />
                <stop offset="100%" stop-color="#be185d" />
            </linearGradient>
            <filter id="glow-int" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="4" result="blur" />
                <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
        </defs>
        <rect width="100%" height="100%" fill="#0f172a" rx="12"/>
        <g transform="translate(30, 15)">
            <!-- Microphone graphic -->
            <rect x="45" y="15" width="30" height="55" rx="15" fill="none" stroke="url(#int-grad)" stroke-width="4" filter="url(#glow-int)"/>
            <!-- Mic Grill detail -->
            <line x1="45" y1="35" x2="75" y2="35" stroke="#fbcfe8" stroke-width="2"/>
            <line x1="45" y1="45" x2="75" y2="45" stroke="#fbcfe8" stroke-width="2"/>
            <!-- Stand -->
            <path d="M 35 50 C 35 80 85 80 85 50" fill="none" stroke="url(#int-grad)" stroke-width="4"/>
            <line x1="60" y1="78" x2="60" y2="105" stroke="url(#int-grad)" stroke-width="4"/>
            <line x1="40" y1="105" x2="80" y2="105" stroke="url(#int-grad)" stroke-width="4" stroke-linecap="round"/>
            <!-- Audio Waves -->
            <path d="M 95 30 C 105 40 105 60 95 70" fill="none" stroke="#fbcfe8" stroke-width="3" stroke-linecap="round"/>
            <path d="M 25 30 C 15 40 15 60 25 70" fill="none" stroke="#fbcfe8" stroke-width="3" stroke-linecap="round"/>
        </g>
        <!-- Title Text -->
        <text x="170" y="60" font-family="'Outfit', 'Inter', sans-serif" font-size="28" font-weight="bold" fill="#ffffff">Speech & Mock Interview</text>
        <text x="170" y="90" font-family="'Inter', sans-serif" font-size="14" fill="#94a3b8">PIQ-personalized questions, audio recording & confidence check</text>
    </svg>
    """

def get_piq_logo():
    return """
    <svg width="100%" height="130" viewBox="0 0 600 130" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="piq-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#06b6d4" />
                <stop offset="100%" stop-color="#0891b2" />
            </linearGradient>
            <filter id="glow-piq" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="4" result="blur" />
                <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
        </defs>
        <rect width="100%" height="100%" fill="#0f172a" rx="12"/>
        <g transform="translate(30, 15)">
            <!-- Clipboard Card -->
            <rect x="20" y="15" width="80" height="90" rx="8" fill="none" stroke="url(#piq-grad)" stroke-width="4" filter="url(#glow-piq)"/>
            <!-- Clipboard Clip -->
            <path d="M 45 15 L 45 8 C 45 5 75 5 75 8 L 75 15" fill="none" stroke="#22d3ee" stroke-width="3" stroke-linecap="round"/>
            <!-- Form Details -->
            <line x1="35" y1="35" x2="85" y2="35" stroke="#22d3ee" stroke-width="3" stroke-linecap="round"/>
            <line x1="35" y1="55" x2="85" y2="55" stroke="#22d3ee" stroke-width="3" stroke-linecap="round"/>
            <line x1="35" y1="75" x2="65" y2="75" stroke="#22d3ee" stroke-width="3" stroke-linecap="round"/>
            <!-- User Silhouette corner overlay -->
            <circle cx="80" cy="85" r="9" fill="#0891b2"/>
        </g>
        <!-- Title Text -->
        <text x="170" y="60" font-family="'Outfit', 'Inter', sans-serif" font-size="28" font-weight="bold" fill="#ffffff">PIQ Form Digitizer</text>
        <text x="170" y="90" font-family="'Inter', sans-serif" font-size="14" fill="#94a3b8">Structured personal questionnaire entry, export & IO question trigger</text>
    </svg>
    """

def get_oir_logo():
    return """
    <svg width="100%" height="130" viewBox="0 0 600 130" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="oir-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#8b5cf6" />
                <stop offset="100%" stop-color="#6d28d9" />
            </linearGradient>
            <filter id="glow-oir" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="4" result="blur" />
                <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
        </defs>
        <rect width="100%" height="100%" fill="#0f172a" rx="12"/>
        <g transform="translate(30, 15)">
            <!-- Isometric Cube representing spatial testing -->
            <polygon points="60,15 95,32 60,50 25,32" fill="none" stroke="url(#oir-grad)" stroke-width="3.5" filter="url(#glow-oir)"/>
            <polygon points="25,32 60,50 60,95 25,77" fill="none" stroke="url(#oir-grad)" stroke-width="3.5" filter="url(#glow-oir)"/>
            <polygon points="60,50 95,32 95,77 60,95" fill="none" stroke="url(#oir-grad)" stroke-width="3.5" filter="url(#glow-oir)"/>
            <!-- Verbal letter details overlay -->
            <text x="50" y="38" font-family="'Outfit', sans-serif" font-size="12" fill="#c084fc" font-weight="bold">A</text>
            <text x="35" y="65" font-family="'Outfit', sans-serif" font-size="12" fill="#c084fc" font-weight="bold">B</text>
            <text x="75" y="65" font-family="'Outfit', sans-serif" font-size="12" fill="#c084fc" font-weight="bold">C</text>
        </g>
        <!-- Title Text -->
        <text x="170" y="60" font-family="'Outfit', 'Inter', sans-serif" font-size="28" font-weight="bold" fill="#ffffff">OIR Practice Exam</text>
        <text x="170" y="90" font-family="'Inter', sans-serif" font-size="14" fill="#94a3b8">Officer Intelligence Rating practice - Verbal & Non-Verbal timed sprints</text>
    </svg>
    """

def get_lecturette_logo():
    return """
    <svg width="100%" height="130" viewBox="0 0 600 130" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="lect-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#f43f5e" />
                <stop offset="100%" stop-color="#e11d48" />
            </linearGradient>
            <filter id="glow-lect" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="4" result="blur" />
                <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
        </defs>
        <rect width="100%" height="100%" fill="#0f172a" rx="12"/>
        <g transform="translate(30, 15)">
            <!-- Speaking podium / lectern -->
            <path d="M 30 100 L 45 40 L 75 40 L 90 100 Z" fill="none" stroke="url(#lect-grad)" stroke-width="4" filter="url(#glow-lect)"/>
            <!-- Podium Mic -->
            <path d="M 50 40 L 50 22 C 50 20 60 15 65 18" fill="none" stroke="#fda4af" stroke-width="3" stroke-linecap="round"/>
            <circle cx="67" cy="18" r="3" fill="#fda4af"/>
            <!-- Star Spotlight Spark -->
            <path d="M 60 48 L 60 92" stroke="url(#lect-grad)" stroke-width="2" opacity="0.6"/>
            <polygon points="60,50 63,58 72,60 63,62 60,70 57,62 48,60 57,58" fill="#fda4af"/>
        </g>
        <!-- Title Text -->
        <text x="170" y="60" font-family="'Outfit', 'Inter', sans-serif" font-size="28" font-weight="bold" fill="#ffffff">GTO Lecturette</text>
        <text x="170" y="90" font-family="'Inter', sans-serif" font-size="14" fill="#94a3b8">3-Minute chit prep, 5-minute speaking delivery & self-grading rubric</text>
    </svg>
    """

def get_dashboard_logo():
    return """
    <svg width="100%" height="130" viewBox="0 0 600 130" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="dash-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#0ea5e9" />
                <stop offset="100%" stop-color="#2563eb" />
            </linearGradient>
            <filter id="glow-dash" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="4" result="blur" />
                <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
        </defs>
        <rect width="100%" height="100%" fill="#0f172a" rx="12"/>
        <g transform="translate(30, 15)">
            <!-- Dashboard gauge/dial -->
            <path d="M 20 80 C 20 30 100 30 100 80" fill="none" stroke="url(#dash-grad)" stroke-width="4.5" stroke-linecap="round" filter="url(#glow-dash)"/>
            <!-- Dial needle -->
            <line x1="60" y1="80" x2="85" y2="45" stroke="#7dd3fc" stroke-width="4" stroke-linecap="round"/>
            <circle cx="60" cy="80" r="8" fill="#7dd3fc"/>
            <!-- Small Bar chart detail inside -->
            <rect x="25" y="85" width="12" height="15" fill="#0ea5e9" rx="2"/>
            <rect x="42" y="85" width="12" height="25" fill="#0ea5e9" rx="2"/>
            <rect x="59" y="85" width="12" height="35" fill="#0ea5e9" rx="2"/>
            <rect x="76" y="85" width="12" height="20" fill="#0ea5e9" rx="2"/>
        </g>
        <!-- Title Text -->
        <text x="170" y="60" font-family="'Outfit', 'Inter', sans-serif" font-size="28" font-weight="bold" fill="#ffffff">Psychological & Performance Dashboard</text>
        <text x="170" y="90" font-family="'Inter', sans-serif" font-size="14" fill="#94a3b8">Monitor overall sentiment trends, confidence ratings, and officer-like traits</text>
    </svg>
    """

def get_main_app_logo():
    return """
    <svg width="100%" height="150" viewBox="0 0 800 150" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="shield-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#3b82f6" />
                <stop offset="50%" stop-color="#10b981" />
                <stop offset="100%" stop-color="#1d4ed8" />
            </linearGradient>
            <filter id="shield-glow" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="6" result="blur" />
                <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
        </defs>
        <rect width="100%" height="100%" fill="#0f172a" rx="16" stroke="rgba(255, 255, 255, 0.05)" stroke-width="1.5"/>
        
        <!-- Large Shield Emblem with Star -->
        <g transform="translate(45, 15)">
            <!-- Outer Shield -->
            <path d="M 30 10 Q 60 10 90 20 Q 90 70 60 100 Q 30 70 30 20 Z" fill="none" stroke="url(#shield-grad)" stroke-width="4.5" filter="url(#shield-glow)"/>
            <!-- Inner Shield Accent -->
            <path d="M 38 20 Q 60 20 82 28 Q 82 66 60 90 Q 38 66 38 28 Z" fill="none" stroke="#10b981" stroke-width="1.5" opacity="0.6"/>
            <!-- Center Star -->
            <polygon points="60,35 64,48 76,48 66,56 70,69 60,60 50,69 54,56 44,48 56,48" fill="#3b82f6"/>
            <circle cx="60" cy="52" r="3" fill="#ffffff"/>
            <!-- Laurel leaves under star -->
            <path d="M 45 75 Q 60 85 75 75" fill="none" stroke="#10b981" stroke-width="2.5" stroke-linecap="round"/>
        </g>
        
        <!-- Title Text -->
        <text x="175" y="65" font-family="'Outfit', 'Inter', sans-serif" font-size="36" font-weight="900" fill="#ffffff" letter-spacing="2">COMMANDER'S ARCH</text>
        <text x="175" y="98" font-family="'Inter', sans-serif" font-size="16" font-weight="700" fill="#10b981" letter-spacing="4">SSB PREPARATION SUITE</text>
        <text x="175" y="122" font-family="'Inter', sans-serif" font-size="12" fill="#64748b">Unified Cognitive & Psychological Assessment Platforms</text>
    </svg>
    """
