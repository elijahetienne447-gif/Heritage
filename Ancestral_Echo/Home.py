import streamlit as st
import datetime
import random

# Page configuration with Caribbean theme
st.set_page_config(
    page_title="Caribbean Cultural Heritage Explorer", 
    layout="wide",
    page_icon="🏝️"
)

# Initialize session state
def initialize_session_state():
    if 'selected_island' not in st.session_state:
        st.session_state['selected_island'] = None
    if 'quiz_started' not in st.session_state:
        st.session_state['quiz_started'] = False
        st.session_state['current_question'] = 0
        st.session_state['score'] = 0
    if 'current_view' not in st.session_state:
        st.session_state['current_view'] = 'home'

initialize_session_state()

# Caribbean islands data structure
CARIBBEAN_ISLANDS = {
    "Greater Antilles": {
        "Cuba": {
            "flag": "🇨🇺",
            "capital": "Havana",
            "independence": "May 20, 1902",
            "population": "11.3 million",
            "languages": ["Spanish"],
            "culture_highlights": [
                "Afro-Cuban music and dance (Salsa, Rumba, Mambo)",
                "Santería religious traditions",
                "Revolutionary art and murals",
                "Cuban cigars and coffee culture"
            ],
            "famous_people": ["José Martí", "Ernest Hemingway (adopted)", "Celia Cruz", "Fidel Castro"],
            "unesco_sites": ["Old Havana", "Trinidad and the Valley de los Ingenios"],
            "traditional_food": ["Ropa Vieja", "Moros y Cristianos", "Tostones", "Cuban Sandwich"],
            "color": "#FF6B6B"
        },
        "Jamaica": {
            "flag": "🇯🇲",
            "capital": "Kingston",
            "independence": "August 6, 1962",
            "population": "2.9 million",
            "languages": ["English", "Jamaican Patois"],
            "culture_highlights": [
                "Reggae music birthplace (Bob Marley)",
                "Rastafarian movement",
                "Olympic sprinting dominance",
                "Blue Mountain coffee"
            ],
            "famous_people": ["Bob Marley", "Usain Bolt", "Marcus Garvey", "Louise Bennett-Coverley"],
            "unesco_sites": ["Blue and John Crow Mountains"],
            "traditional_food": ["Jerk Chicken", "Ackee and Saltfish", "Curry Goat", "Patties"],
            "color": "#4ECDC4"
        },
        "Haiti": {
            "flag": "🇭🇹",
            "capital": "Port-au-Prince",
            "independence": "January 1, 1804",
            "population": "11.4 million",
            "languages": ["French", "Haitian Creole"],
            "culture_highlights": [
                "First free Black republic",
                "Vodou spiritual traditions",
                "Vibrant visual arts and sculptures",
                "Kompa music"
            ],
            "famous_people": ["Toussaint Louverture", "Jean-Jacques Dessalines", "Jean-Michel Basquiat", "Wyclef Jean"],
            "unesco_sites": ["National History Park – Citadel, Sans Souci, Ramiers"],
            "traditional_food": ["Griot", "Bouillon", "Pikliz", "Akasan"],
            "color": "#FF9F43"
        },
        "Dominican Republic": {
            "flag": "🇩🇴",
            "capital": "Santo Domingo",
            "independence": "February 27, 1844",
            "population": "10.8 million",
            "languages": ["Spanish"],
            "culture_highlights": [
                "Merengue and Bachata music",
                "Baseball culture",
                "Colonial architecture in Santo Domingo",
                "Carnival celebrations"
            ],
            "famous_people": ["Juan Luis Guerra", "Pedro Henríquez Ureña", "David Ortiz", "Oscar de la Renta"],
            "unesco_sites": ["Colonial City of Santo Domingo"],
            "traditional_food": ["Mangu", "Sancocho", "Tostones", "Tres Golpes"],
            "color": "#5D4E75"
        },
        "Puerto Rico": {
            "flag": "🇵🇷",
            "capital": "San Juan",
            "independence": "U.S. Territory since 1898",
            "population": "3.2 million",
            "languages": ["Spanish", "English"],
            "culture_highlights": [
                "Salsa music and dance",
                "El Yunque rainforest",
                "Bioluminescent bays",
                "Day of the Three Kings celebrations"
            ],
            "famous_people": ["Roberto Clemente", "Rita Moreno", "Lin-Manuel Miranda", "Ricky Martin"],
            "unesco_sites": ["La Fortaleza and San Juan National Historic Site"],
            "traditional_food": ["Mofongo", "Pasteles", "Jibarito", "Alcapurrias"],
            "color": "#E17055"
        }
    },
    "Lesser Antilles": {
        "Barbados": {
            "flag": "🇧🇧",
            "capital": "Bridgetown",
            "independence": "November 30, 1966",
            "population": "287,000",
            "languages": ["English", "Bajan Creole"],
            "culture_highlights": [
                "Birthplace of rum",
                "Crop Over festival",
                "Calypso and soca music",
                "Cricket culture"
            ],
            "famous_people": ["Rihanna", "Sir Garfield Sobers", "George Lamming", "Kamau Brathwaite"],
            "unesco_sites": ["Historic Bridgetown and its Garrison"],
            "traditional_food": ["Flying Fish and Cou-Cou", "Pudding and Souse", "Bajan Macaroni Pie"],
            "color": "#00B894"
        },
        "Trinidad and Tobago": {
            "flag": "🇹🇹",
            "capital": "Port of Spain",
            "independence": "August 31, 1962",
            "population": "1.4 million",
            "languages": ["English", "Hindi", "French Creole"],
            "culture_highlights": [
                "Carnival birthplace",
                "Steel pan music invention",
                "Calypso and soca music",
                "Multicultural festivals (Diwali, Eid)"
            ],
            "famous_people": ["V.S. Naipaul", "C.L.R. James", "Brian Lara", "Machel Montano"],
            "unesco_sites": [],
            "traditional_food": ["Doubles", "Roti", "Pelau", "Bake and Shark"],
            "color": "#FDCB6E"
        },
        "Saint Lucia": {
            "flag": "🇱🇨",
            "capital": "Castries",
            "independence": "February 22, 1979",
            "population": "183,000",
            "languages": ["English", "Kwéyòl"],
            "culture_highlights": [
                "The Pitons UNESCO site",
                "Two Nobel Prize winners",
                "Jazz Festival",
                "Drive-through volcano"
            ],
            "famous_people": ["Derek Walcott", "Sir Arthur Lewis", "Julien Alfred"],
            "unesco_sites": ["Pitons Management Area"],
            "traditional_food": ["Green Figs and Saltfish", "Bouyon", "Accra", "Lambi"],
            "color": "#74B9FF"
        },
        "Grenada": {
            "flag": "🇬🇩",
            "capital": "St. George's",
            "independence": "February 7, 1974",
            "population": "112,000",
            "languages": ["English", "Grenadian Creole"],
            "culture_highlights": [
                "Spice Island (nutmeg, mace)",
                "Spice Mas Carnival",
                "Underwater sculpture park",
                "Chocolate and cocoa heritage"
            ],
            "famous_people": ["Maurice Bishop", "Kirani James", "Joan Pujolie"],
            "unesco_sites": [],
            "traditional_food": ["Oil Down", "Callaloo", "Lambi Souse", "Nutmeg Ice Cream"],
            "color": "#A29BFE"
        }
    },
    "Netherlands Antilles": {
        "Aruba": {
            "flag": "🇦🇼",
            "capital": "Oranjestad",
            "independence": "Autonomous since 1986",
            "population": "107,000",
            "languages": ["Dutch", "Papiamento", "English", "Spanish"],
            "culture_highlights": [
                "Papiamento language",
                "Carnival celebrations",
                "Dutch colonial architecture",
                "Aloe vera cultivation"
            ],
            "famous_people": ["Juan Chabaya Lampe", "Xander Bogaerts"],
            "unesco_sites": [],
            "traditional_food": ["Keshi Yena", "Pastechi", "Ayaca", "Pan Bati"],
            "color": "#FF7675"
        },
        "Curaçao": {
            "flag": "🇨🇼",
            "capital": "Willemstad",
            "independence": "Autonomous since 2010",
            "population": "164,000",
            "languages": ["Dutch", "Papiamento", "English"],
            "culture_highlights": [
                "UNESCO World Heritage Willemstad",
                "Blue Curaçao liqueur origin",
                "Tumba and merengue music",
                "Jewish heritage (oldest synagogue)"
            ],
            "famous_people": ["Tania Kross", "Churandy Martina"],
            "unesco_sites": ["Historic Area of Willemstad"],
            "traditional_food": ["Iguana Stew", "Keshi Yena", "Funchi", "Stoba"],
            "color": "#81ECEC"
        }
    },
    "French Caribbean": {
        "Martinique": {
            "flag": "🇲🇶",
            "capital": "Fort-de-France",
            "independence": "French Overseas Territory",
            "population": "375,000",
            "languages": ["French", "Martinican Creole"],
            "culture_highlights": [
                "Zouk music birthplace",
                "Mount Pelée volcano",
                "Rhum agricole production",
                "Créole architecture"
            ],
            "famous_people": ["Aimé Césaire", "Frantz Fanon", "Patrick Chamoiseau"],
            "unesco_sites": [],
            "traditional_food": ["Colombo", "Accras de Morue", "Boudin", "Ti' Punch"],
            "color": "#00CEC9"
        },
        "Guadeloupe": {
            "flag": "🇬🇵",
            "capital": "Basse-Terre",
            "independence": "French Overseas Territory",
            "population": "400,000",
            "languages": ["French", "Guadeloupean Creole"],
            "culture_highlights": [
                "Gwo Ka traditional music",
                "Butterfly-shaped twin islands",
                "Carnival celebrations",
                "Sugar cane heritage"
            ],
            "famous_people": ["Saint-John Perse", "Maryse Condé", "Thierry Henry (family roots)"],
            "unesco_sites": [],
            "traditional_food": ["Bokit", "Colombo de Cabri", "Accras", "Sorbet Coco"],
            "color": "#6C5CE7"
        }
    }
}

# Enhanced CSS for Caribbean theme
def load_caribbean_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;900&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%);
        background-size: 400% 400%;
        animation: caribbeanWave 20s ease infinite;
        padding: 0;
    }
    
    @keyframes caribbeanWave {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .stApp {
        background: transparent;
    }
    
    /* Main container */
    .main-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 25px;
        padding: 2rem;
        margin: 1rem;
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Header styling */
    .caribbean-header {
        background: 
            linear-gradient(135deg, rgba(102, 126, 234, 0.9), rgba(245, 87, 108, 0.9)),
            radial-gradient(circle at 30% 20%, rgba(79, 172, 254, 0.3), transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(240, 147, 251, 0.3), transparent 50%);
        color: white;
        padding: 3rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .caribbean-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: conic-gradient(from 0deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        animation: headerRotate 15s linear infinite;
    }
    
    @keyframes headerRotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .caribbean-title {
        font-size: 3.5rem;
        font-weight: 900;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.3);
        background: linear-gradient(45deg, #FFD700, #FFF, #FFD700, #FF6B6B);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        background-size: 300% 300%;
        animation: titleShimmer 4s ease-in-out infinite;
        position: relative;
        z-index: 1;
    }
    
    @keyframes titleShimmer {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .caribbean-subtitle {
        font-size: 1.3rem;
        opacity: 0.95;
        font-style: italic;
        position: relative;
        z-index: 1;
    }
    
    /* Island region cards */
    .region-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(240, 247, 255, 0.9));
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(102, 126, 234, 0.2);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .region-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.2);
        border-color: rgba(102, 126, 234, 0.4);
    }
    
    .region-title {
        color: #667eea;
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Island cards */
    .island-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(248, 250, 252, 0.95));
        border-radius: 15px;
        padding: 1.5rem;
        margin: 0.8rem;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
        border-left: 4px solid;
        transition: all 0.3s ease;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .island-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.6), transparent);
        transition: left 0.5s ease;
    }
    
    .island-card:hover::before {
        left: 100%;
    }
    
    .island-card:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.15);
    }
    
    .island-name {
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .island-info {
        font-size: 0.9rem;
        color: #666;
        line-height: 1.4;
    }
    
    /* Featured island section */
    .featured-island {
        background: linear-gradient(135deg, rgba(79, 172, 254, 0.1), rgba(240, 147, 251, 0.1));
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        border: 2px solid rgba(79, 172, 254, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .featured-island::after {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(79, 172, 254, 0.1) 0%, transparent 70%);
        animation: featuredPulse 8s ease-in-out infinite;
    }
    
    @keyframes featuredPulse {
        0%, 100% { transform: scale(0.8); opacity: 0.5; }
        50% { transform: scale(1.2); opacity: 0.8; }
    }
    
    /* Cultural highlight boxes */
    .culture-highlight {
        background: linear-gradient(135deg, rgba(245, 87, 108, 0.1), rgba(255, 215, 0, 0.1));
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #f5576c;
        box-shadow: 0 5px 15px rgba(245, 87, 108, 0.1);
        position: relative;
    }
    
    .culture-highlight h3 {
        color: #f5576c;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Stats boxes */
    .stats-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .stat-box {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    
    .stat-box:hover {
        transform: translateY(-3px);
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 900;
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        color: #666;
        font-weight: 600;
    }
    
    /* Navigation buttons */
    .nav-button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.8rem 2rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        margin: 0.5rem;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    
    .nav-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, #764ba2, #f093fb);
    }
    
    /* Back button */
    .back-button {
        background: linear-gradient(135deg, #f5576c, #f093fb);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        margin-bottom: 1rem;
    }
    
    .back-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(245, 87, 108, 0.4);
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .caribbean-title {
            font-size: 2.5rem;
        }
        
        .caribbean-subtitle {
            font-size: 1rem;
        }
        
        .main-container {
            margin: 0.5rem;
            padding: 1rem;
        }
        
        .stats-container {
            grid-template-columns: 1fr;
        }
    }
    
    /* Quiz styles */
    .quiz-container {
        background: linear-gradient(135deg, rgba(79, 172, 254, 0.1), rgba(102, 126, 234, 0.1));
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    }
    
    .quiz-question {
        font-size: 1.3rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 1.5rem;
    }
    
    /* Food and culture grid */
    .culture-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .culture-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    
    .culture-card:hover {
        transform: translateY(-5px);
    }
    </style>
    """, unsafe_allow_html=True)

# Load the CSS
load_caribbean_css()

def get_caribbean_daily_fact():
    """Get a daily Caribbean fact"""
    facts = [
        "The Caribbean is home to over 7,000 islands, islets, and cays!",
        "Steel pan music was invented in Trinidad and Tobago in the 1930s!",
        "The Caribbean has produced more Nobel Prize winners per capita than any other region!",
        "Reggae music from Jamaica is recognized by UNESCO as a cultural heritage of humanity!",
        "The Caribbean is the birthplace of rum, invented in Barbados in the 17th century!",
        "Haiti was the first country to abolish slavery and the second to gain independence in the Americas!",
        "The Caribbean has over 13,000 plant species, half of which are found nowhere else!",
        "Carnival celebrations originated in Trinidad and spread throughout the Caribbean!",
        "The Caribbean Sea contains the second-largest barrier reef in the world!",
        "Dominican Republic and Haiti share the island of Hispaniola!",
        "Cuba is the largest Caribbean island, about the size of Pennsylvania!",
        "The word 'Caribbean' comes from the Kalinago people, the region's indigenous inhabitants!"
    ]
    
    day_of_year = datetime.datetime.now().timetuple().tm_yday
    return facts[day_of_year % len(facts)]

def render_header():
    """Render the main header"""
    st.markdown("""
        <div class="caribbean-header">
            <h1 class="caribbean-title">🏝️ Caribbean Cultural Heritage Explorer</h1>
            <p class="caribbean-subtitle">✨ Discover the Rich Tapestry of Caribbean Islands ✨</p>
            <p style="font-size: 1.1rem; margin-top: 1rem; position: relative; z-index: 1;">
                From the Greater Antilles to the Lesser Antilles - explore the diverse cultures, traditions, 
                and heritage of the Caribbean archipelago
            </p>
        </div>
        """, unsafe_allow_html=True)

def render_caribbean_stats():
    """Render Caribbean region statistics"""
    total_islands = sum(len(islands) for islands in CARIBBEAN_ISLANDS.values())
    total_population = "44+ million"  # Approximate
    languages_count = "10+ major languages"
    unesco_sites = sum(1 for region in CARIBBEAN_ISLANDS.values() 
                      for island in region.values() 
                      for site in island.get('unesco_sites', []) if site)
    
    st.markdown(f"""
    <div class="stats-container">
        <div class="stat-box">
            <div class="stat-number">{total_islands}</div>
            <div class="stat-label">Islands Featured</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">{total_population}</div>
            <div class="stat-label">Total Population</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">{languages_count}</div>
            <div class="stat-label">Languages Spoken</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">{unesco_sites}</div>
            <div class="stat-label">UNESCO World Heritage Sites</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_daily_fact():
    """Render the daily Caribbean fact"""
    st.markdown("""
    <div class="culture-highlight">
        <h3>🌟 Caribbean Fact of the Day</h3>
    """, unsafe_allow_html=True)
    
    daily_fact = get_caribbean_daily_fact()
    st.markdown(f"""
        <p><strong>Did you know?</strong> {daily_fact}</p>
        <p style="font-style: italic; color: #666; font-size: 0.9rem;">
            💡 This fact changes daily - come back tomorrow for something new!
        </p>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_island_regions():
    """Render all Caribbean island regions"""
    st.markdown("## 🗺️ Explore Caribbean Regions")
    
    for region_name, islands in CARIBBEAN_ISLANDS.items():
        with st.expander(f"🏝️ {region_name} ({len(islands)} islands)", expanded=True):
            cols = st.columns(min(3, len(islands)))
            
            for idx, (island_name, island_data) in enumerate(islands.items()):
                col_idx = idx % len(cols)
                
                with cols[col_idx]:
                    # Create island card with color coding
                    color = island_data.get('color', '#667eea')
                    
                    if st.button(
                        f"{island_data['flag']} {island_name}",
                        key=f"btn_{island_name}",
                        help=f"Explore {island_name}'s cultural heritage",
                        use_container_width=True
                    ):
                        st.session_state.selected_island = island_name
                        st.session_state.current_view = 'island_detail'
                        st.rerun()
                    
                    st.markdown(f"""
                    <div class="island-card" style="border-left-color: {color};">
                        <div class="island-name">{island_data['flag']} {island_name}</div>
                        <div class="island-info">
                            <strong>Capital:</strong> {island_data['capital']}<br>
                            <strong>Population:</strong> {island_data['population']}<br>
                            <strong>Languages:</strong> {', '.join(island_data['languages'][:2])}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

def render_island_detail(island_name):
    """Render detailed view of a specific island"""
    # Find the island data
    island_data = None
    for region in CARIBBEAN_ISLANDS.values():
        if island_name in region:
            island_data = region[island_name]
            break
    
    if not island_data:
        st.error("Island data not found!")
        return
    
    # Back button
    if st.button("← Back to All Islands", key="back_to_home"):
        st.session_state.current_view = 'home'
        st.session_state.selected_island = None
        st.rerun()
    
    # Island header
    st.markdown(f"""
    <div class="featured-island">
        <h1 style="color: #667eea; font-size: 2.5rem; margin-bottom: 1rem; position: relative; z-index: 1;">
            {island_data['flag']} {island_name}
        </h1>
        <p style="font-size: 1.2rem; color: #333; position: relative; z-index: 1;">
            <strong>Capital:</strong> {island_data['capital']} | 
            <strong>Independence:</strong> {island_data['independence']} | 
            <strong>Population:</strong> {island_data['population']}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different aspects of the island
    tab1, tab2, tab3, tab4 = st.tabs(["🎭 Culture & Traditions", "🍽️ Traditional Food", "👥 Famous People", "🏛️ Heritage Sites"])
    
    with tab1:
        st.markdown("### 🎨 Cultural Highlights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="culture-highlight">
                <h3>🌟 Cultural Treasures</h3>
                <ul>
            """, unsafe_allow_html=True)
            
            for highlight in island_data['culture_highlights']:
                st.markdown(f"<li>{highlight}</li>", unsafe_allow_html=True)
            
            st.markdown("</ul></div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="culture-highlight">
                <h3>🗣️ Languages</h3>
                <p><strong>Official Languages:</strong></p>
                <ul>
            """, unsafe_allow_html=True)
            
            for language in island_data['languages']:
                st.markdown(f"<li>{language}</li>", unsafe_allow_html=True)
            
            st.markdown("</ul></div>", unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 🍽️ Traditional Cuisine")
        
        st.markdown(f"""
        <div class="culture-highlight">
            <h3>🥘 Signature Dishes</h3>
            <div class="culture-grid">
        """, unsafe_allow_html=True)
        
        for food in island_data['traditional_food']:
            st.markdown(f"""
            <div class="culture-card">
                <h4>🍴 {food}</h4>
                <p>A beloved traditional dish that represents the rich culinary heritage of {island_name}.</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### 👥 Notable Figures")
        
        st.markdown(f"""
        <div class="culture-highlight">
            <h3>🌟 Famous People from {island_name}</h3>
        """, unsafe_allow_html=True)
        
        cols = st.columns(2)
        
        for idx, person in enumerate(island_data['famous_people']):
            col_idx = idx % 2
            
            with cols[col_idx]:
                st.markdown(f"""
                <div class="culture-card">
                    <h4>⭐ {person}</h4>
                    <p>A distinguished figure who has brought honor and recognition to {island_name}.</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab4:
        st.markdown("### 🏛️ UNESCO World Heritage Sites")
        
        if island_data['unesco_sites']:
            st.markdown(f"""
            <div class="culture-highlight">
                <h3>🏛️ UNESCO World Heritage Sites</h3>
            """, unsafe_allow_html=True)
            
            for site in island_data['unesco_sites']:
                st.markdown(f"""
                <div class="culture-card">
                    <h4>🏛️ {site}</h4>
                    <p>Recognized by UNESCO for its outstanding universal value to humanity.</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="culture-highlight">
                <h3>🏛️ Heritage Sites</h3>
                <p>While {island_name} may not currently have UNESCO World Heritage Sites, 
                the island is rich in cultural and natural heritage that defines its unique identity.</p>
            </div>
            """, unsafe_allow_html=True)

def render_caribbean_quiz():
    """Render an interactive Caribbean quiz"""
    st.markdown("## 🧠 Caribbean Heritage Quiz")
    
    quiz_questions = [
        {
            "question": "Which Caribbean island is known as the 'Spice Island'?",
            "options": ["Jamaica", "Grenada", "Barbados", "Saint Lucia"],
            "correct": 1,
            "explanation": "Grenada is known as the 'Spice Island' due to its production of nutmeg, mace, cinnamon, and other spices!"
        },
        {
            "question": "Which music genre was invented in Trinidad and Tobago?",
            "options": ["Reggae", "Salsa", "Steel Pan", "Merengue"],
            "correct": 2,
            "explanation": "Steel pan music was invented in Trinidad and Tobago in the 1930s and is now the national instrument!"
        },
        {
            "question": "Which Caribbean country was the first to abolish slavery?",
            "options": ["Jamaica", "Haiti", "Barbados", "Cuba"],
            "correct": 1,
            "explanation": "Haiti was the first country in the world to abolish slavery in 1804 after its successful revolution!"
        },
        {
            "question": "What is the traditional language of Aruba and Curaçao?",
            "options": ["Spanish", "Dutch", "Papiamento", "English"],
            "correct": 2,
            "explanation": "Papiamento is the widely spoken creole language in Aruba, Curaçao, and Bonaire!"
        },
        {
            "question": "Which Caribbean island is famous for Blue Mountain coffee?",
            "options": ["Jamaica", "Puerto Rico", "Dominican Republic", "Haiti"],
            "correct": 0,
            "explanation": "Jamaica's Blue Mountain coffee is considered among the world's finest and most expensive coffees!"
        }
    ]
    
    if not st.session_state.quiz_started:
        st.markdown("""
        <div class="quiz-container">
            <h3>🎯 Test Your Caribbean Knowledge!</h3>
            <p>Challenge yourself with questions about Caribbean culture, history, and traditions.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Start Caribbean Quiz", key="start_quiz", use_container_width=True):
            st.session_state.quiz_started = True
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.rerun()
    
    else:
        if st.session_state.current_question < len(quiz_questions):
            q = quiz_questions[st.session_state.current_question]
            
            st.markdown(f"""
            <div class="quiz-container">
                <p><strong>Question {st.session_state.current_question + 1} of {len(quiz_questions)}</strong></p>
                <div class="quiz-question">{q['question']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            user_answer = st.radio("Choose your answer:", q['options'], key=f"quiz_q_{st.session_state.current_question}")
            
            col1, col2 = st.columns([1, 4])
            
            with col1:
                if st.button("Submit Answer", key=f"submit_{st.session_state.current_question}"):
                    if q['options'].index(user_answer) == q['correct']:
                        st.success(f"✅ Correct! {q['explanation']}")
                        st.session_state.score += 1
                    else:
                        st.error(f"❌ Incorrect. The correct answer is: {q['options'][q['correct']]}. {q['explanation']}")
                    
                    st.session_state.current_question += 1
                    
                    if st.session_state.current_question < len(quiz_questions):
                        if st.button("Next Question ➡️"):
                            st.rerun()
                    else:
                        st.balloons()
                        score_percentage = (st.session_state.score / len(quiz_questions)) * 100
                        
                        if score_percentage >= 80:
                            message = "🏆 Caribbean Culture Expert!"
                        elif score_percentage >= 60:
                            message = "🎯 Caribbean Culture Enthusiast!"
                        else:
                            message = "📚 Keep Learning About the Caribbean!"
                        
                        st.success(f"🎉 Quiz Complete! Your score: {st.session_state.score}/{len(quiz_questions)} - {message}")
                        
                        if st.button("🔄 Restart Quiz"):
                            st.session_state.quiz_started = False
                            st.session_state.current_question = 0
                            st.session_state.score = 0
                            st.rerun()

def render_featured_content():
    """Render featured Caribbean content"""
    st.markdown("## ✨ Featured Caribbean Heritage")
    
    # Featured island of the day (rotates based on date)
    all_islands = []
    for region in CARIBBEAN_ISLANDS.values():
        all_islands.extend(region.keys())
    
    day_of_year = datetime.datetime.now().timetuple().tm_yday
    featured_island_name = all_islands[day_of_year % len(all_islands)]
    
    # Find the featured island data
    featured_island_data = None
    for region in CARIBBEAN_ISLANDS.values():
        if featured_island_name in region:
            featured_island_data = region[featured_island_name]
            break
    
    if featured_island_data:
        st.markdown(f"""
        <div class="featured-island">
            <h3 style="color: #667eea; position: relative; z-index: 1;">
                🌟 Featured Island Today: {featured_island_data['flag']} {featured_island_name}
            </h3>
            <p style="position: relative; z-index: 1;">
                <strong>{featured_island_name}</strong> - {featured_island_data['culture_highlights'][0]}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"🔍 Explore {featured_island_name}", key="explore_featured"):
            st.session_state.selected_island = featured_island_name
            st.session_state.current_view = 'island_detail'
            st.rerun()

def main():
    """Main application function"""
    
    # Load CSS
    load_caribbean_css()
    
    # Container for the entire app
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Handle different views
    if st.session_state.current_view == 'island_detail' and st.session_state.selected_island:
        render_island_detail(st.session_state.selected_island)
    else:
        # Home view
        render_header()
        render_caribbean_stats()
        render_daily_fact()
        render_featured_content()
        render_island_regions()
        render_caribbean_quiz()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #667eea; font-style: italic;">
        <p>🏝️ Caribbean Cultural Heritage Explorer - Celebrating the Diversity of the Caribbean Archipelago 🏝️</p>
        <p><small>Explore • Learn • Celebrate - Built with ❤️ for Caribbean heritage preservation</small></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Run the application
if __name__ == "__main__":
    main()