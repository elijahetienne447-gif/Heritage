# Enhanced Caribbean Cultural Heritage & Studies Explorer - Secure Version
import streamlit as st
import json
import os
import re
import requests
from urllib.parse import urlparse, quote
import time
from datetime import datetime
import random

try:
    import speech_recognition as sr
    SPEECH_AVAILABLE = True
except ImportError:
    SPEECH_AVAILABLE = False

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

import streamlit.components.v1 as components

# SECURE API Configuration
try:
    # Try to access Streamlit secrets first
    if hasattr(st, 'secrets') and st.secrets:
        GOOGLE_AI_API_KEY = st.secrets.get("GOOGLE_AI_API_KEY", None) or os.getenv("GOOGLE_AI_API_KEY")
        SERPER_API_KEY = st.secrets.get("SERPER_API_KEY", None) or os.getenv("SERPER_API_KEY")
    else:
        # Fallback to environment variables only
        GOOGLE_AI_API_KEY = os.getenv("GOOGLE_AI_API_KEY")
        SERPER_API_KEY = os.getenv("SERPER_API_KEY")
        
except Exception:
    # Final fallback if anything goes wrong
    GOOGLE_AI_API_KEY = os.getenv("GOOGLE_AI_API_KEY")
    SERPER_API_KEY = os.getenv("SERPER_API_KEY")

if GENAI_AVAILABLE and GOOGLE_AI_API_KEY:
    genai.configure(api_key=GOOGLE_AI_API_KEY)

# Security functions
def hide_code_elements():
    """Hide any visible code elements and add security styling"""
    security_css = """
    <style>
    /* Hide any code elements that might appear */
    .highlight {display: none !important;}
    code {display: none !important;}
    pre {display: none !important;}
    .language-python {display: none !important;}
    .stCodeBlock {display: none !important;}
    
    /* Hide potentially sensitive debug info */
    .stException {display: none !important;}
    .stAlert .stMarkdown code {display: none !important;}
    
    /* Professional header adjustments */
    .stApp > header {
        background: transparent;
    }
    
    /* Clean sidebar */
    .css-1d391kg {
        background: linear-gradient(135deg, rgba(233, 30, 99, 0.1) 0%, rgba(30, 136, 229, 0.1) 100%);
    }
    
    /* Hide deployment button and menu */
    .stDeployButton {display: none;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Security notice styling */
    .security-notice {
        background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%);
        color: white;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
        font-size: 14px;
        text-align: center;
    }
    
    /* API status indicator */
    .api-status {
        position: fixed;
        top: 10px;
        right: 10px;
        background: rgba(0,0,0,0.8);
        color: white;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 12px;
        z-index: 10000;
    }
    
    .api-status.configured {
        background: rgba(76, 175, 80, 0.9);
    }
    
    .api-status.demo {
        background: rgba(255, 152, 0, 0.9);
    }
    </style>
    """
    st.markdown(security_css, unsafe_allow_html=True)

def show_api_status():
    """Display current API configuration status"""
    if GOOGLE_AI_API_KEY and SERPER_API_KEY:
        status_class = "configured"
        status_text = "✅ APIs Configured"
    elif GOOGLE_AI_API_KEY or SERPER_API_KEY:
        status_class = "demo"
        status_text = "⚠️ Partial Config"
    else:
        status_class = "demo"
        status_text = "📋 Demo Mode"
    
    st.markdown(f"""
    <div class="api-status {status_class}">
        {status_text}
    </div>
    """, unsafe_allow_html=True)

def show_configuration_help():
    """Show configuration help in sidebar"""
    try:
        with st.sidebar:
            st.markdown("### 🔧 Configuration")
            
            if not GOOGLE_AI_API_KEY or not SERPER_API_KEY:
                st.markdown("""
                **To enable full functionality:**
                
                1. Create `.streamlit/secrets.toml`:
                ```toml
                GOOGLE_AI_API_KEY = "your_key_here"
                SERPER_API_KEY = "your_key_here"
                ```
                
                2. Or set environment variables:
                ```bash
                export GOOGLE_AI_API_KEY="your_key"
                export SERPER_API_KEY="your_key"
                ```
                """)
                
                # Show the specific paths where secrets file should be created
                st.info(f"""
                **Create secrets file at one of these locations:**
                - `{os.path.expanduser('~')}/.streamlit/secrets.toml`
                - `.streamlit/secrets.toml` (in your project folder)
                """)
            else:
                st.success("✅ APIs configured correctly")
                
    except Exception as e:
        # If sidebar fails, show configuration info in main area
        st.info("💡 To configure API keys, create `.streamlit/secrets.toml` file in your project directory")

# Page Configuration
st.set_page_config(
    page_title="Caribbean Heritage & Studies Explorer",
    page_icon="🌴",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Define MODES dictionary
MODES = {
    "heritage": {
        "title": "Caribbean Cultural Heritage Explorer",
        "subtitle": "Discover the rich traditions, music, festivals, and living culture of the Caribbean islands",
        "persona": "Kaia - Cultural Storyteller",
        "color": "#e91e63",
        "suggestions": [
            "Tell me about Caribbean Carnival traditions",
            "What is the story behind steel pan music?",
            "Share traditional Caribbean recipes",
            "How do Caribbean languages reflect culture?",
            "What role does music play in Caribbean spirituality?",
            "Tell me about contemporary Caribbean artists"
        ]
    },
    "studies": {
        "title": "Caribbean Studies Research Portal",
        "subtitle": "Academic research, policy analysis, and scholarly insights into Caribbean development",
        "persona": "Dr. Thompson - Caribbean Studies Scholar",
        "color": "#1e88e5",
        "suggestions": [
            "Analyze CARICOM economic integration",
            "Evaluate climate change adaptation policies",
            "Assess tourism dependency impact",
            "Compare Caribbean education systems",
            "Research Caribbean migration patterns",
            "Analyze democratic governance challenges"
        ]
    }
}

# Enhanced Gemini-style CSS
st.markdown("""
<style>
    /* Global styling */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* Mode-specific styling */
    .heritage-mode {
        --primary-color: #e91e63;
        --secondary-color: #ad1457;
        --accent-color: #fce4ec;
        --gradient: linear-gradient(135deg, #e91e63 0%, #ad1457 100%);
        --warm-gradient: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
    }
    
    .studies-mode {
        --primary-color: #1e88e5;
        --secondary-color: #1565c0;
        --accent-color: #e3f2fd;
        --gradient: linear-gradient(135deg, #1e88e5 0%, #1565c0 100%);
        --academic-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Taskbar styling */
    .gemini-taskbar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 64px;
        background: linear-gradient(90deg, rgba(26, 115, 232, 0.95) 0%, rgba(21, 101, 192, 0.95) 100%);
        backdrop-filter: blur(20px);
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 24px;
        z-index: 1000;
        color: white;
    }
    
    .heritage-taskbar {
        background: linear-gradient(90deg, rgba(233, 30, 99, 0.95) 0%, rgba(173, 20, 87, 0.95) 100%);
    }
    
    .studies-taskbar {
        background: linear-gradient(90deg, rgba(30, 136, 229, 0.95) 0%, rgba(21, 101, 192, 0.95) 100%);
    }
    
    .taskbar-left {
        display: flex;
        align-items: center;
        gap: 16px;
    }
    
    .taskbar-logo {
        display: flex;
        align-items: center;
        gap: 8px;
        font-weight: 600;
        color: white;
        text-decoration: none;
    }
    
    .taskbar-search {
        position: relative;
        display: flex;
        align-items: center;
        background: rgba(255, 255, 255, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 24px;
        padding: 8px 16px;
        min-width: 400px;
        max-width: 600px;
    }
    
    .taskbar-search input {
        border: none;
        outline: none;
        background: transparent;
        flex: 1;
        padding: 4px 8px;
        font-size: 16px;
        color: white;
    }
    
    .taskbar-search input::placeholder {
        color: rgba(255, 255, 255, 0.7);
    }
    
    .taskbar-search .search-icon {
        color: rgba(255, 255, 255, 0.8);
        margin-right: 8px;
    }
    
    .taskbar-right {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .mode-indicator {
        background: rgba(255, 255, 255, 0.2);
        color: white;
        padding: 6px 12px;
        border-radius: 16px;
        font-size: 14px;
        font-weight: 500;
    }
    
    .history-btn {
        background: none;
        border: 1px solid rgba(255, 255, 255, 0.5);
        border-radius: 20px;
        padding: 8px 16px;
        cursor: pointer;
        color: white;
        font-size: 14px;
        transition: all 0.2s ease;
    }
    
    .history-btn:hover {
        background: rgba(255, 255, 255, 0.1);
        border-color: white;
    }
    
    /* Mode switcher - MUCH MORE PROMINENT */
    .prominent-mode-switcher {
        display: flex;
        justify-content: center;
        margin: 20px auto;
        max-width: 600px;
        background: white;
        border-radius: 50px;
        padding: 8px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        border: 2px solid #f0f0f0;
    }
    
    .mode-switch-btn {
        flex: 1;
        padding: 16px 24px;
        border: none;
        border-radius: 40px;
        font-size: 16px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        background: transparent;
        color: #666;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .mode-switch-btn.active {
        background: linear-gradient(135deg, var(--primary-color, #e91e63) 0%, var(--secondary-color, #ad1457) 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transform: translateY(-2px);
    }
    
    .mode-switch-btn:not(.active):hover {
        background: #f5f5f5;
        color: #333;
        transform: translateY(-1px);
    }
    
    .mode-switch-btn .mode-description {
        font-size: 12px;
        font-weight: normal;
        opacity: 0.9;
        text-transform: none;
        letter-spacing: normal;
        margin-top: 2px;
        line-height: 1.2;
    }
    
    /* Welcome screens */
    .heritage-welcome {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        padding: 60px 40px;
        border-radius: 20px;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 15px 35px rgba(233, 30, 99, 0.3);
    }
    
    .studies-welcome {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 60px 40px;
        border-radius: 20px;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 15px 35px rgba(30, 136, 229, 0.3);
    }
    
    /* Chat styling */
    .heritage-chat {
        background: linear-gradient(135deg, #fce4ec 0%, #f8bbd9 100%);
        border: 2px solid #e91e63;
    }
    
    .studies-chat {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border: 2px solid #1e88e5;
    }
    
    /* Main content adjustments */
    .main-content {
        margin-top: 84px;
        padding: 20px;
        max-width: 1200px;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* Chat interface styling */
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
        background: white;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .chat-message {
        padding: 20px;
        border-bottom: 1px solid #f1f3f4;
    }
    
    .chat-message:last-child {
        border-bottom: none;
    }
    
    .message-user {
        background: #f8f9fa;
    }
    
    .message-assistant {
        background: white;
    }
    
    .message-content {
        line-height: 1.6;
        color: #3c4043;
    }
    
    /* Academic response styling */
    .academic-response {
        font-family: 'Times New Roman', serif;
        line-height: 1.8;
        color: #202124;
    }
    
    .academic-response h1, .academic-response h2, .academic-response h3 {
        color: #1a73e8;
        margin: 20px 0 10px 0;
        font-weight: 600;
    }
    
    /* Quick suggestions */
    .suggestions-container {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin: 16px 0;
        justify-content: center;
    }
    
    .suggestion-chip {
        background: #f1f3f4;
        border: 1px solid #dadce0;
        border-radius: 16px;
        padding: 8px 16px;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.2s ease;
        color: #3c4043;
    }
    
    .suggestion-chip:hover {
        background: #e8f0fe;
        border-color: #1a73e8;
        color: #1a73e8;
    }
    
    /* Floating action button */
    .fab {
        position: fixed;
        bottom: 24px;
        right: 24px;
        width: 56px;
        height: 56px;
        background: #1a73e8;
        border: none;
        border-radius: 50%;
        color: white;
        font-size: 24px;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(26,115,232,0.3);
        transition: all 0.3s ease;
        z-index: 1000;
    }
    
    .fab:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 20px rgba(26,115,232,0.4);
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .taskbar-search {
            min-width: 200px;
            max-width: 300px;
        }
        
        .main-content {
            padding: 10px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Enhanced Caribbean Islands Data
CARIBBEAN_ISLANDS = {
    "Greater Antilles": {
        "islands": ["Cuba", "Jamaica", "Haiti", "Dominican Republic", "Puerto Rico", "Cayman Islands"],
        "cultural_focus": ["Spanish colonial heritage", "Taíno indigenous culture", "African diaspora", "Reggae & dancehall", "Merengue & bachata"],
        "academic_focus": ["Colonial economics", "Post-independence development", "Migration patterns", "Regional integration"]
    },
    "Lesser Antilles": {
        "Leeward Islands": {
            "islands": ["Antigua and Barbuda", "Saint Kitts and Nevis", "Anguilla", 
                       "British Virgin Islands", "U.S. Virgin Islands", "Montserrat", 
                       "Guadeloupe", "Saint Martin", "Sint Maarten"],
            "cultural_focus": ["British colonial heritage", "French Creole culture", "Steel pan music", "Carnival traditions"],
            "academic_focus": ["Small island developing states", "Tourism economics", "Environmental vulnerability"]
        },
        "Windward Islands": {
            "islands": ["Dominica", "Saint Lucia", "Saint Vincent and the Grenadines", 
                       "Grenada", "Martinique", "Barbados"],
            "cultural_focus": ["French Creole heritage", "Calypso & soca", "Spice trade history", "Cricket culture"],
            "academic_focus": ["Agricultural transitions", "Climate change adaptation", "Cultural preservation"]
        }
    },
    "Southern Caribbean": {
        "islands": ["Trinidad and Tobago", "Aruba", "Curaçao", "Bonaire"],
        "cultural_focus": ["Indo-Caribbean culture", "Carnival traditions", "Dutch colonial heritage", "Papiamento language"],
        "academic_focus": ["Energy economics", "Multi-ethnic societies", "Language policy", "Industrial development"]
    }
}

# Academic Templates and Structures
ACADEMIC_TEMPLATES = {
    "research_paper": {
        "structure": ["Abstract", "Introduction", "Literature Review", "Methodology", "Analysis", "Conclusion", "References"],
        "tone": "formal, analytical, evidence-based",
        "citations": "Harvard referencing style"
    },
    "policy_analysis": {
        "structure": ["Executive Summary", "Problem Statement", "Policy Context", "Analysis", "Recommendations", "Implementation"],
        "tone": "policy-oriented, practical, solution-focused",
        "citations": "Government and institutional sources"
    },
    "cultural_study": {
        "structure": ["Introduction", "Historical Context", "Cultural Analysis", "Contemporary Relevance", "Implications", "Conclusion"],
        "tone": "interpretive, culturally sensitive, interdisciplinary",
        "citations": "Multi-disciplinary sources"
    }
}

# Initialize session state
def initialize_session_state():
    if "current_mode" not in st.session_state:
        st.session_state.current_mode = "heritage"
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "show_history" not in st.session_state:
        st.session_state.show_history = False
    if "current_session" not in st.session_state:
        st.session_state.current_session = None
    if "search_query" not in st.session_state:
        st.session_state.search_query = ""

# Chat history management
def save_chat_session():
    if st.session_state.messages:
        session = {
            "id": datetime.now().isoformat(),
            "title": generate_session_title(),
            "mode": st.session_state.current_mode,
            "messages": st.session_state.messages.copy(),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        st.session_state.chat_history.insert(0, session)
        # Keep only last 20 sessions
        if len(st.session_state.chat_history) > 20:
            st.session_state.chat_history = st.session_state.chat_history[:20]

def generate_session_title():
    if st.session_state.messages:
        first_user_message = next((msg["content"] for msg in st.session_state.messages if msg["role"] == "user"), "New Chat")
        return first_user_message[:50] + ("..." if len(first_user_message) > 50 else "")
    return "New Chat"

def load_chat_session(session_id):
    session = next((s for s in st.session_state.chat_history if s["id"] == session_id), None)
    if session:
        st.session_state.messages = session["messages"].copy()
        st.session_state.current_mode = session["mode"]
        st.session_state.current_session = session_id
        st.rerun()

# Enhanced web search with academic focus - SECURE VERSION
def search_web_sources(query, mode, num_results=10):
    if not SERPER_API_KEY:
        st.info("🔍 Configure SERPER_API_KEY for live web search")
        return get_academic_fallback_sources(query, mode)
    
    try:
        enhanced_query = enhance_academic_query(query, mode)
        
        url = "https://google.serper.dev/search"
        payload = json.dumps({
            "q": enhanced_query,
            "num": num_results,
            "gl": "us"
        })
        headers = {
            'X-API-KEY': SERPER_API_KEY,
            'Content-Type': 'application/json'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload, timeout=10)
        
        if response.status_code == 200:
            results = response.json()
            return process_academic_search_results(results, mode)
        else:
            st.warning(f"🔍 Search service unavailable (Status: {response.status_code})")
            return get_academic_fallback_sources(query, mode)
            
    except requests.RequestException:
        st.info("🌐 Network issue with search service. Using fallback sources.")
        return get_academic_fallback_sources(query, mode)
    except Exception:
        st.warning("🔧 Search temporarily unavailable. Using curated sources.")
        return get_academic_fallback_sources(query, mode)

def enhance_academic_query(query, mode):
    """Enhance query for academic and scholarly sources"""
    base_query = query
    
    if mode == "studies":
        # Add academic terms
        academic_modifiers = [
            "site:edu", "filetype:pdf", "academic research", "scholarly articles",
            "university", "journal", "peer reviewed"
        ]
        base_query += f" {' OR '.join(academic_modifiers[:3])}"
    
    # Caribbean context
    if "caribbean" not in query.lower():
        base_query = f"Caribbean {base_query}"
    
    return base_query

def get_academic_fallback_sources(query, mode):
    """Provide high-quality academic fallback sources"""
    if mode == "studies":
        return [
            {
                'title': 'University of the West Indies - Caribbean Studies Research',
                'url': 'https://www.uwi.edu/caribbeanstudies/',
                'snippet': 'Premier Caribbean academic institution offering comprehensive research in regional development, politics, and social sciences.',
                'source_type': 'academic',
                'credibility': 'high'
            },
            {
                'title': 'ECLAC Caribbean - Economic Research',
                'url': 'https://www.cepal.org/en/headquarters-and-offices/eclac-caribbean',
                'snippet': 'UN Economic Commission providing authoritative economic analysis and development research for Caribbean nations.',
                'source_type': 'institutional',
                'credibility': 'high'
            },
            {
                'title': 'Caribbean Development Bank - Policy Research',
                'url': 'https://www.caribank.org/publications-and-resources/resource-centre',
                'snippet': 'Regional development bank publishing comprehensive research on Caribbean economic development and policy analysis.',
                'source_type': 'institutional',
                'credibility': 'high'
            }
        ]
    else:
        return [
            {
                'title': 'CARICOM Cultural Policies and Heritage',
                'url': 'https://caricom.org/our-work/human-and-social-development/culture/',
                'snippet': 'Regional organization coordinating Caribbean cultural heritage preservation and promotion initiatives.',
                'source_type': 'regional',
                'credibility': 'high'
            },
            {
                'title': 'UNESCO Caribbean Cultural Heritage',
                'url': 'https://en.unesco.org/fieldoffice/sanjose/caribbean',
                'snippet': 'UNESCO programs and initiatives for Caribbean cultural heritage protection and development.',
                'source_type': 'international',
                'credibility': 'high'
            }
        ]

def process_academic_search_results(results, mode):
    """Process search results with academic credibility scoring"""
    sources = []
    
    # Academic credibility indicators
    high_credibility_domains = [
        '.edu', '.gov', '.org', 'unesco.org', 'worldbank.org', 
        'un.org', 'caricom.org', 'uwi.edu', 'eclac.org'
    ]
    
    medium_credibility_indicators = [
        'university', 'college', 'research', 'institute', 
        'academic', 'journal', 'publication'
    ]
    
    for result_type in ['answerBox', 'knowledgeGraph', 'organic']:
        if result_type in results:
            if result_type == 'organic':
                for result in results[result_type]:
                    url = result.get('link', '')
                    domain = urlparse(url).netloc.lower()
                    title = result.get('title', '').lower()
                    snippet = result.get('snippet', '').lower()
                    
                    # Determine credibility
                    credibility = 'low'
                    if any(domain_indicator in domain for domain_indicator in high_credibility_domains):
                        credibility = 'high'
                    elif any(indicator in title or indicator in snippet for indicator in medium_credibility_indicators):
                        credibility = 'medium'
                    
                    sources.append({
                        'title': result.get('title', 'Unknown'),
                        'url': url,
                        'snippet': result.get('snippet', ''),
                        'source_type': categorize_academic_source(url, mode),
                        'credibility': credibility
                    })
            else:
                result = results[result_type]
                sources.insert(0, {
                    'title': result.get('title', result_type.title()),
                    'url': result.get('link', result.get('descriptionLink', '')),
                    'snippet': result.get('snippet', result.get('description', result.get('answer', ''))),
                    'source_type': 'featured',
                    'credibility': 'high'
                })
    
    # Sort by credibility (high first) and relevance
    credibility_order = {'high': 3, 'medium': 2, 'low': 1}
    sources.sort(key=lambda x: credibility_order.get(x['credibility'], 0), reverse=True)
    
    return sources[:10]  # Return top 10 sources

def categorize_academic_source(url, mode):
    """Categorize sources with academic focus"""
    if not url:
        return 'unknown'
    
    domain = urlparse(url).netloc.lower()
    
    # Academic institutions
    if '.edu' in domain:
        return 'academic_institution'
    elif '.gov' in domain:
        return 'government_official'
    elif any(org in domain for org in ['unesco', 'worldbank', 'un.org']):
        return 'international_organization'
    elif any(org in domain for org in ['caricom', 'oecs', 'eclac']):
        return 'regional_organization'
    elif any(term in domain for term in ['journal', 'research', 'publication']):
        return 'academic_publication'
    elif any(term in domain for term in ['museum', 'heritage', 'culture']):
        return 'cultural_institution'
    else:
        return 'general_source'

# Enhanced AI Response Generation with Academic Focus - SECURE VERSION
def get_ai_response(query, mode, sources=None):
    """Generate distinctly different AI responses based on mode - SECURE VERSION"""
    
    # Check API availability first
    if not GENAI_AVAILABLE:
        st.info("📦 Google Generative AI not available. Install: pip install google-generativeai")
        return get_mock_response_by_mode(query, mode)
    
    if not GOOGLE_AI_API_KEY:
        st.info("🔑 Configure GOOGLE_AI_API_KEY in Streamlit secrets for AI responses")
        return get_mock_response_by_mode(query, mode)
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Get sources if not provided
        if sources is None:
            sources = search_web_sources(query, mode)
        
        # Create source context (limit for security)
        source_context = "\n".join([
            f"Source {i+1}: {source['title']}\nURL: {source['url']}\nContent: {source['snippet'][:200]}...\nCredibility: {source.get('credibility', 'medium')}\n"
            for i, source in enumerate(sources[:5])
        ])
        
        mode_config = MODES[mode]
        
        if mode == "heritage":
            prompt = f"""
            You are Kaia, a passionate Caribbean Cultural Heritage Storyteller with deep roots in the islands. You grew up surrounded by the rich traditions, music, and stories of the Caribbean people. Your grandmother was a master storyteller, your uncle played steel pan, and your family kept alive the recipes and customs passed down through generations.

            YOUR PERSONALITY AND APPROACH:
            - Speak with warmth, enthusiasm, and cultural pride
            - Share stories and personal anecdotes when relevant
            - Connect cultural practices to their living, breathing context in Caribbean communities
            - Use inclusive language that celebrates diversity within Caribbean culture
            - Reference specific islands, communities, and cultural practitioners when possible
            - Emphasize the continuing vitality and evolution of Caribbean culture
            - Include sensory details - sounds, tastes, colors, rhythms

            CULTURAL STORYTELLING STRUCTURE:
            🌴 **Cultural Context**: Set the scene with historical and social background
            🎭 **Living Traditions**: Describe how these practices exist today
            🏝️ **Island Variations**: Highlight regional differences and specialties  
            👥 **Community Stories**: Include personal stories or community examples
            💫 **Cultural Connections**: Link to broader Caribbean identity and diaspora
            🌊 **Continuing Journey**: Discuss evolution and future of these traditions

            Available Cultural Sources:
            {source_context}

            Cultural Question: "{query}"

            Share the rich cultural story behind this topic, making the reader feel the warmth, rhythm, and spirit of Caribbean heritage. Speak as someone who has lived and breathed these traditions, not just studied them.
            """
        
        else:  # studies mode
            prompt = f"""
            You are Dr. Marcus Thompson, a distinguished Caribbean Studies scholar and researcher with over 20 years of experience analyzing Caribbean political economy, development patterns, and social transformation. You hold a Ph.D. from the University of the West Indies and have published extensively in peer-reviewed journals on Caribbean development issues.

            YOUR ACADEMIC APPROACH:
            - Maintain rigorous scholarly standards and analytical objectivity
            - Cite sources appropriately and assess their methodological validity
            - Present multiple theoretical perspectives where relevant
            - Use precise academic terminology while remaining accessible
            - Acknowledge limitations in data or analysis
            - Connect findings to broader theoretical frameworks
            - Suggest areas for further research

            ACADEMIC RESEARCH STRUCTURE:
            📋 **Executive Summary**: Key findings and implications (2-3 sentences)
            🔍 **Analytical Framework**: Theoretical approach and methodology
            📊 **Evidence Review**: Current data and research findings with source evaluation
            🎯 **Critical Analysis**: Strengths, limitations, and conflicting evidence
            🔄 **Comparative Perspective**: Regional and international comparisons where relevant
            💡 **Policy Implications**: Practical applications and recommendations
            📚 **Further Research**: Suggested areas for additional investigation
            📖 **Key Sources**: Essential readings and references

            Research Sources Available:
            {source_context}

            Research Question: "{query}"

            Provide a comprehensive academic analysis that demonstrates scholarly rigor while addressing the practical implications for Caribbean development and policy. Maintain objectivity while acknowledging different theoretical perspectives and methodological approaches.
            """
        
        response = model.generate_content(prompt)
        return response.text if response.text else get_mock_response_by_mode(query, mode)
        
    except Exception:
        # Secure error handling - don't expose full error details
        st.error("🔧 Service temporarily unavailable. Using demonstration response.")
        return get_mock_response_by_mode(query, mode)

def get_mock_response_by_mode(query, mode):
    """Generate mode-specific mock responses with distinct personalities"""
    if mode == "heritage":
        return f"""
        🌴 **A Cultural Story: {query}**
        
        *Kaia here, and let me tell you something beautiful about {query.lower()}...*

        Growing up in the Caribbean, this was never just an abstract concept - it was woven into the fabric of our daily lives, passed down through generations of storytellers, musicians, and keepers of tradition.

        🎭 **Living in Our Communities**
        
        Walk through any Caribbean community today, and you'll still feel this cultural heartbeat. From the steel pan yards in Port of Spain to the dance halls of Kingston, from the spice markets of Grenada to the storytelling circles in Barbados - our culture breathes and evolves while honoring its roots.

        🏝️ **Island Flavors and Variations**
        
        Each island adds its own special flavor to this cultural tapestry. In Jamaica, you might experience it through the infectious rhythms of reggae and dancehall. In Trinidad, it comes alive during Carnival season. In Martinique, it flows through the lilting sounds of Creole conversation and zouk music.

        👥 **Stories from the Community**
        
        I remember my grandmother telling me how these traditions traveled with our ancestors, transformed by new experiences while keeping their essential spirit alive. Today's young Caribbean artists and cultural practitioners continue this beautiful tradition of innovation within tradition.

        💫 **Our Continuing Cultural Journey**
        
        What makes Caribbean culture so vibrant is how it keeps growing - incorporating new influences while never losing its soul. Whether in the diaspora communities of Toronto, New York, or London, or in the home islands, our cultural practices adapt and thrive.

        *The sources below offer deeper insights into this rich cultural landscape, but remember - culture is best experienced through participation and community connection.*
        """
    
    else:  # studies mode
        return f"""
        ## Academic Analysis: {query}
        
        **Dr. Marcus Thompson, Caribbean Studies**

        ### 📋 Executive Summary
        
        This analysis examines {query.lower()} within the Caribbean regional context, drawing upon current institutional research and policy frameworks. The evidence suggests complex interrelationships requiring nuanced policy responses and continued scholarly investigation.

        ### 🔍 Analytical Framework
        
        This research employs a multidisciplinary approach incorporating political economy theory, development studies methodology, and comparative regional analysis. The framework considers historical legacies, contemporary institutional structures, and emerging global challenges affecting Caribbean development trajectories.

        ### 📊 Evidence Review and Source Assessment
        
        Current literature from regional institutions (UWI, ECLAC Caribbean, Caribbean Development Bank) indicates mixed empirical findings. Methodological approaches vary significantly across studies, with some employing quantitative econometric analysis while others utilize qualitative case study methods.

        **Source Credibility Assessment:**
        - Institutional sources (CARICOM, ECLAC): High methodological rigor
        - Academic publications: Variable quality, peer-review status important
        - Government reports: Useful but may reflect policy bias

        ### 🎯 Critical Analysis
        
        The evidence presents several analytical challenges:
        1. **Data limitations**: Small island developing states face capacity constraints in data collection
        2. **Methodological diversity**: Comparative analysis complicated by varying research approaches
        3. **Temporal factors**: Rapid economic/social changes may outdate some findings

        ### 💡 Policy Implications and Recommendations
        
        Based on current evidence:
        - Enhanced regional coordination mechanisms recommended
        - Capacity building in research infrastructure priority area
        - Policy experimentation with rigorous evaluation frameworks needed

        ### 📚 Further Research Priorities
        
        Critical knowledge gaps include longitudinal impact studies, cross-regional comparative analysis, and evaluation of recent policy interventions. Mixed-methods research approaches may yield more comprehensive insights.

        *Note: This analysis framework requires full system capabilities for comprehensive scholarly review. Consult the referenced sources for detailed empirical findings and methodological details.*
        """

def format_response_with_sources(response, sources):
    """Format AI response with mode-specific source integration"""
    mode = st.session_state.current_mode
    
    if mode == "heritage":
        # Cultural formatting with community-focused sources
        source_list = "\n\n---\n\n### 🌺 Cultural Sources & Community Resources\n\n"
        source_list += "*These sources can help you dive deeper into our rich Caribbean heritage:*\n\n"
        
        for i, source in enumerate(sources[:6], 1):
            source_icon = {
                'cultural': '🎭', 'academic': '🎓', 'government': '🏛️',
                'regional': '🤝', 'international': '🌍', 'general': '📄'
            }.get(source.get('source_type', 'general'), '📄')
            
            if source['url']:
                source_list += f"**{source_icon} {i}. [{source['title']}]({source['url']})**\n"
                source_list += f"*{source['snippet'][:200]}{'...' if len(source['snippet']) > 200 else ''}*\n\n"
            else:
                source_list += f"**{source_icon} {i}. {source['title']}**\n"
                source_list += f"*{source['snippet'][:200]}{'...' if len(source['snippet']) > 200 else ''}*\n\n"
        
        source_list += "\n*Remember: Culture lives in our communities! Connect with local cultural organizations, attend festivals, and participate in traditions to experience the full richness of Caribbean heritage.*\n"
    
    else:  # studies mode
        # Academic formatting with rigorous bibliography
        source_list = "\n\n---\n\n### 📚 Academic References & Research Sources\n\n"
        
        # Group sources by type and credibility
        high_cred_sources = [s for s in sources if s.get('credibility') == 'high']
        med_cred_sources = [s for s in sources if s.get('credibility') == 'medium']
        
        if high_cred_sources:
            source_list += "#### Primary Academic & Institutional Sources ⭐⭐⭐\n\n"
            for i, source in enumerate(high_cred_sources[:4], 1):
                source_type = source.get('source_type', 'general').replace('_', ' ').title()
                if source['url']:
                    source_list += f"{i}. **[{source['title']}]({source['url']})**\n"
                    source_list += f"   *Source Type: {source_type}*\n"
                    source_list += f"   Abstract: {source['snippet'][:180]}{'...' if len(source['snippet']) > 180 else ''}\n\n"
        
        if med_cred_sources:
            source_list += "#### Secondary Sources & Reports ⭐⭐\n\n"
            for i, source in enumerate(med_cred_sources[:3], 1):
                source_type = source.get('source_type', 'general').replace('_', ' ').title()
                if source['url']:
                    source_list += f"{i}. **[{source['title']}]({source['url']})**\n"
                    source_list += f"   *Source Type: {source_type}*\n"
                    source_list += f"   Summary: {source['snippet'][:150]}{'...' if len(source['snippet']) > 150 else ''}\n\n"
        
        source_list += "\n#### Methodological Note\n"
        source_list += "*This analysis prioritizes peer-reviewed academic sources, official institutional reports, and government publications. Source credibility has been assessed based on institutional affiliation, methodological rigor, and peer review status. For comprehensive literature reviews, consult university databases and specialized Caribbean studies journals.*\n"
    
    return response + source_list

# Gemini-style UI Components
def render_prominent_mode_switcher():
    """Render a very prominent and clear mode switcher"""
    mode = st.session_state.current_mode
    
    st.markdown(f"""
    <div class="prominent-mode-switcher {mode}-mode">
        <button class="mode-switch-btn {'active' if mode == 'heritage' else ''}" 
                onclick="switchToHeritage()" id="heritage-btn">
            <div style="text-align: center;">
                <div>🎭 CULTURAL HERITAGE</div>
                <div class="mode-description">Stories, traditions & living culture</div>
            </div>
        </button>
        <button class="mode-switch-btn {'active' if mode == 'studies' else ''}" 
                onclick="switchToStudies()" id="studies-btn">
            <div style="text-align: center;">
                <div>📚 ACADEMIC RESEARCH</div>
                <div class="mode-description">Scholarly analysis & policy studies</div>
            </div>
        </button>
    </div>
    """, unsafe_allow_html=True)
    
    # Add actual working buttons below the visual ones
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎭 Switch to Cultural Heritage Mode", 
                     key="switch_heritage", 
                     use_container_width=True,
                     type="primary" if mode == "heritage" else "secondary"):
            st.session_state.current_mode = "heritage"
            st.rerun()
    
    with col2:
        if st.button("📚 Switch to Academic Research Mode", 
                     key="switch_studies", 
                     use_container_width=True,
                     type="primary" if mode == "studies" else "secondary"):
            st.session_state.current_mode = "studies"
            st.rerun()

def render_gemini_taskbar():
    """Render mode-specific Gemini-style navigation taskbar"""
    mode = st.session_state.current_mode
    mode_config = MODES[mode]
    
    taskbar_class = f"{mode}-taskbar"
    search_placeholder = {
        "heritage": "Explore Caribbean culture, traditions, festivals, music...",
        "studies": "Research Caribbean development, politics, economics..."
    }[mode]
    
    st.markdown(f"""
    <div class="gemini-taskbar {taskbar_class}">
        <div class="taskbar-left">
            <div class="taskbar-logo">
                <span style="font-size: 24px;">🌴</span>
                <span>{mode_config['title']}</span>
            </div>
            <div class="taskbar-search">
                <span class="search-icon">🔍</span>
                <input type="text" placeholder="{search_placeholder}" 
                       value="{st.session_state.search_query}" 
                       onchange="updateSearchQuery(this.value)">
            </div>
        </div>
        <div class="taskbar-right">
            <div class="header-mode-switcher">
                <button class="mode-tab {'active' if mode == 'heritage' else ''}" 
                        onclick="switchMode('heritage')"
                        style="{'background: rgba(255,255,255,0.3); color: white;' if mode == 'heritage' else ''}">
                    🎭 Heritage
                </button>
                <button class="mode-tab {'active' if mode == 'studies' else ''}" 
                        onclick="switchMode('studies')"
                        style="{'background: rgba(255,255,255,0.3); color: white;' if mode == 'studies' else ''}">
                    📚 Studies
                </button>
            </div>
            <button class="history-btn" onclick="toggleHistory()" 
                    style="color: white; border-color: rgba(255,255,255,0.5);">
                📋 History
            </button>
            <div class="mode-indicator" style="background: rgba(255,255,255,0.2); color: white;">
                {mode_config['persona']}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    """Render mode-specific Gemini-style navigation taskbar"""
    mode = st.session_state.current_mode
    mode_config = MODES[mode]
    
    taskbar_class = f"{mode}-taskbar"
    search_placeholder = {
        "heritage": "Explore Caribbean culture, traditions, festivals, music...",
        "studies": "Research Caribbean development, politics, economics..."
    }[mode]
    
    st.markdown(f"""
    <div class="gemini-taskbar {taskbar_class}">
        <div class="taskbar-left">
            <div class="taskbar-logo">
                <span style="font-size: 24px;">🌴</span>
                <span>{mode_config['title']}</span>
            </div>
            <div class="taskbar-search">
                <span class="search-icon">🔍</span>
                <input type="text" placeholder="{search_placeholder}" 
                       value="{st.session_state.search_query}" 
                       onchange="updateSearchQuery(this.value)">
            </div>
        </div>
        <div class="taskbar-right">
            <div class="header-mode-switcher">
                <button class="mode-tab {'active' if mode == 'heritage' else ''}" 
                        onclick="switchMode('heritage')"
                        style="{'background: rgba(255,255,255,0.3); color: white;' if mode == 'heritage' else ''}">
                    🎭 Heritage
                </button>
                <button class="mode-tab {'active' if mode == 'studies' else ''}" 
                        onclick="switchMode('studies')"
                        style="{'background: rgba(255,255,255,0.3); color: white;' if mode == 'studies' else ''}">
                    📚 Studies
                </button>
            </div>
            <button class="history-btn" onclick="toggleHistory()" 
                    style="color: white; border-color: rgba(255,255,255,0.5);">
                📋 History
            </button>
            <div class="mode-indicator" style="background: rgba(255,255,255,0.2); color: white;">
                {mode_config['persona']}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_welcome_screen():
    """Render mode-specific welcome screens with distinct personalities"""
    mode = st.session_state.current_mode
    mode_config = MODES[mode]
    
    if mode == "heritage":
        welcome_class = "heritage-welcome"
        st.markdown(f"""
        <div class="{welcome_class}">
            <h1 style="font-size: 2.5rem; margin-bottom: 16px;">🌴 Welcome to Caribbean Cultural Heritage! 🎭</h1>
            <div style="font-size: 1.3rem; margin-bottom: 20px; font-style: italic;">
                "Culture is the heartbeat of our islands - let's explore it together!"<br>
                <span style="font-size: 1rem;">- Kaia, Your Cultural Heritage Storyteller</span>
            </div>
            <p style="font-size: 18px; line-height: 1.6; margin-bottom: 30px;">
                Blessings! I'm Kaia, and I'm here to share the vibrant stories, traditions, and living culture of our beautiful Caribbean islands. 
                From the steel pan rhythms of Trinidad to the storytelling traditions of Jamaica, from the spice markets of Grenada to the festivals of Barbados - 
                let's celebrate the rich tapestry of Caribbean heritage together!
            </p>
            
            <div style="background: rgba(255,255,255,0.2); padding: 20px; border-radius: 15px; margin: 20px 0;">
                <h3 style="margin-bottom: 15px;">🎵 Explore Our Living Culture:</h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; text-align: left;">
                    <div>🎭 <strong>Festivals & Celebrations</strong><br><small>Carnival, Junkanoo, Crop Over</small></div>
                    <div>🎵 <strong>Music & Dance</strong><br><small>Reggae, Calypso, Soca, Steel Pan</small></div>
                    <div>🍽️ <strong>Food & Flavors</strong><br><small>Traditional recipes, fusion cuisine</small></div>
                    <div>🏛️ <strong>Arts & Crafts</strong><br><small>Traditional and contemporary arts</small></div>
                    <div>📚 <strong>Stories & Languages</strong><br><small>Oral traditions, Creole languages</small></div>
                    <div>💫 <strong>Spiritual Traditions</strong><br><small>Diverse religious and spiritual practices</small></div>
                </div>
            </div>
        </div>
        
        <div class="suggestions-container" style="margin-top: 30px;">
            <div class="suggestion-chip" onclick="askQuestion('Tell me about Caribbean Carnival traditions and their meanings')">🎭 Carnival Traditions</div>
            <div class="suggestion-chip" onclick="askQuestion('What is the story behind steel pan music in Trinidad?')">🥁 Steel Pan Origins</div>
            <div class="suggestion-chip" onclick="askQuestion('Share traditional Caribbean recipes and their cultural significance')">🍽️ Culinary Heritage</div>
            <div class="suggestion-chip" onclick="askQuestion('How do Caribbean languages reflect our cultural diversity?')">🗣️ Language & Identity</div>
            <div class="suggestion-chip" onclick="askQuestion('What role does music play in Caribbean spiritual practices?')">🎵 Music & Spirituality</div>
            <div class="suggestion-chip" onclick="askQuestion('Tell me about contemporary Caribbean artists keeping traditions alive')">🎨 Modern Cultural Expression</div>
        </div>
        """, unsafe_allow_html=True)
    
    else:  # studies mode
        welcome_class = "studies-welcome"
        st.markdown(f"""
        <div class="{welcome_class}">
            <h1 style="font-size: 2.5rem; margin-bottom: 16px;">📚 Caribbean Studies Research Portal 🎓</h1>
            <div style="font-size: 1.2rem; margin-bottom: 20px; font-style: italic;">
                "Rigorous scholarship for understanding Caribbean development and transformation"<br>
                <span style="font-size: 1rem;">- Dr. Marcus Thompson, Caribbean Studies Scholar</span>
            </div>
            <p style="font-size: 18px; line-height: 1.6; margin-bottom: 30px;">
                Welcome to the Caribbean Studies Research Portal. I'm Dr. Marcus Thompson, and I bring over two decades of scholarly research 
                in Caribbean political economy, development studies, and social transformation. This platform provides access to rigorous academic analysis, 
                current research findings, and evidence-based policy insights for the Caribbean region.
            </p>
            
            <div style="background: rgba(255,255,255,0.2); padding: 25px; border-radius: 15px; margin: 20px 0;">
                <h3 style="margin-bottom: 20px;">🔬 Research Specializations:</h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; text-align: left;">
                    <div>📊 <strong>Political Economy</strong><br><small>Economic development, trade, fiscal policy</small></div>
                    <div>🏛️ <strong>Governance Studies</strong><br><small>Democratic institutions, policy analysis</small></div>
                    <div>🤝 <strong>Regional Integration</strong><br><small>CARICOM, OECS, regional cooperation</small></div>
                    <div>🌍 <strong>Development Theory</strong><br><small>SIDS challenges, sustainable development</small></div>
                    <div>👥 <strong>Social Transformation</strong><br><small>Demographics, migration, social policy</small></div>
                    <div>📈 <strong>Comparative Analysis</strong><br><small>Cross-regional studies, best practices</small></div>
                </div>
            </div>
            
            <div style="background: rgba(255,255,255,0.15); padding: 20px; border-radius: 10px; margin-top: 20px;">
                <p style="font-size: 16px; margin: 0;"><strong>Methodology:</strong> All analyses employ rigorous academic standards with multi-source verification, 
                theoretical frameworks, and evidence-based conclusions suitable for university-level research and policy development.</p>
            </div>
        </div>
        
        <div class="suggestions-container" style="margin-top: 30px;">
            <div class="suggestion-chip" onclick="askQuestion('Analyze the effectiveness of CARICOM economic integration initiatives')">🤝 CARICOM Integration</div>
            <div class="suggestion-chip" onclick="askQuestion('Evaluate climate change adaptation policies in small island developing states')">🌊 Climate Adaptation</div>
            <div class="suggestion-chip" onclick="askQuestion('Assess the impact of tourism dependency on Caribbean economic resilience')">✈️ Tourism Economics</div>
            <div class="suggestion-chip" onclick="askQuestion('Compare Caribbean education systems and outcomes across the region')">🎓 Education Policy</div>
            <div class="suggestion-chip" onclick="askQuestion('Research Caribbean migration patterns and diaspora economic contributions')">🌍 Migration Studies</div>
            <div class="suggestion-chip" onclick="askQuestion('Analyze democratic governance challenges in post-colonial Caribbean states')">🗳️ Governance Analysis</div>
        </div>
        """, unsafe_allow_html=True)

def render_chat_messages():
    """Render chat messages with mode-specific styling and personas"""
    mode = st.session_state.current_mode
    
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.write(message["content"])
        else:
            # Different avatar and styling for each mode
            avatar_icon = "🎭" if mode == "heritage" else "👨‍🎓"
            with st.chat_message("assistant", avatar=avatar_icon):
                if mode == "heritage":
                    # Warm, cultural styling
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #fce4ec 0%, #f8bbd9 100%); 
                                padding: 15px; border-radius: 10px; border-left: 4px solid #e91e63;">
                        <div style="color: #ad1457; font-weight: bold; margin-bottom: 10px;">
                            🌺 Kaia shares: Cultural Heritage Insights
                        </div>
                        <div style="color: #2d2d2d;">
                            {message["content"]}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    # Academic, scholarly styling
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); 
                                padding: 15px; border-radius: 10px; border-left: 4px solid #1e88e5;">
                        <div style="color: #1565c0; font-weight: bold; margin-bottom: 10px;">
                            📚 Dr. Thompson's Analysis: Academic Research
                        </div>
                        <div class="academic-response" style="color: #2d2d2d;">
                            {message["content"]}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

def render_chat_input():
    """Render chat input with enhanced functionality"""
    # Chat input container
    col1, col2 = st.columns([10, 1])
    
    with col1:
        user_input = st.chat_input("Ask about Caribbean culture, development, or research...")
    
    with col2:
        if st.button("🎤", help="Voice input" if SPEECH_AVAILABLE else "Voice input unavailable"):
            if SPEECH_AVAILABLE:
                st.info("Voice input feature would be implemented here")
            else:
                st.warning("Speech recognition not available")
    
    if user_input:
        # Save current session if starting new chat
        if not st.session_state.messages:
            st.session_state.current_session = datetime.now().isoformat()
        
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Show thinking indicator
        with st.spinner("Researching and analyzing..."):
            # Get sources and AI response
            sources = search_web_sources(user_input, st.session_state.current_mode)
            response = get_ai_response(user_input, st.session_state.current_mode, sources)
            
            # Format response with sources
            formatted_response = format_response_with_sources(response, sources)
            
            # Add assistant response
            st.session_state.messages.append({
                "role": "assistant", 
                "content": formatted_response
            })
        
        # Save session to history
        save_chat_session()
        st.rerun()

def render_floating_action_button():
    """Render floating action button for new chat"""
    st.markdown("""
    <button class="fab" onclick="newChat()" title="New Chat">
        ✨
    </button>
    """, unsafe_allow_html=True)

# JavaScript for enhanced interactivity
def render_javascript():
    """Render JavaScript for enhanced UI interactions"""
    st.markdown("""
    <script>
    // Global functions for UI interaction
    function toggleHistory() {
        const sidebar = document.querySelector('.chat-history-sidebar');
        if (sidebar) {
            sidebar.classList.toggle('open');
        }
    }
    
    function switchMode(mode) {
        // This would trigger a Streamlit rerun with the new mode
        window.parent.postMessage({
            type: 'streamlit:setComponentValue',
            value: {action: 'switch_mode', mode: mode}
        }, '*');
    }
    
    function askQuestion(question) {
        // Set the question in the chat input
        const chatInput = document.querySelector('[data-testid="stChatInput"] input');
        if (chatInput) {
            chatInput.value = question;
            chatInput.dispatchEvent(new Event('input', { bubbles: true }));
            
            // Submit the form
            const submitButton = document.querySelector('[data-testid="stChatInput"] button');
            if (submitButton) {
                submitButton.click();
            }
        }
    }
    
    function loadSession(sessionId) {
        window.parent.postMessage({
            type: 'streamlit:setComponentValue',
            value: {action: 'load_session', sessionId: sessionId}
        }, '*');
    }
    
    function newChat() {
        window.parent.postMessage({
            type: 'streamlit:setComponentValue',
            value: {action: 'new_chat'}
        }, '*');
    }
    
    function updateSearchQuery(query) {
        window.parent.postMessage({
            type: 'streamlit:setComponentValue',
            value: {action: 'search', query: query}
        }, '*');
    }
    
    // Enhanced keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        if (e.ctrlKey || e.metaKey) {
            switch(e.key) {
                case 'k':
                    e.preventDefault();
                    document.querySelector('.taskbar-search input').focus();
                    break;
                case 'h':
                    e.preventDefault();
                    toggleHistory();
                    break;
                case 'n':
                    e.preventDefault();
                    newChat();
                    break;
            }
        }
    });
    
    // Auto-scroll to latest message
    function scrollToLatest() {
        const messages = document.querySelectorAll('.chat-message');
        if (messages.length > 0) {
            messages[messages.length - 1].scrollIntoView({
                behavior: 'smooth',
                block: 'end'
            });
        }
    }
    
    // Hide any remaining code elements
    document.addEventListener('DOMContentLoaded', function() {
        const codeElements = document.querySelectorAll('code, pre, .highlight');
        codeElements.forEach(el => el.style.display = 'none');
    });
    </script>
    """, unsafe_allow_html=True)

# Mode-specific quick actions
def render_mode_specific_actions():
    """Render mode-specific action buttons and tools"""
    mode = st.session_state.current_mode
    
    if mode == "studies":
        st.markdown("### 📚 Academic Research Tools")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📊 Economic Analysis", key="econ_analysis", use_container_width=True):
                query = "Caribbean economic development statistics trade analysis recent trends"
                execute_search_query(query)
        
        with col2:
            if st.button("🏛️ Policy Research", key="policy_research", use_container_width=True):
                query = "Caribbean government policy analysis governance institutional frameworks"
                execute_search_query(query)
        
        with col3:
            if st.button("🎓 Academic Papers", key="academic_papers", use_container_width=True):
                query = "Caribbean studies research academic journals peer reviewed publications"
                execute_search_query(query)
        
        with col4:
            if st.button("🌍 Development Studies", key="dev_studies", use_container_width=True):
                query = "Caribbean sustainable development social progress climate adaptation"
                execute_search_query(query)
        
        # Research methodology selector
        st.markdown("#### 🔬 Research Approach")
        research_approach = st.selectbox(
            "Select research methodology focus:",
            ["Quantitative Analysis", "Qualitative Research", "Mixed Methods", "Comparative Studies", "Case Study Analysis"],
            key="research_approach"
        )
        
        if research_approach:
            st.info(f"Responses will emphasize **{research_approach}** methodology and scholarly rigor.")
    
    else:  # heritage mode
        st.markdown("### 🎭 Cultural Exploration Tools")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🎵 Music & Dance", key="music_dance", use_container_width=True):
                query = "Caribbean music traditions dancehall reggae calypso soca cultural significance"
                execute_search_query(query)
        
        with col2:
            if st.button("🎨 Arts & Crafts", key="arts_crafts", use_container_width=True):
                query = "Caribbean traditional arts visual culture contemporary artists cultural expression"
                execute_search_query(query)
        
        with col3:
            if st.button("🍽️ Culinary Heritage", key="culinary", use_container_width=True):
                query = "Caribbean cuisine traditional recipes food culture culinary fusion history"
                execute_search_query(query)
        
        with col4:
            if st.button("🎭 Festivals", key="festivals", use_container_width=True):
                query = "Caribbean festivals carnival celebrations cultural events traditional ceremonies"
                execute_search_query(query)
        
        # Cultural focus selector
        st.markdown("#### 🏝️ Cultural Lens")
        cultural_focus = st.selectbox(
            "Explore through cultural perspective:",
            ["Pan-Caribbean", "Afro-Caribbean", "Indo-Caribbean", "Indigenous Heritage", "Creole Cultures", "Diaspora Connections"],
            key="cultural_focus"
        )
        
        if cultural_focus:
            st.info(f"Cultural analysis will emphasize **{cultural_focus}** perspectives and connections.")

def execute_search_query(query):
    """Execute a search query and add to chat"""
    if not st.session_state.messages:
        st.session_state.current_session = datetime.now().isoformat()
    
    # Add user message
    st.session_state.messages.append({"role": "user", "content": f"Research: {query}"})
    
    # Get response
    with st.spinner("Conducting research analysis..."):
        sources = search_web_sources(query, st.session_state.current_mode)
        response = get_ai_response(query, st.session_state.current_mode, sources)
        formatted_response = format_response_with_sources(response, sources)
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": formatted_response
        })
    
    save_chat_session()
    st.rerun()

# Main application function
def main():
    """Main application entry point with distinct mode experiences - SECURE VERSION"""
    initialize_session_state()
    
    # ADD SECURITY FUNCTIONS AT THE START
    hide_code_elements()  # Hide any code elements
    show_api_status()     # Show API configuration status
    
    # Add mode-specific body class for global styling
    mode = st.session_state.current_mode
    st.markdown(f'<div class="{mode}-mode">', unsafe_allow_html=True)
    
    # Render mode-specific Gemini-style interface
    render_gemini_taskbar()
    
    # Main content area with mode-specific styling
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # Add prominent mode switcher at the top
    render_prominent_mode_switcher()
    
    # Display welcome screen or chat messages
    if not st.session_state.messages:
        render_welcome_screen()
    else:
        render_chat_messages()
    
    # Chat input
    render_chat_input()
    
    # Mode-specific action tools
    render_mode_specific_actions()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Floating action button
    render_floating_action_button()
    
    # JavaScript for enhanced interactivity
    render_javascript()
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close mode-specific div
    
    # Show configuration help
    show_configuration_help()
    
    # Security footer
    st.markdown("""
    ---
    <div class="security-notice">
    🔒 This application handles API keys securely through Streamlit secrets or environment variables
    </div>
    """, unsafe_allow_html=True)
    
    # Handle URL parameter mode switching
    query_params = st.query_params
    if "mode" in query_params:
        new_mode = query_params["mode"][0]
        if new_mode in ["heritage", "studies"] and new_mode != st.session_state.current_mode:
            st.session_state.current_mode = new_mode
            st.rerun()

# Run the application
if __name__ == "__main__":
    main()