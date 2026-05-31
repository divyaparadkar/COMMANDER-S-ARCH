# Data Bank for WAT (Word Association Test) and SRT (Situation Reaction Test)

WAT_WORDS = [
    "Cooperate", "Fear", "Responsibility", "Difficult", "Society",
    "Stamina", "System", "Enemy", "Mistake", "Success",
    "Danger", "Organise", "Initiative", "Defeat", "Influence",
    "Liveliness", "Courage", "Struggle", "Lead", "Agree",
    "Duty", "Team", "Solve", "Risk", "Decision",
    "Justice", "Character", "Determine", "Active", "Obedient",
    "Honest", "Future", "Youth", "Friend", "Progress",
    "Discipline", "Country", "Work", "Challenge", "Goal",
    "Help", "Support", "Plan", "Improve", "Happy",
    "Love", "Respect", "Peace", "Knowledge", "Confidence",
    "Unity", "Inspire", "Grow", "Time", "Action",
    "Change", "Adapt", "Strong", "Patience", "Victory"
]

SRT_SITUATIONS = [
    {
        "id": 1,
        "situation": "He was on his way to an important job interview when he saw a child hit by a speeding vehicle and bleeding heavily. What did he do?"
    },
    {
        "id": 2,
        "situation": "While traveling by train, he noticed two suspicious persons handing over a package to each other and whispering about a bomb. What did he do?"
    },
    {
        "id": 3,
        "situation": "He was the captain of the football team. Just before the final match, three key players fell ill, and the opponent team was very strong. What did he do?"
    },
    {
        "id": 4,
        "situation": "In a forest camp at night, his companion was bitten by a poisonous snake and there was no doctor or vehicle nearby. What did he do?"
    },
    {
        "id": 5,
        "situation": "His parents wanted him to marry a girl of their choice, but he had already decided to marry another girl whom he loved. What did he do?"
    },
    {
        "id": 6,
        "situation": "He was camping in the mountains when a sudden cloudburst triggered a landslide, blocking their return route and injuring two members. What did he do?"
    },
    {
        "id": 7,
        "situation": "He found that the treasurer of his college club was misappropriating funds, but the treasurer was a close friend of the college principal. What did he do?"
    },
    {
        "id": 8,
        "situation": "He was walking alone in a dark alley at night when three armed dacoits surrounded him and demanded his money and watch. What did he do?"
    },
    {
        "id": 9,
        "situation": "During a group discussion, he found that his group mates were shouting and not letting anyone speak, and the coordinator was observing closely. What did he do?"
    },
    {
        "id": 10,
        "situation": "He had worked hard for an exam but failed to qualify, and his family was disappointed. What did he do?"
    },
    {
        "id": 11,
        "situation": "His boat capsized in the middle of a river while he was boating with two friends who did not know how to swim. What did he do?"
    },
    {
        "id": 12,
        "situation": "He saw a fire breaking out in the neighboring house at midnight while everyone was asleep. What did he do?"
    },
    {
        "id": 13,
        "situation": "A communal tension broke out in his town, and rumors started spreading rapidly on social media. What did he do?"
    },
    {
        "id": 14,
        "situation": "He was assigned to lead a team for a village development project, but the villagers were hostile and refused to cooperate. What did he do?"
    },
    {
        "id": 15,
        "situation": "He was travelling in a bus when a group of eve-teasers started misbehaving with a girl passenger, and other passengers remained silent. What did he do?"
    },
    {
        "id": 16,
        "situation": "His senior officer gave him an order which he knew would lead to a heavy financial loss for the organization. What did he do?"
    },
    {
        "id": 17,
        "situation": "He lost his wallet containing important ID cards, debit cards, and cash in a new city where he did not know anyone. What did he do?"
    },
    {
        "id": 18,
        "situation": "He was appointed the manager of a project that was running behind schedule and facing a severe budget crunch. What did he do?"
    },
    {
        "id": 19,
        "situation": "He noticed that his younger brother had fallen into bad company and started smoking and bunking classes. What did he do?"
    },
    {
        "id": 20,
        "situation": "While trekking, he got separated from his team in a dense fog without any network signal on his mobile phone. What did he do?"
    },
    {
        "id": 21,
        "situation": "He wanted to start a new business venture, but his family was completely against taking the risk and wanted him to take a stable job. What did he do?"
    },
    {
        "id": 22,
        "situation": "A junior colleague of his made a critical error in a presentation to the client, and the boss blamed him for poor supervision. What did he do?"
    },
    {
        "id": 23,
        "situation": "He saw his neighbor beating his wife brutally in public. What did he do?"
    },
    {
        "id": 24,
        "situation": "He was traveling to an exam center and got stuck in a massive traffic jam with only 15 minutes left for the exam to start. What did he do?"
    },
    {
        "id": 25,
        "situation": "During a heavy flood in his area, the drinking water supply was contaminated, and diseases started spreading. What did he do?"
    },
    {
        "id": 26,
        "situation": "He was selected for a prestigious training course abroad, but his mother fell seriously ill just a day before his departure. What did he do?"
    },
    {
        "id": 27,
        "situation": "He discovered that his roommate was secretly using drugs in the hostel. What did he do?"
    },
    {
        "id": 28,
        "situation": "He was leading a trekking party when they encountered a wild bear blocking their path. What did he do?"
    },
    {
        "id": 29,
        "situation": "His father faced a sudden business setback and could not afford to pay his college tuition fees. What did he do?"
    },
    {
        "id": 30,
        "situation": "He went to a restaurant and after having his meal, he realized that he had forgotten his wallet and phone at home. What did he do?"
    }
]

INTERVIEW_QUESTIONS = {
    "Personal & PIQ-based": [
        "Can you introduce yourself and tell me about the key highlights of your Personal Information Questionnaire (PIQ)?",
        "Why do you want to join the Armed Forces, and what specific preparation have you done for this attempt?",
        "What are your three biggest strengths and three weaknesses, and how are you working to overcome your weaknesses?",
        "Tell me about a time when you had a disagreement with your parents or close friends. How did you resolve it?",
        "How do you spend your free time? What hobbies or extra-curricular activities are you passionately involved in?",
        "Describe your relationship with your siblings and parents. Who are you closest to, and why?"
    ],
    "Situation & OLQ-based": [
        "If you are selected to lead a rescue team during a sudden flood in a remote village, how will you organize your team and resources?",
        "Describe a situation in your life where you had to make a very quick, high-stakes decision. What was the outcome?",
        "If you discover that one of your team members is leaking confidential project details to a rival team, how will you handle the situation?",
        "How do you handle criticism or failure? Share a specific instance where you failed to achieve a goal and how you dealt with it.",
        "If you are assigned a task under a boss who is very difficult to work with and constantly rejects your ideas, what would you do?",
        "Tell me about a time you took the initiative to start something new in your college or workplace. What challenges did you face?"
    ],
    "Current Affairs & General Knowledge": [
        "What is your opinion on the impact of Artificial Intelligence and automation on future job markets, particularly in developing nations?",
        "Can you discuss a recent geopolitical conflict or international event and analyze its strategic implications for India's national security?",
        "What are the major internal security challenges India is currently facing, and what steps do you suggest to address them?",
        "Explain the concept of renewable energy transition. What are the key bottlenecks in shifting fully to green energy?",
        "What is your view on the privatization of public sector undertakings? Do you think it helps or hinders economic development?",
        "Discuss the significance of space exploration programs (like Chandrayaan/Gaganyaan) for a developing country's technology and economy."
    ]
}

OIR_VERBAL_QUESTIONS = [
    {
        "id": 1,
        "type": "Coding-Decoding",
        "question": "If BOMBAY is coded as MYMYMY, what is the code for TAMILNADU?",
        "options": ["TIATIATIA", "ALNALNALN", "MNUMNUMNU", "MNUMNUMUN"],
        "answer": "MNUMNUMNU",
        "explanation": "The letters at position 3 and 6 (M and Y) are repeated thrice. For TAMILNADU, position 3, 6, 9 are M, N, U. Repeating them gives MNUMNUMNU."
    },
    {
        "id": 2,
        "type": "Odd One Out",
        "question": "Choose the word which is least like the other words in the group.",
        "options": ["Copper", "Zinc", "Brass", "Aluminum"],
        "answer": "Brass",
        "explanation": "Brass is an alloy, while all others are pure metals."
    },
    {
        "id": 3,
        "type": "Synonyms & Antonyms",
        "question": "Choose the word that is most nearly opposite in meaning to EMANCIPATE.",
        "options": ["Liberate", "Enslave", "Absolve", "Exonerate"],
        "answer": "Enslave",
        "explanation": "Emancipate means to set free. Its opposite is to enslave."
    },
    {
        "id": 4,
        "type": "Blood Relations",
        "question": "Pointing to a photograph, Amit said, 'I have no brother or sister but that man's father is my father's son.' Whose photograph was it?",
        "options": ["His Father's", "His Son's", "His Uncle's", "His Cousin's"],
        "answer": "His Son's",
        "explanation": "Amit has no brother or sister. So, 'my father's son' is Amit himself. Therefore, the man in the photograph's father is Amit, meaning it is Amit's son's photo."
    },
    {
        "id": 5,
        "type": "Direction Sense",
        "question": "A man walks 4 km North, then turns right and walks 3 km. How far is he from his starting point?",
        "options": ["5 km", "7 km", "1 km", "12 km"],
        "answer": "5 km",
        "explanation": "Applying Pythagoras theorem: Distance = sqrt(4^2 + 3^2) = sqrt(16 + 9) = sqrt(25) = 5 km."
    },
    {
        "id": 6,
        "type": "Number Series",
        "question": "Complete the missing term in the sequence: 2, 6, 12, 20, 30, ?",
        "options": ["36", "42", "40", "44"],
        "answer": "42",
        "explanation": "The differences between consecutive terms are +4, +6, +8, +10, so the next difference is +12. 30 + 12 = 42."
    },
    {
        "id": 7,
        "type": "Alphabet Series",
        "question": "Find the next alphabet in the series: A, C, F, J, O, ?",
        "options": ["T", "U", "V", "W"],
        "answer": "U",
        "explanation": "The positions of characters are 1 (+2) -> 3 (+3) -> 6 (+4) -> 10 (+5) -> 15 (+6) -> 21. The 21st letter is U."
    },
    {
        "id": 8,
        "type": "Jumbled Words",
        "question": "Rearrange the jumbled letters 'O N T E M N T I C' to form a word. What category does it belong to?",
        "options": ["A Country", "A Continent", "An Ocean", "A Mountain Range"],
        "answer": "A Continent",
        "explanation": "The letters rearrange to form the word 'CONTINENT'."
    },
    {
        "id": 9,
        "type": "Dictionary Rank",
        "question": "Arrange the following words in alphabetical order: 1. Absolute, 2. Ability, 3. Abandon, 4. Abstract.",
        "options": ["3, 2, 1, 4", "3, 1, 2, 4", "2, 3, 1, 4", "3, 2, 4, 1"],
        "answer": "3, 2, 1, 4",
        "explanation": "Alphabetical sorting order: Abandon (3) -> Ability (2) -> Absolute (1) -> Abstract (4)."
    },
    {
        "id": 10,
        "type": "Odd One Out",
        "question": "Spot the number that does not fit the mathematical pattern.",
        "options": ["27", "64", "125", "144"],
        "answer": "144",
        "explanation": "27 (3^3), 64 (4^3), and 125 (5^3) are perfect cubes, whereas 144 (12^2) is a perfect square."
    },
    {
        "id": 11,
        "type": "Verbal Analogy",
        "question": "Light is to Darkness as Knowledge is to ________.",
        "options": ["Wisdom", "Ignorance", "Books", "Intelligence"],
        "answer": "Ignorance",
        "explanation": "Light removes Darkness, and Knowledge removes Ignorance."
    },
    {
        "id": 12,
        "type": "Jumbled Sentences",
        "question": "Rearrange: 'bites / dog / a / barking / seldom'. What is the meaning of the resulting proverb?",
        "options": ["Barking dogs are dangerous", "Those who threaten rarely act", "Dogs bite everyone", "Actions speak louder than words"],
        "answer": "Those who threaten rarely act",
        "explanation": "The rearranged sentence is 'A barking dog seldom bites', which means people who make loud threats rarely take action."
    }
]

OIR_NON_VERBAL_QUESTIONS = [
    {
        "id": 1,
        "type": "Cube & Dice Counting",
        "question": "How many blocks make up this 3D stair structure?",
        "svg": """
        <svg width="200" height="150" viewBox="0 0 200 150" style="display:block; margin:auto;">
          <!-- Column 1 (height 3) -->
          <polygon points="30,50 50,40 70,50 50,60" fill="#60a5fa" stroke="#1e3a8a" stroke-width="1.5"/>
          <polygon points="30,50 50,60 50,130 30,120" fill="#2563eb" stroke="#1e3a8a" stroke-width="1.5"/>
          
          <!-- Column 2 (height 2) -->
          <polygon points="70,70 90,60 110,70 90,80" fill="#60a5fa" stroke="#1e3a8a" stroke-width="1.5"/>
          <polygon points="70,70 90,80 90,130 70,120" fill="#2563eb" stroke="#1e3a8a" stroke-width="1.5"/>
          <polygon points="90,80 110,70 110,120 90,130" fill="#1d4ed8" stroke="#1e3a8a" stroke-width="1.5"/>

          <!-- Column 3 (height 1) -->
          <polygon points="110,90 130,80 150,90 130,100" fill="#93c5fd" stroke="#1e3a8a" stroke-width="1.5"/>
          <polygon points="110,90 130,100 130,130 110,120" fill="#3b82f6" stroke="#1e3a8a" stroke-width="1.5"/>
          <polygon points="130,100 150,90 150,120 130,130" fill="#1d4ed8" stroke="#1e3a8a" stroke-width="1.5"/>
        </svg>
        """,
        "options": ["4", "5", "6", "8"],
        "answer": "6",
        "explanation": "Column 1 has 3 stacked blocks, Column 2 has 2, and Column 3 has 1 block. Total = 3 + 2 + 1 = 6 blocks."
    },
    {
        "id": 2,
        "type": "Pattern Completion",
        "question": "Which of the options completes the missing lower-right quadrant?",
        "svg": """
        <svg width="200" height="200" viewBox="0 0 200 200" style="display:block; margin:auto; background:#1e293b; border:2px solid #475569;">
          <!-- Quadrant dividers -->
          <line x1="100" y1="0" x2="100" y2="200" stroke="#475569" stroke-width="2"/>
          <line x1="0" y1="100" x2="200" y2="100" stroke="#475569" stroke-width="2"/>
          <!-- Top Left -->
          <circle cx="100" cy="100" r="80" fill="none" stroke="#60a5fa" stroke-width="3" stroke-dasharray="0 120 120"/>
          <line x1="100" y1="100" x2="20" y2="20" stroke="#38bdf8" stroke-width="3"/>
          <!-- Top Right -->
          <circle cx="100" cy="100" r="80" fill="none" stroke="#60a5fa" stroke-width="3" stroke-dasharray="120 0 120"/>
          <line x1="100" y1="100" x2="180" y2="20" stroke="#38bdf8" stroke-width="3"/>
          <!-- Bottom Left -->
          <circle cx="100" cy="100" r="80" fill="none" stroke="#60a5fa" stroke-width="3" stroke-dasharray="120 120 0"/>
          <line x1="100" y1="100" x2="20" y2="180" stroke="#38bdf8" stroke-width="3"/>
          <!-- Bottom Right (Missing) -->
          <rect x="110" y="110" width="80" height="80" fill="#334155" rx="5"/>
          <text x="140" y="155" fill="#94a3b8" font-size="24" font-weight="bold">?</text>
        </svg>
        """,
        "options": ["Diagonal line pointing outward & corner arc", "Vertical line & horizontal line", "Full shaded square", "Empty quadrant"],
        "answer": "Diagonal line pointing outward & corner arc",
        "explanation": "To maintain symmetrical balance, the bottom-right quadrant must contain a diagonal line going from center to bottom-right corner and a corresponding quadrant arc of the main circle."
    },
    {
        "id": 3,
        "type": "Figure Classification (Odd One Out)",
        "question": "Identify the figure that does NOT fit the classification rule.",
        "svg": """
        <svg width="320" height="100" viewBox="0 0 320 100" style="display:block; margin:auto;">
          <!-- Fig A -->
          <rect x="10" y="10" width="60" height="60" fill="none" stroke="#f43f5e" stroke-width="2.5"/>
          <line x1="10" y1="10" x2="70" y2="70" stroke="#f43f5e" stroke-width="2.5"/>
          <line x1="70" y1="10" x2="10" y2="70" stroke="#f43f5e" stroke-width="2.5"/>
          <text x="35" y="90" fill="#94a3b8" font-weight="bold">A</text>

          <!-- Fig B -->
          <rect x="90" y="10" width="60" height="60" fill="none" stroke="#f43f5e" stroke-width="2.5"/>
          <line x1="90" y1="40" x2="150" y2="40" stroke="#f43f5e" stroke-width="2.5"/>
          <line x1="120" y1="10" x2="120" y2="70" stroke="#f43f5e" stroke-width="2.5"/>
          <text x="115" y="90" fill="#94a3b8" font-weight="bold">B</text>

          <!-- Fig C -->
          <rect x="170" y="10" width="60" height="60" fill="none" stroke="#f43f5e" stroke-width="2.5"/>
          <line x1="170" y1="10" x2="230" y2="70" stroke="#f43f5e" stroke-width="2.5"/>
          <text x="195" y="90" fill="#94a3b8" font-weight="bold">C</text>

          <!-- Fig D -->
          <rect x="250" y="10" width="60" height="60" fill="none" stroke="#f43f5e" stroke-width="2.5"/>
          <line x1="250" y1="10" x2="310" y2="70" stroke="#f43f5e" stroke-width="2.5"/>
          <line x1="310" y1="10" x2="250" y2="70" stroke="#f43f5e" stroke-width="2.5"/>
          <text x="275" y="90" fill="#94a3b8" font-weight="bold">D</text>
        </svg>
        """,
        "options": ["A", "B", "C", "D"],
        "answer": "C",
        "explanation": "Figures A, B, and D are divided into 4 equal segments by two intersecting lines. Figure C has only one dividing line and has 2 segments."
    },
    {
        "id": 4,
        "type": "Series Continuation",
        "question": "Which direction will the arrow point in the next step of the sequence?",
        "svg": """
        <svg width="300" height="80" viewBox="0 0 300 80" style="display:block; margin:auto; background:#1e293b; border-radius:8px;">
          <!-- Clock 1: Arrow pointing North (90deg) -->
          <circle cx="40" cy="40" r="30" fill="none" stroke="#475569" stroke-width="2"/>
          <line x1="40" y1="40" x2="40" y2="15" stroke="#10b981" stroke-width="3" marker-end="url(#arrow)"/>
          <circle cx="40" cy="40" r="4" fill="#10b981"/>
          
          <!-- Clock 2: Arrow pointing Northeast (45deg) -->
          <circle cx="120" cy="40" r="30" fill="none" stroke="#475569" stroke-width="2"/>
          <line x1="120" y1="40" x2="140" y2="20" stroke="#10b981" stroke-width="3"/>
          <circle cx="120" cy="40" r="4" fill="#10b981"/>

          <!-- Clock 3: Arrow pointing East (0deg) -->
          <circle cx="200" cy="40" r="30" fill="none" stroke="#475569" stroke-width="2"/>
          <line x1="200" y1="40" x2="225" y2="40" stroke="#10b981" stroke-width="3"/>
          <circle cx="200" cy="40" r="4" fill="#10b981"/>

          <!-- Next Box -->
          <rect x="250" y="10" width="40" height="60" fill="#334155" rx="4"/>
          <text x="265" y="45" fill="#94a3b8" font-size="20">?</text>
        </svg>
        """,
        "options": ["Southeast", "South", "Southwest", "Northwest"],
        "answer": "Southeast",
        "explanation": "The arrow rotates clockwise by 45 degrees in each step. North -> Northeast -> East -> Southeast."
    },
    {
        "id": 5,
        "type": "Paper Folding & Cutting",
        "question": "A square paper is folded diagonally, and then a circle hole is punched in it. What does it look like unfolded?",
        "svg": """
        <svg width="250" height="100" viewBox="0 0 250 100" style="display:block; margin:auto;">
          <!-- Folded State -->
          <rect x="20" y="20" width="60" height="60" fill="none" stroke="#e2e8f0" stroke-width="2"/>
          <line x1="20" y1="20" x2="80" y2="80" stroke="#94a3b8" stroke-dasharray="4 4"/>
          <circle cx="40" cy="60" r="6" fill="#ef4444"/>

          <!-- Unfolded Option mockup -->
          <rect x="150" y="20" width="60" height="60" fill="none" stroke="#e2e8f0" stroke-width="2"/>
          <circle cx="170" cy="60" r="6" fill="#38bdf8"/>
          <circle cx="190" cy="40" r="6" fill="#38bdf8"/>
        </svg>
        """,
        "options": ["Two symmetrical holes across the diagonal fold", "One single hole", "Four holes (one in each corner)", "No holes"],
        "answer": "Two symmetrical holes across the diagonal fold",
        "explanation": "Unfolding the diagonal crease will mirror the punched hole on the opposite side of the diagonal fold line, producing exactly two symmetrical holes."
    },
    {
        "id": 6,
        "type": "Dice Opposition Test",
        "question": "In a standard six-sided dice, what number lies directly opposite to the face with 3 dots?",
        "svg": """
        <svg width="150" height="100" viewBox="0 0 150 100" style="display:block; margin:auto;">
          <!-- Isometric Cube representing Dice -->
          <polygon points="75,20 115,35 75,50 35,35" fill="#f8fafc" stroke="#475569" stroke-width="2"/>
          <polygon points="35,35 75,50 75,90 35,75" fill="#f1f5f9" stroke="#475569" stroke-width="2"/>
          <polygon points="75,50 115,35 115,75 75,90" fill="#e2e8f0" stroke="#475569" stroke-width="2"/>
          
          <!-- Top face (3 dots) -->
          <circle cx="55" cy="30" r="3" fill="#0f172a"/>
          <circle cx="75" cy="35" r="3" fill="#0f172a"/>
          <circle cx="95" cy="40" r="3" fill="#0f172a"/>

          <!-- Left face (1 dot) -->
          <circle cx="55" cy="62" r="3" fill="#0f172a"/>

          <!-- Right face (2 dots) -->
          <circle cx="90" cy="60" r="3" fill="#0f172a"/>
          <circle cx="100" cy="70" r="3" fill="#0f172a"/>
        </svg>
        """,
        "options": ["4", "5", "6", "2"],
        "answer": "4",
        "explanation": "In any standard dice, the sum of opposite faces is always equal to 7. Therefore, the face opposite to 3 is 7 - 3 = 4."
    }
]

LECTURETTE_TOPICS = {
    "High / National Affairs": [
        "The Uniform Civil Code (UCC): Implementation challenges, regional perspectives, and social impact.",
        "One Nation, One Election: Feasibility, constitutional amendments required, and democratic pros/cons.",
        "India's Semiconductor Mission: Progress in local manufacturing, global supply chain positioning, and bottlenecks.",
        "Internal Security & Left-Wing Extremism: Current status, government development strategies, and remaining challenges."
    ],
    "Medium / International Relations": [
        "The Changing Dynamics of the Global South: India's leadership role, economic shifts, and strategic autonomy.",
        "The Indo-Pacific Geopolitics: The Quad, countering maritime assertions, and freedom of navigation.",
        "Global Refugee & Migration Crises: Economic impacts on host nations, border security, and humanitarian concerns.",
        "The Rise of Alternative Currencies: De-dollarization trends, BRICS payment systems, and digital currencies in global trade."
    ],
    "Low / Technology & Innovation": [
        "Generative AI Regulation & Ethics: Balancing deepfakes, intellectual property rights, and national security risks.",
        "The Militarization of Space: Anti-satellite weapons, space debris, and the role of defense space agencies.",
        "Quantum Computing: The next geopolitical race, cybersecurity threats, and cryptographic vulnerabilities.",
        "Renewable Energy Grid Integration: Green Hydrogen, solid-state batteries, and the logistics of transitioning away from fossil fuels."
    ],
    "General / Object-based": [
        "Value of Discipline in Armed Forces",
        "Role of Youth in Nation Building",
        "Impact of Social Media on Mental Health",
        "Tourism in India: Growth, challenges, and cultural diplomacy"
    ]
}


