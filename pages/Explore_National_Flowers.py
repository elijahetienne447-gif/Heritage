import streamlit as st
import json
import pandas as pd
from datetime import datetime
import base64

# Set page configuration
st.set_page_config(
    page_title="Caribbean National Flowers - Cultural Heritage",
    page_icon="🌺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
    }
    
    .flower-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
        border-left: 5px solid #e74c3c;
    }
    
    .island-header {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #f39c12;
    }
    
    .cultural-significance {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #e74c3c;
    }
    
    .traditional-uses {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #27ae60;
    }
    
    .flower-stats {
        background: linear-gradient(135deg, #ffd89b 0%, #19547b 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
    
    .search-highlight {
        background-color: #fff3cd;
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
        border: 1px solid #ffeaa7;
    }
    
    .stSelectbox > div > div > div {
        background-color: rgba(255, 255, 255, 0.8);
    }
</style>
""", unsafe_allow_html=True)

# Caribbean Islands Flowers Database
@st.cache_data
def load_caribbean_flowers_database():
    return {
        # GREATER ANTILLES
        "jamaica_hibiscus": {
            "island": "Jamaica",
            "common_name": "Hibiscus (Lignum Vitae)",
            "scientific_name": "Guaiacum officinale",
            "family": "Zygophyllaceae",
            "description": "Jamaica's national flower is actually the Lignum Vitae, known for its beautiful blue flowers and extremely hard wood. This tree produces small, delicate blue blooms and has been crucial to Jamaican maritime history.",
            "cultural_significance": "The Lignum Vitae represents strength, endurance, and Jamaica's maritime heritage. Its extremely hard wood was used for ship parts, and the tree symbolizes the resilience of the Jamaican people.",
            "traditional_uses": [
                "Traditional medicine for arthritis",
                "Ship building and construction",
                "Cultural ceremonies and national celebrations",
                "Medicinal teas and remedies",
                "Woodworking and crafts",
                "National symbol and pride",
                "Environmental conservation symbol"
            ],
            "colors": ["Blue", "Purple-blue"],
            "blooming_season": "Year-round",
            "habitat": "Dry forests and coastal areas",
            "cultural_festivals": ["Independence Day", "National Tree Day"],
            "medicinal_properties": "Anti-inflammatory, arthritis treatment, skin conditions",
            "symbolism": "Strength, endurance, maritime heritage",
            "image_url": "https://i.pinimg.com/originals/07/49/51/0749510537b42fa53262d66c0cb5b6f6.jpg"
        },
        
        "cuba_mariposa": {
            "island": "Cuba",
            "common_name": "Mariposa (White Ginger)",
            "scientific_name": "Hedychium coronarium",
            "family": "Zingiberaceae",
            "description": "Cuba's national flower, the Mariposa or White Ginger, produces fragrant white flowers that were symbols of rebellion and independence. The flower's pure white color and sweet fragrance made it beloved by Cuban women.",
            "cultural_significance": "The Mariposa became a symbol of Cuban independence and purity during the colonial period. Cuban women wore these flowers as symbols of rebellion against Spanish rule, representing freedom and national identity.",
            "traditional_uses": [
                "Symbol of independence and rebellion",
                "Traditional perfumes and scents",
                "Wedding decorations and ceremonies",
                "Religious and spiritual practices",
                "National celebrations and festivals",
                "Cultural identity expression",
                "Traditional medicine"
            ],
            "colors": ["White", "Cream"],
            "blooming_season": "Year-round",
            "habitat": "Wetlands and tropical gardens",
            "cultural_festivals": ["Independence Day", "José Martí Day"],
            "medicinal_properties": "Digestive aid, aromatherapy, respiratory health",
            "symbolism": "Independence, purity, rebellion, freedom",
            "image_url": "https://helonational.com/wp-content/uploads/2017/01/White-Mariposa-the-national-flower-of-cuba-1140x820.jpg"
        },
        
        "haiti_hibiscus": {
            "island": "Haiti",
            "common_name": "Hibiscus",
            "scientific_name": "Hibiscus rosa-sinensis",
            "family": "Malvaceae",
            "description": "Haiti's national flower is the vibrant red hibiscus, representing the blood of heroes and the beauty of the nation. These large, showy flowers bloom year-round and are deeply embedded in Haitian culture.",
            "cultural_significance": "The red hibiscus symbolizes the courage and sacrifice of Haitian heroes who fought for independence. It represents the blood shed for freedom and the enduring beauty of the Haitian spirit.",
            "traditional_uses": [
                "National celebrations and ceremonies",
                "Traditional medicine and healing",
                "Hair decorations and beauty",
                "Religious ceremonies and offerings",
                "Cultural festivals and parades",
                "Herbal teas and health remedies",
                "Artistic inspiration and crafts"
            ],
            "colors": ["Red", "Pink", "Yellow", "White"],
            "blooming_season": "Year-round",
            "habitat": "Tropical gardens and landscapes",
            "cultural_festivals": ["Independence Day", "Flag Day"],
            "medicinal_properties": "Blood pressure regulation, antioxidant, digestive health",
            "symbolism": "Courage, sacrifice, heroism, beauty",
            "image_url": "https://a-z-animals.com/media/2022/09/shutterstock_410492524-1024x683.jpg"
        },
        
        "dominican_rose": {
            "island": "Dominican Republic",
            "common_name": "Bayahibe Rose",
            "scientific_name": "Pereskia quisqueyana",
            "family": "Cactaceae",
            "description": "The Dominican Republic's national flower is the Bayahibe Rose, a unique cactus flower found only in the country. This rare, beautiful flower represents the unique natural heritage of the Dominican Republic.",
            "cultural_significance": "The Bayahibe Rose symbolizes the Dominican Republic's unique biodiversity and natural beauty. As an endemic species, it represents the country's commitment to environmental conservation and national pride.",
            "traditional_uses": [
                "Environmental conservation symbol",
                "National pride and identity",
                "Tourism promotion",
                "Educational programs",
                "Botanical research",
                "Cultural celebrations",
                "Conservation awareness campaigns"
            ],
            "colors": ["Pink", "White"],
            "blooming_season": "Dry season",
            "habitat": "Coastal areas and dry forests",
            "cultural_festivals": ["Earth Day", "National Flower Day"],
            "medicinal_properties": "Traditional uses in folk medicine",
            "symbolism": "Uniqueness, conservation, national heritage",
            "image_url": "https://thegardengossip.com/wp-content/uploads/2024/04/Untitled-design-1.png"
        },
        
        "puerto_rico_flor": {
            "island": "Puerto Rico",
            "common_name": "Flor de Maga",
            "scientific_name": "Thespesia grandiflora",
            "family": "Malvaceae",
            "description": "Puerto Rico's national flower, the Flor de Maga, is a beautiful red flower that grows on a tree native to the island. The flower opens in the morning and changes color throughout the day.",
            "cultural_significance": "The Flor de Maga represents Puerto Rican resilience and beauty. The flower's ability to bloom after hurricanes and adversity makes it a symbol of the Puerto Rican spirit and recovery.",
            "traditional_uses": [
                "National symbol and pride",
                "Hurricane recovery symbol",
                "Traditional crafts and art",
                "Cultural celebrations",
                "Educational programs",
                "Tourism promotion",
                "Environmental awareness"
            ],
            "colors": ["Red", "Orange-red"],
            "blooming_season": "Year-round",
            "habitat": "Coastal forests and gardens",
            "cultural_festivals": ["Constitution Day", "Discovery Day"],
            "medicinal_properties": "Traditional medicinal uses",
            "symbolism": "Resilience, recovery, Puerto Rican spirit",
            "image_url": "https://a-z-animals.com/media/2022/12/shutterstock_1566085447.jpg"
        },
        
        # LESSER ANTILLES
        "saint_lucia_hibiscus": {
            "island": "Saint Lucia",
            "common_name": "Hibiscus",
            "scientific_name": "Hibiscus rosa-sinensis",
            "family": "Malvaceae",
            "description": "Saint Lucia's national flower, the vibrant hibiscus, blooms year-round and represents the island's tropical beauty and hospitality. These stunning flowers are deeply embedded in Saint Lucian culture.",
            "cultural_significance": "The hibiscus represents beauty, resilience, and the vibrant spirit of Saint Lucia. It symbolizes hospitality and welcome, making it central to the island's tourism and cultural identity.",
            "traditional_uses": [
                "Hair decorations and personal adornment",
                "Traditional ceremonies and festivals",
                "Herbal tea for health benefits",
                "Welcome garlands for visitors",
                "Cultural festivals and parades",
                "Traditional medicine",
                "Tourism promotion"
            ],
            "colors": ["Red", "Pink", "Yellow", "Orange", "White"],
            "blooming_season": "Year-round",
            "habitat": "Gardens, roadsides, tropical landscapes",
            "cultural_festivals": ["Independence Day", "Tourism Week"],
            "medicinal_properties": "Blood pressure regulation, antioxidant properties",
            "symbolism": "Beauty, hospitality, national pride",
            "image_url": "https://c8.alamy.com/comp/BPKTR0/white-hibiscus-st-lucia-caribbean-BPKTR0.jpg"
        },
        
        "barbados_pride": {
            "island": "Barbados",
            "common_name": "Pride of Barbados (Dwarf Poinciana)",
            "scientific_name": "Caesalpinia pulcherrima",
            "family": "Fabaceae",
            "description": "Barbados' national flower is the Pride of Barbados, featuring beautiful orange and red petals with long red stamens. This striking flower blooms almost year-round in tropical climates.",
            "cultural_significance": "The Pride of Barbados represents the island's natural beauty and vibrant culture. Its bright colors reflect the warmth and friendliness of Barbadian people, and it's often used in national celebrations.",
            "traditional_uses": [
                "National celebrations and festivals",
                "Garden landscaping and decoration",
                "Traditional medicine",
                "Cultural ceremonies",
                "Tourism promotion",
                "Educational displays",
                "Natural dyes"
            ],
            "colors": ["Orange", "Red", "Yellow"],
            "blooming_season": "Year-round",
            "habitat": "Tropical gardens and landscapes",
            "cultural_festivals": ["Independence Day", "Crop Over Festival"],
            "medicinal_properties": "Anti-inflammatory, fever reduction, digestive aid",
            "symbolism": "Pride, beauty, tropical warmth",
            "image_url": "https://i.pinimg.com/originals/7f/3d/d7/7f3dd791b8620cdfb83649ba7f6da817.jpg"
        },
        
        "trinidad_chaconia": {
            "island": "Trinidad and Tobago",
            "common_name": "Chaconia (Wild Poinsettia)",
            "scientific_name": "Warszewiczia coccinea",
            "family": "Rubiaceae",
            "description": "Trinidad and Tobago's national flower, the Chaconia, blooms around independence time with brilliant red bracts. This native flower is named after the last Spanish governor of Trinidad.",
            "cultural_significance": "The Chaconia represents Trinidad and Tobago's independence and national sovereignty. Its blooming during independence season makes it a powerful symbol of freedom and national identity.",
            "traditional_uses": [
                "Independence celebrations",
                "National decorations",
                "Cultural festivals",
                "Traditional crafts",
                "Educational programs",
                "Tourism promotion",
                "National identity expression"
            ],
            "colors": ["Red", "Scarlet"],
            "blooming_season": "August-September (Independence season)",
            "habitat": "Mountain forests and cultivated gardens",
            "cultural_festivals": ["Independence Day", "Republic Day"],
            "medicinal_properties": "Traditional uses in folk medicine",
            "symbolism": "Independence, sovereignty, national identity",
            "image_url": "https://i.pinimg.com/originals/bc/9a/56/bc9a56e8461499f41adc36f4088bd571.jpg"
        },
        
        "antigua_dagger": {
            "island": "Antigua and Barbuda",
            "common_name": "Dagger's Log (Agave)",
            "scientific_name": "Agave karatto",
            "family": "Asparagaceae",
            "description": "Antigua and Barbuda's national flower comes from the Dagger's Log or Agave plant, which produces a spectacular tall flowering spike. This drought-resistant plant represents survival and adaptation.",
            "cultural_significance": "The Dagger's Log represents resilience and adaptation to harsh conditions, reflecting the strength of Antiguan and Barbudan people. Its ability to survive droughts symbolizes perseverance.",
            "traditional_uses": [
                "Traditional crafts and rope making",
                "Drought-resistant landscaping",
                "Cultural ceremonies",
                "Traditional medicine",
                "Construction materials",
                "National symbol",
                "Educational purposes"
            ],
            "colors": ["Yellow", "Green-yellow"],
            "blooming_season": "Once in lifetime (after many years)",
            "habitat": "Dry coastal areas and hills",
            "cultural_festivals": ["Independence Day", "Heritage Week"],
            "medicinal_properties": "Traditional uses for wounds and inflammation",
            "symbolism": "Resilience, adaptation, survival",
            "image_url": "https://3.bp.blogspot.com/-oM0Vxq5xEts/W4qS6rd-t6I/AAAAAAAAHcI/OS9_ASKHk08ZjPztpoVXHWBXHjbrFKn6gCLcBGAs/s640/Agave_tripne.com.jpg"
        },
        
        "dominica_bwa": {
            "island": "Dominica",
            "common_name": "Bwa Kwaib (Carib Wood)",
            "scientific_name": "Sabinea carinalis",
            "family": "Rubiaceae",
            "description": "Dominica's national flower, the Bwa Kwaib, is endemic to the island and represents its unique biodiversity. This rare flower is found only in Dominica's mountain forests.",
            "cultural_significance": "The Bwa Kwaib represents Dominica's unique natural heritage and its connection to the indigenous Kalinago (Carib) people. It symbolizes the island's commitment to environmental conservation.",
            "traditional_uses": [
                "Environmental conservation symbol",
                "Indigenous cultural connection",
                "Educational programs",
                "Botanical research",
                "Ecotourism promotion",
                "National pride",
                "Conservation awareness"
            ],
            "colors": ["Pink", "Purple"],
            "blooming_season": "Rainy season",
            "habitat": "Mountain rainforests (endemic)",
            "cultural_festivals": ["Independence Day", "World Environment Day"],
            "medicinal_properties": "Traditional uses by indigenous peoples",
            "symbolism": "Uniqueness, conservation, indigenous heritage",
            "image_url": "https://www.dom767.com/media/2024/10/bwa-kwaib-dominica-national-flower-780x465.webp"
        },
        
        "grenada_bougainvillea": {
            "island": "Grenada",
            "common_name": "Bougainvillea",
            "scientific_name": "Bougainvillea spectabilis",
            "family": "Nyctaginaceae",
            "description": "Grenada's national flower is the colorful bougainvillea, which cascades over walls and fences throughout the Spice Island. These vibrant flowers complement Grenada's reputation for natural beauty.",
            "cultural_significance": "Bougainvillea represents Grenada's vibrant culture and natural beauty. The flower's abundance and variety of colors reflect the island's diversity and warmth of its people.",
            "traditional_uses": [
                "Ornamental landscaping",
                "Cultural decorations",
                "Festival displays",
                "Natural privacy screens",
                "Tourism enhancement",
                "Traditional medicine",
                "Craft activities"
            ],
            "colors": ["Purple", "Pink", "Red", "Orange", "White", "Yellow"],
            "blooming_season": "Year-round",
            "habitat": "Gardens and coastal areas",
            "cultural_festivals": ["Independence Day", "Spice Mas Carnival"],
            "medicinal_properties": "Respiratory health, anti-inflammatory",
            "symbolism": "Vibrancy, beauty, tropical abundance",
            "image_url": "https://i.pinimg.com/474x/c9/38/30/c938305fe2d8a605965624859a0e7292--grenada-bougainvillea.jpg"
        },
        
        "st_vincent_bird": {
            "island": "Saint Vincent and the Grenadines",
            "common_name": "Soufriere Tree (Bird of Paradise)",
            "scientific_name": "Strelitzia reginae",
            "family": "Strelitziaceae",
            "description": "Saint Vincent and the Grenadines' national flower is the striking Bird of Paradise, with its distinctive orange and blue colors resembling a tropical bird in flight.",
            "cultural_significance": "The Bird of Paradise represents the freedom and natural beauty of Saint Vincent and the Grenadines. Its bird-like appearance symbolizes the islands' connection to nature and flight to independence.",
            "traditional_uses": [
                "National celebrations",
                "Tourism promotion",
                "Ornamental gardens",
                "Cultural art and crafts",
                "Hotel landscaping",
                "Photography subjects",
                "Symbol of paradise"
            ],
            "colors": ["Orange", "Blue", "White"],
            "blooming_season": "Year-round with proper care",
            "habitat": "Tropical gardens and landscapes",
            "cultural_festivals": ["Independence Day", "Vincy Mas Carnival"],
            "medicinal_properties": "Primarily ornamental",
            "symbolism": "Freedom, paradise, natural beauty",
            "image_url": "https://i.pinimg.com/736x/79/ba/c9/79bac93bca7d7884c568a237adb0598c.jpg"
        },
        
        "saint_kitts_poinciana": {
            "island": "Saint Kitts and Nevis",
            "common_name": "Poinciana (Flamboyant)",
            "scientific_name": "Delonix regia",
            "family": "Fabaceae",
            "description": "Saint Kitts and Nevis' national flower is the spectacular Poinciana or Flamboyant tree, which produces brilliant red-orange flowers that create a stunning canopy when in bloom.",
            "cultural_significance": "The Poinciana represents the beauty and grandeur of Saint Kitts and Nevis. Its spectacular blooming period symbolizes celebration, pride, and the islands' natural magnificence.",
            "traditional_uses": [
                "Shade tree and landscaping",
                "National celebrations",
                "Cultural festivals",
                "Tourism attraction",
                "Educational programs",
                "Ornamental purposes",
                "Symbol of tropical beauty"
            ],
            "colors": ["Red", "Orange", "Scarlet"],
            "blooming_season": "Dry season (December-May)",
            "habitat": "Parks, streets, and tropical landscapes",
            "cultural_festivals": ["Independence Day", "Culturama"],
            "medicinal_properties": "Traditional uses in folk medicine",
            "symbolism": "Grandeur, celebration, tropical magnificence",
            "image_url": "https://i.pinimg.com/736x/67/9c/6d/679c6daf92ba2c3baceddcf97ba084c5.jpg"
        },
        
        # BAHAMAS
        "bahamas_yellow_elder": {
            "island": "The Bahamas",
            "common_name": "Yellow Elder",
            "scientific_name": "Tecoma stans",
            "family": "Bignoniaceae",
            "description": "The Bahamas' national flower is the bright yellow Yellow Elder, which blooms almost continuously throughout the year. This hardy shrub produces trumpet-shaped golden flowers.",
            "cultural_significance": "The Yellow Elder represents the sunny disposition and resilience of Bahamian people. Its bright yellow color reflects the islands' year-round sunshine and optimistic spirit.",
            "traditional_uses": [
                "National symbol and celebrations",
                "Traditional medicine for diabetes",
                "Landscaping and gardens",
                "Cultural festivals",
                "Herbal remedies",
                "Tourism promotion",
                "Educational programs"
            ],
            "colors": ["Bright yellow", "Golden"],
            "blooming_season": "Year-round",
            "habitat": "Gardens, roadsides, and coastal areas",
            "cultural_festivals": ["Independence Day", "Junkanoo"],
            "medicinal_properties": "Diabetes management, digestive health",
            "symbolism": "Sunshine, optimism, resilience",
            "image_url": "https://www.plantindex.com/wp-content/uploads/2020/07/yellow-elder-bush.jpg"
        }
    }

def main():
    # Load Caribbean flowers database
    flowers_db = load_caribbean_flowers_database()
    
    # Main header
    st.markdown("""
    <div class="main-header">
        <h1>🌺 Caribbean National Flowers 🌺</h1>
        <h3>Cultural Heritage & Traditional Significance Across the Caribbean Islands</h3>
        <p>Exploring the beautiful flowers that define Caribbean culture and tradition from the Greater Antilles to the Lesser Antilles</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for navigation
    st.sidebar.title("🏝️ Navigation")
    
    # Page selection
    page = st.sidebar.selectbox(
        "Choose a section:",
        ["🏠 Home - All Islands", "🏝️ By Island", "🔍 Individual Flower Explorer", "🏛️ Cultural Significance", "📊 Regional Statistics", "💾 Data Export"]
    )
    
    if page == "🏠 Home - All Islands":
        show_all_flowers(flowers_db)
    elif page == "🏝️ By Island":
        show_by_island(flowers_db)
    elif page == "🔍 Individual Flower Explorer":
        show_individual_flower(flowers_db)
    elif page == "🏛️ Cultural Significance":
        show_cultural_significance(flowers_db)
    elif page == "📊 Regional Statistics":
        show_statistics(flowers_db)
    elif page == "💾 Data Export":
        show_data_export(flowers_db)

def show_all_flowers(flowers_db):
    st.title("🏠 All Caribbean National Flowers")
    
    # Search functionality
    search_term = st.text_input("🔍 Search flowers by name, island, or cultural significance:", "")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        islands = list(set([flower['island'] for flower in flowers_db.values()]))
        island_filter = st.multiselect(
            "Filter by island:",
            options=islands,
            default=[]
        )
    
    with col2:
        color_filter = st.multiselect(
            "Filter by available colors:",
            options=list(set([color for flower in flowers_db.values() for color in flower['colors']])),
            default=[]
        )
    
    with col3:
        season_filter = st.selectbox(
            "Filter by blooming season:",
            options=["All seasons"] + list(set([flower['blooming_season'] for flower in flowers_db.values()]))
        )
    
    # Caribbean Statistics
    total_islands = len(set([flower['island'] for flower in flowers_db.values()]))
    total_uses = sum(len(flower['traditional_uses']) for flower in flowers_db.values())
    total_festivals = sum(len(flower['cultural_festivals']) for flower in flowers_db.values())
    
    st.markdown(f"""
    <div class="flower-stats">
        <h3>📊 Caribbean Flowers Database</h3>
        <p><strong>{len(flowers_db)} National Flowers</strong> | 
        <strong>{total_islands} Caribbean Islands</strong> | 
        <strong>{total_uses} Traditional Uses</strong> | 
        <strong>{total_festivals} Cultural Festivals</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    
    # Display flowers based on filters
    filtered_flowers = filter_flowers(flowers_db, search_term, color_filter, season_filter, island_filter)
    
    if not filtered_flowers:
        st.warning("No flowers match your search criteria. Please try different filters.")
        return
    
    # Group by region for better organization
    regions = {
        "Greater Antilles": ["Jamaica", "Cuba", "Haiti", "Dominican Republic", "Puerto Rico"],
        "Lesser Antilles": ["Saint Lucia", "Barbados", "Trinidad and Tobago", "Antigua and Barbuda", 
                          "Dominica", "Grenada", "Saint Vincent and the Grenadines", "Saint Kitts and Nevis"],
        "Bahamas": ["The Bahamas"]
    }
    
    for region, region_islands in regions.items():
        region_flowers = {k: v for k, v in filtered_flowers.items() if v['island'] in region_islands}
        if region_flowers:
            st.markdown(f"## 🏝️ {region}")
            for flower_id, flower in region_flowers.items():
                display_flower_card(flower_id, flower)

def show_by_island(flowers_db):
    st.title("🏝️ Flowers by Caribbean Island")
    
    # Get unique islands
    islands = list(set([flower['island'] for flower in flowers_db.values()]))
    islands.sort()
    
    selected_island = st.selectbox("Choose a Caribbean island:", islands)
    
    if selected_island:
        island_flowers = {k: v for k, v in flowers_db.items() if v['island'] == selected_island}
        
        st.markdown(f"## 🌺 {selected_island}")
        
        if island_flowers:
            for flower_id, flower in island_flowers.items():
                display_detailed_flower_card(flower_id, flower)
        else:
            st.warning(f"No flowers found for {selected_island}")

def show_individual_flower(flowers_db):
    st.title("🔍 Individual Flower Explorer")
    
    # Flower selection
    flower_names = {f"{flower['common_name']} - {flower['island']} ({flower['scientific_name']})": flower_id 
                   for flower_id, flower in flowers_db.items()}
    
    selected_display_name = st.selectbox(
        "Choose a flower to explore in detail:",
        options=list(flower_names.keys())
    )
    
    if selected_display_name:
        flower_id = flower_names[selected_display_name]
        flower = flowers_db[flower_id]
        
        # Display detailed flower information
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.image(flower['image_url'], caption=f"{flower['common_name']} - {flower['island']}", use_container_width=True)
            
            # Basic info
            st.markdown(f"""
            <div class="flower-card">
                <h4>Basic Information</h4>
                <p><strong>Island:</strong> {flower['island']}</p>
                <p><strong>Scientific Name:</strong> <em>{flower['scientific_name']}</em></p>
                <p><strong>Family:</strong> {flower['family']}</p>
                <p><strong>Colors:</strong> {', '.join(flower['colors'])}</p>
                <p><strong>Blooming Season:</strong> {flower['blooming_season']}</p>
                <p><strong>Habitat:</strong> {flower['habitat']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"# 🌺 {flower['common_name']}")
            st.markdown(f"### 🏝️ National flower of {flower['island']}")
            
            # Description
            st.markdown(f"**Description:** {flower['description']}")
            
            # Cultural significance
            st.markdown(f"""
            <div class="cultural-significance">
                <h4>🏛️ Cultural Significance</h4>
                <p>{flower['cultural_significance']}</p>
                <p><strong>Symbolism:</strong> {flower['symbolism']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Traditional uses
            st.markdown(f"""
            <div class="traditional-uses">
                <h4>🌸 Traditional Uses</h4>
                <ul>
                    {''.join([f'<li>{use}</li>' for use in flower['traditional_uses']])}
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Additional information
            col3, col4 = st.columns(2)
            with col3:
                st.markdown("**🎉 Cultural Festivals:**")
                for festival in flower['cultural_festivals']:
                    st.write(f"• {festival}")
            
            with col4:
                st.markdown("**💊 Medicinal Properties:**")
                st.write(flower['medicinal_properties'])

def show_cultural_significance(flowers_db):
    st.title("🏛️ Cultural Significance Across the Caribbean")
    
    st.markdown("""
    This section explores the deep cultural roots and traditional significance of national flowers across the Caribbean islands. 
    Each flower carries unique meanings and plays important roles in their respective island's cultural practices.
    """)
    
    # Create tabs for different cultural aspects
    tab1, tab2, tab3, tab4 = st.tabs(["🎭 Symbolism by Region", "🎉 Cultural Festivals", "💊 Traditional Medicine", "🏝️ Island Identity"])
    
    with tab1:
        st.subheader("Symbolic Meanings Across Caribbean Regions")
        
        # Group by regions
        regions = {
            "Greater Antilles": ["Jamaica", "Cuba", "Haiti", "Dominican Republic", "Puerto Rico"],
            "Lesser Antilles": ["Saint Lucia", "Barbados", "Trinidad and Tobago", "Antigua and Barbuda", 
                              "Dominica", "Grenada", "Saint Vincent and the Grenadines", "Saint Kitts and Nevis"],
            "Bahamas": ["The Bahamas"]
        }
        
        for region, region_islands in regions.items():
            st.markdown(f"### 🏝️ {region}")
            region_flowers = {k: v for k, v in flowers_db.items() if v['island'] in region_islands}
            
            for flower_id, flower in region_flowers.items():
                with st.expander(f"🌺 {flower['common_name']} ({flower['island']}) - {flower['symbolism']}"):
                    st.write(f"**Cultural Significance:** {flower['cultural_significance']}")
    
    with tab2:
        st.subheader("Flowers in Caribbean Cultural Festivals")
        festival_flowers = {}
        for flower_id, flower in flowers_db.items():
            for festival in flower['cultural_festivals']:
                if festival not in festival_flowers:
                    festival_flowers[festival] = []
                festival_flowers[festival].append((flower['island'], flower['common_name'], flower['symbolism']))
        
        for festival, flowers in festival_flowers.items():
            st.markdown(f"**🎉 {festival}**")
            for island, flower_name, symbolism in flowers:
                st.write(f"• {flower_name} ({island}) - {symbolism}")
            st.write("---")
    
    with tab3:
        st.subheader("Traditional Medicinal Uses Across the Caribbean")
        for flower_id, flower in flowers_db.items():
            if flower['medicinal_properties'] != "Primarily ornamental" and flower['medicinal_properties'] != "Traditional uses in folk medicine":
                st.markdown(f"**🌺 {flower['common_name']} ({flower['island']})**")
                st.write(f"Medicinal Properties: {flower['medicinal_properties']}")
                st.write("---")
    
    with tab4:
        st.subheader("Flowers as Symbols of Island Identity")
        identity_themes = {}
        for flower_id, flower in flowers_db.items():
            themes = flower['symbolism'].split(', ')
            for theme in themes:
                theme = theme.strip()
                if theme not in identity_themes:
                    identity_themes[theme] = []
                identity_themes[theme].append((flower['island'], flower['common_name']))
        
        for theme, islands_flowers in identity_themes.items():
            st.markdown(f"**{theme.title()}**")
            for island, flower_name in islands_flowers:
                st.write(f"• {flower_name} ({island})")
            st.write("---")

def show_statistics(flowers_db):
    st.title("📊 Caribbean Flowers Regional Statistics")
    
    # Create dataframe for analysis
    data = []
    for flower_id, flower in flowers_db.items():
        data.append({
            'Flower': flower['common_name'],
            'Island': flower['island'],
            'Scientific_Name': flower['scientific_name'],
            'Family': flower['family'],
            'Number_of_Colors': len(flower['colors']),
            'Number_of_Uses': len(flower['traditional_uses']),
            'Number_of_Festivals': len(flower['cultural_festivals']),
            'Blooming_Season': flower['blooming_season'],
            'Symbolism': flower['symbolism']
        })
    
    df = pd.DataFrame(data)
    
    # Regional grouping
    def assign_region(island):
        greater_antilles = ["Jamaica", "Cuba", "Haiti", "Dominican Republic", "Puerto Rico"]
        lesser_antilles = ["Saint Lucia", "Barbados", "Trinidad and Tobago", "Antigua and Barbuda", 
                          "Dominica", "Grenada", "Saint Vincent and the Grenadines", "Saint Kitts and Nevis"]
        if island in greater_antilles:
            return "Greater Antilles"
        elif island in lesser_antilles:
            return "Lesser Antilles"
        else:
            return "Bahamas"
    
    df['Region'] = df['Island'].apply(assign_region)
    
    # Display overall statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Islands", df['Island'].nunique())
    with col2:
        st.metric("Total Flowers", len(flowers_db))
    with col3:
        st.metric("Total Traditional Uses", df['Number_of_Uses'].sum())
    with col4:
        st.metric("Plant Families", df['Family'].nunique())
    
    # Regional statistics
    st.subheader("📈 Regional Distribution")
    region_stats = df.groupby('Region').agg({
        'Flower': 'count',
        'Number_of_Uses': 'sum',
        'Number_of_Festivals': 'sum'
    }).round(2)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Flowers by Region")
        st.bar_chart(region_stats['Flower'])
    
    with col2:
        st.subheader("Traditional Uses by Region")
        st.bar_chart(region_stats['Number_of_Uses'])
    
    # Charts
    st.subheader("📊 Detailed Analysis")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Traditional Uses per Flower")
        chart_data = df.set_index('Flower')['Number_of_Uses']
        st.bar_chart(chart_data)
    
    with col2:
        st.subheader("Colors Available per Flower")
        chart_data = df.set_index('Flower')['Number_of_Colors']
        st.bar_chart(chart_data)
    
    # Family distribution
    st.subheader("Distribution by Plant Family")
    family_counts = df['Family'].value_counts()
    st.bar_chart(family_counts)
    
    # Blooming seasons
    st.subheader("Blooming Seasons Distribution")
    season_counts = df['Blooming_Season'].value_counts()
    st.bar_chart(season_counts)
    
    # Display the dataframe
    st.subheader("📋 Complete Caribbean Flowers Database")
    st.dataframe(df, use_container_width=True)

def show_data_export(flowers_db):
    st.title("💾 Data Export")
    
    st.markdown("""
    Export the complete Caribbean flowers database in various formats for use in chatbots, 
    research, educational purposes, or other applications.
    """)
    
    export_format = st.selectbox(
        "Choose export format:",
        ["JSON", "CSV", "Text Summary", "Regional Summary"]
    )
    
    if export_format == "JSON":
        json_data = json.dumps(flowers_db, indent=2)
        st.code(json_data, language='json')
        
        # Download button
        st.download_button(
            label="📥 Download JSON",
            data=json_data,
            file_name=f"caribbean_flowers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    elif export_format == "CSV":
        # Create CSV data
        data = []
        for flower_id, flower in flowers_db.items():
            data.append({
                'ID': flower_id,
                'Island': flower['island'],
                'Common_Name': flower['common_name'],
                'Scientific_Name': flower['scientific_name'],
                'Family': flower['family'],
                'Description': flower['description'],
                'Cultural_Significance': flower['cultural_significance'],
                'Traditional_Uses': '; '.join(flower['traditional_uses']),
                'Colors': ', '.join(flower['colors']),
                'Blooming_Season': flower['blooming_season'],
                'Habitat': flower['habitat'],
                'Cultural_Festivals': ', '.join(flower['cultural_festivals']),
                'Medicinal_Properties': flower['medicinal_properties'],
                'Symbolism': flower['symbolism']
            })
        
        df = pd.DataFrame(data)
        csv_data = df.to_csv(index=False)
        
        st.dataframe(df, use_container_width=True)
        
        # Download button
        st.download_button(
            label="📥 Download CSV",
            data=csv_data,
            file_name=f"caribbean_flowers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    elif export_format == "Text Summary":
        summary_text = "CARIBBEAN NATIONAL FLOWERS - CULTURAL HERITAGE SUMMARY\n"
        summary_text += "=" * 70 + "\n\n"
        
        # Group by regions
        regions = {
            "GREATER ANTILLES": ["Jamaica", "Cuba", "Haiti", "Dominican Republic", "Puerto Rico"],
            "LESSER ANTILLES": ["Saint Lucia", "Barbados", "Trinidad and Tobago", "Antigua and Barbuda", 
                              "Dominica", "Grenada", "Saint Vincent and the Grenadines", "Saint Kitts and Nevis"],
            "BAHAMAS": ["The Bahamas"]
        }
        
        for region, region_islands in regions.items():
            summary_text += f"{region}\n" + "-" * len(region) + "\n\n"
            
            region_flowers = {k: v for k, v in flowers_db.items() if v['island'] in region_islands}
            for flower_id, flower in region_flowers.items():
                summary_text += f"{flower['island']}: {flower['common_name']} ({flower['scientific_name']})\n"
                summary_text += f"Symbolism: {flower['symbolism']}\n"
                summary_text += f"Cultural Significance: {flower['cultural_significance'][:150]}...\n"
                summary_text += f"Traditional Uses: {', '.join(flower['traditional_uses'][:3])}...\n"
                summary_text += "\n"
            summary_text += "\n"
        
        st.text_area("Caribbean Flowers Summary", summary_text, height=600)
        
        # Download button
        st.download_button(
            label="📥 Download Text Summary",
            data=summary_text,
            file_name=f"caribbean_flowers_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )
    
    elif export_format == "Regional Summary":
        regional_data = create_regional_summary(flowers_db)
        st.markdown("### 🏝️ Caribbean Regional Summary")
        st.text_area("Regional Summary", regional_data, height=600)
        
        # Download button
        st.download_button(
            label="📥 Download Regional Summary",
            data=regional_data,
            file_name=f"caribbean_regional_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )

def create_regional_summary(flowers_db):
    """Create a regional summary of Caribbean flowers"""
    regions = {
        "GREATER ANTILLES": ["Jamaica", "Cuba", "Haiti", "Dominican Republic", "Puerto Rico"],
        "LESSER ANTILLES": ["Saint Lucia", "Barbados", "Trinidad and Tobago", "Antigua and Barbuda", 
                          "Dominica", "Grenada", "Saint Vincent and the Grenadines", "Saint Kitts and Nevis"],
        "BAHAMAS": ["The Bahamas"]
    }
    
    summary = "CARIBBEAN FLOWERS BY REGION\n"
    summary += "=" * 40 + "\n\n"
    
    for region, islands in regions.items():
        summary += f"{region} ({len(islands)} islands)\n"
        summary += "-" * (len(region) + len(f" ({len(islands)} islands)")) + "\n"
        
        region_flowers = {k: v for k, v in flowers_db.items() if v['island'] in islands}
        
        # Common themes in the region
        all_symbolism = []
        all_uses = []
        for flower in region_flowers.values():
            all_symbolism.extend(flower['symbolism'].split(', '))
            all_uses.extend(flower['traditional_uses'])
        
        from collections import Counter
        common_themes = Counter(all_symbolism).most_common(3)
        common_uses = Counter(all_uses).most_common(3)
        
        summary += f"Common Cultural Themes: {', '.join([theme for theme, count in common_themes])}\n"
        summary += f"Popular Traditional Uses: {', '.join([use for use, count in common_uses])}\n\n"
        
        for flower in region_flowers.values():
            summary += f"• {flower['island']}: {flower['common_name']} - {flower['symbolism']}\n"
        
        summary += "\n\n"
    
    return summary

def display_flower_card(flower_id, flower):
    """Display a flower card with all information"""
    
    st.markdown(f"""
    <div class="island-header">
        <h4>🏝️ {flower['island']}</h4>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image(flower['image_url'], caption=f"{flower['common_name']} - {flower['island']}", use_container_width=True)
    
    with col2:
        st.markdown(f"### 🌺 {flower['common_name']}")
        st.markdown(f"*{flower['scientific_name']}* | Family: {flower['family']}")
        
        # Colors and season
        st.markdown(f"**Colors:** {', '.join(flower['colors'])} | **Season:** {flower['blooming_season']}")
        
        # Description
        st.markdown(f"**Description:** {flower['description'][:200]}...")
        
        # Cultural significance in colored box
        st.markdown(f"""
        <div class="cultural-significance">
            <strong>🏛️ Cultural Significance:</strong><br>
            {flower['cultural_significance'][:200]}...
        </div>
        """, unsafe_allow_html=True)
        
        # Expandable traditional uses
        with st.expander("🌸 View Traditional Uses"):
            for use in flower['traditional_uses']:
                st.write(f"• {use}")
        
        # Quick info
        st.markdown(f"**Symbolism:** {flower['symbolism']}")
    
    st.markdown("---")

def display_detailed_flower_card(flower_id, flower):
    """Display a detailed flower card for single island view"""
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image(flower['image_url'], caption=flower['common_name'], use_container_width=True)
        
        # Basic info
        st.markdown(f"""
        <div class="flower-card">
            <h4>Basic Information</h4>
            <p><strong>Scientific Name:</strong> <em>{flower['scientific_name']}</em></p>
            <p><strong>Family:</strong> {flower['family']}</p>
            <p><strong>Colors:</strong> {', '.join(flower['colors'])}</p>
            <p><strong>Blooming Season:</strong> {flower['blooming_season']}</p>
            <p><strong>Habitat:</strong> {flower['habitat']}</p>
            <p><strong>Symbolism:</strong> {flower['symbolism']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"# 🌺 {flower['common_name']}")
        
        # Description
        st.markdown(f"**Description:** {flower['description']}")
        
        # Cultural significance
        st.markdown(f"""
        <div class="cultural-significance">
            <h4>🏛️ Cultural Significance</h4>
            <p>{flower['cultural_significance']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Traditional uses
        st.markdown(f"""
        <div class="traditional-uses">
            <h4>🌸 Traditional Uses</h4>
            <ul>
                {''.join([f'<li>{use}</li>' for use in flower['traditional_uses']])}
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Additional information
        col3, col4 = st.columns(2)
        with col3:
            st.markdown("**🎉 Cultural Festivals:**")
            for festival in flower['cultural_festivals']:
                st.write(f"• {festival}")
        
        with col4:
            st.markdown("**💊 Medicinal Properties:**")
            st.write(flower['medicinal_properties'])
    
    st.markdown("---")

def filter_flowers(flowers_db, search_term, color_filter, season_filter, island_filter):
    """Filter flowers based on search criteria"""
    filtered = {}
    
    for flower_id, flower in flowers_db.items():
        # Text search
        if search_term:
            search_text = f"{flower['common_name']} {flower['scientific_name']} {flower['island']} {flower['description']} {flower['cultural_significance']}".lower()
            if search_term.lower() not in search_text:
                continue
        
        # Island filter
        if island_filter and flower['island'] not in island_filter:
            continue
        
        # Color filter
        if color_filter:
            if not any(color in flower['colors'] for color in color_filter):
                continue
        
        # Season filter
        if season_filter != "All seasons" and flower['blooming_season'] != season_filter:
            continue
        
        filtered[flower_id] = flower
    
    return filtered

if __name__ == "__main__":
    main()