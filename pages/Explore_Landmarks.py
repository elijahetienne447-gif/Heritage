# --- Page Configuration ---
import streamlit as st
from PIL import Image
from typing import List, Optional, Dict, Any
import requests
from io import BytesIO

# --- Custom CSS for Caribbean Cultural Heritage Theme ---
st.markdown("""
<style>
    /* Main background with gradient inspired by Caribbean waters */
    .stApp {
        background: linear-gradient(135deg, 
            #1e3a8a 0%, #2563eb 15%, #0ea5e9 30%, 
            #06b6d4 45%, #10b981 60%, #f59e0b 75%, 
            #dc2626 90%, #7c3aed 100%);
        background-attachment: fixed;
    }
    
    /* Main container styling */
    .main .block-container {
        background: rgba(255, 255, 255, 0.96);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
        backdrop-filter: blur(15px);
        border: 2px solid rgba(255, 255, 255, 0.3);
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    
    /* Header styling */
    h1 {
        color: #1e40af;
        text-align: center;
        font-family: 'Georgia', serif;
        font-weight: bold;
        text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.2);
        margin-bottom: 2rem;
        background: linear-gradient(45deg, #1e40af, #059669, #f59e0b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem;
    }
    
    /* Site card styling */
    .stContainer > div {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border-radius: 15px;
        border: 2px solid #10b981;
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.25);
        padding: 1.5rem;
        margin: 1.5rem 0;
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #059669, #10b981, #34d399);
        color: white;
        border: none;
        border-radius: 30px;
        padding: 0.75rem 2rem;
        font-weight: bold;
        font-size: 1rem;
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
        transition: all 0.4s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Stats cards */
    .stats-card {
        background: linear-gradient(135deg, #fef7cd 0%, #fde68a 100%);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        border: 2px solid #f59e0b;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.2);
    }
    
    /* Caribbean heritage divider */
    .caribbean-divider {
        height: 4px;
        background: linear-gradient(90deg, 
            #1e40af, #0ea5e9, #10b981, #f59e0b, 
            #dc2626, #7c3aed, #ec4899);
        border-radius: 3px;
        margin: 3rem 0;
    }
    
    /* Image placeholder styling */
    .site-placeholder {
        background: linear-gradient(135deg, #0ea5e9, #10b981);
        color: white;
        padding: 2rem;
        text-align: center;
        border-radius: 10px;
        font-weight: bold;
        height: 150px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    /* Image styling */
    .heritage-image {
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        object-fit: cover;
        width: 100%;
        height: 150px;
    }
</style>
""", unsafe_allow_html=True)

# --- Session State Initialization ---
if 'page' not in st.session_state:
    st.session_state.page = 'explore'
if 'selected_island' not in st.session_state:
    st.session_state.selected_island = 'Saint Lucia'
if 'current_site_data' not in st.session_state:
    st.session_state.current_site_data = None

# --- Helper Classes ---
class MediaLink:
    def __init__(self, title: str, url: str, media_type: str):
        self.title = title
        self.url = url
        self.media_type = media_type

# --- Helper Functions ---
def load_image_from_url(url: str) -> Optional[Image.Image]:
    """Load image from URL with error handling."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        return img
    except Exception as e:
        st.error(f"Could not load image: {e}")
        return None

def go_to_explore():
    """Navigate back to the explore page."""
    st.session_state.page = 'explore'
    st.session_state.current_site_data = None
    st.rerun()

def create_caribbean_divider():
    """Create a decorative divider with Caribbean colors."""
    st.markdown('<div class="caribbean-divider"></div>', unsafe_allow_html=True)

def display_site_card(site_data, island_name):
    """Create a visual card for a heritage site with actual images."""
    with st.container(border=True):
        col1, col2 = st.columns([1, 3])
        
        # Left column - Image or placeholder
        with col1:
            if 'image_url' in site_data and site_data['image_url']:
                try:
                    # Try to load and display the actual image
                    img = load_image_from_url(site_data['image_url'])
                    if img:
                        st.image(img, caption=site_data['title'], use_container_width=True)
                    else:
                        # Fallback to placeholder if image fails to load
                        st.markdown(f"""
                        <div class="site-placeholder">
                            <div style='font-size: 2rem; margin-bottom: 0.5rem;'>🏛️</div>
                            <div style='font-size: 0.9rem; line-height: 1.2;'>{site_data['title']}</div>
                            <div style='font-size: 0.8rem; opacity: 0.8; margin-top: 0.5rem;'>📍 {island_name}</div>
                        </div>
                        """, unsafe_allow_html=True)
                except:
                    # Fallback to placeholder if there's any error
                    st.markdown(f"""
                    <div class="site-placeholder">
                        <div style='font-size: 2rem; margin-bottom: 0.5rem;'>🏛️</div>
                        <div style='font-size: 0.9rem; line-height: 1.2;'>{site_data['title']}</div>
                        <div style='font-size: 0.8rem; opacity: 0.8; margin-top: 0.5rem;'>📍 {island_name}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                # Default placeholder when no image URL is available
                st.markdown(f"""
                <div class="site-placeholder">
                    <div style='font-size: 2rem; margin-bottom: 0.5rem;'>🏛️</div>
                    <div style='font-size: 0.9rem; line-height: 1.2;'>{site_data['title']}</div>
                    <div style='font-size: 0.8rem; opacity: 0.8; margin-top: 0.5rem;'>📍 {island_name}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Right column - Site information
        with col2:
            st.markdown(f"### 🏛️ {site_data['title']}")
            st.markdown(f"**📍 {site_data['location']}**")
            if 'year_built' in site_data:
                st.markdown(f"**🗓️ Built: {site_data['year_built']}**")
            st.write(site_data["description"])
            
            # Explore button
            if st.button("🔍 Explore Site", key=f"explore_{island_name}_{site_data['title']}"):
                st.session_state.page = 'site_details'
                st.session_state.current_site_data = {**site_data, 'island': island_name}
                st.rerun()

# --- COMPREHENSIVE CARIBBEAN ISLANDS DATA ---
caribbean_islands_data = {
    "Saint Lucia": {
        "flag": "🇱🇨",
        "capital": "Castries",
        "sites": {
            "fort_rodney": {
                "title": "Fort Rodney",
                "location": "Pigeon Island",
                "year_built": "1778",
                "description": "Built by the British in 1778, Fort Rodney offers panoramic views of the island and played a crucial role in naval battles during the colonial period.",
                "coordinates": "14.0912526,-60.96685",
                "image_url":"https://i.ytimg.com/vi/Ahwid-yrPFw/maxresdefault.jpg",
            },
            "diamond_falls": {
                "title": "Diamond Falls Botanical Gardens",
                "location": "Soufrière",
                "year_built": "1785",
                "description": "A natural wonder featuring lush tropical gardens, mineral baths, and the famous Diamond Falls waterfall with its rainbow-colored minerals.",
                "coordinates": "13.8531522,-61.0489541",
                "image_url":"https://media.tacdn.com/media/attractions-content--1x-1/0b/2c/f9/01.jpg",
            },
            "the_pitons": {
                "title": "The Pitons",
                "location": "Soufrière",
                "description": "UNESCO World Heritage Site featuring two volcanic spires - Gros Piton and Petit Piton. These iconic landmarks are symbols of Saint Lucia.",
                "coordinates": "13.8033167,-61.0669688",
                "image_url":"https://images.fineartamerica.com/images/artworkimages/mediumlarge/2/the-pitons-st-lucia-tom-till.jpg",
            },
            "walcott_house": {
                "title": "Walcott House",
                "location": "Castries",
                "description": "The childhood home of Sir Derek Walcott, Nobel Laureate in Literature, now a museum celebrating Caribbean literary heritage.",
                "coordinates": "14.0074632,-60.987796",
                "image_url":"https://www.govt.lc/media.govt.lc/www/pressroom/news/walcott-place-project.jpg",
            }
        }
    },
    
    "Jamaica": {
        "flag": "🇯🇲",
        "capital": "Kingston",
        "sites": {
            "port_royal": {
                "title": "Port Royal",
                "location": "Kingston Harbour",
                "year_built": "1655",
                "description": "Once known as the 'wickedest city on earth', this former pirate haven was partially destroyed by an earthquake in 1692. Now a UNESCO World Heritage Site.",
                "coordinates": "17.9390,-76.8416",
                "image_url":"https://img.marinas.com/v2/3f2968d41486cc4a5a241afc255782ac6e7f2987b8585f4ff08f7ef1e9e52858.jpg",
            },
            "rose_hall": {
                "title": "Rose Hall Great House",
                "location": "Montego Bay",
                "year_built": "1750s",
                "description": "A restored plantation house famous for the legend of Annie Palmer, the 'White Witch'. Offers insights into Jamaica's colonial and plantation history.",
                "coordinates": "18.5101,-77.9120",
                "image_url":"https://jamaicans.com/wp-content/uploads/2016/10/Rose-Hall-Jamaica.jpg",
            },
            "blue_mountains": {
                "title": "Blue Mountains",
                "location": "Eastern Jamaica",
                "description": "UNESCO World Heritage Site known for coffee production and as the hideout of Maroon communities who fought against slavery.",
                "coordinates": "18.0447,-76.7134",
                "image_url":"https://ran-s3.s3.amazonaws.com/pripsjamaica.com/s3fs-public/images/places/blue-mountains-jamaica-caribbean-cables.jpg",
            },
            "spanish_town": {
                "title": "Spanish Town",
                "location": "St. Catherine Parish",
                "year_built": "1534",
                "description": "Former capital of Jamaica under Spanish rule, featuring colonial architecture and the Cathedral Church of St. James.",
                "coordinates": "17.9910,-76.9574",
                "image_url":"https://i.pinimg.com/originals/41/8f/8b/418f8b4dc429b553d273fc7491965678.jpg",
            }
        }
    },
    
    "Barbados": {
        "flag": "🇧🇧",
        "capital": "Bridgetown",
        "sites": {
            "bridgetown": {
                "title": "Historic Bridgetown",
                "location": "St. Michael Parish",
                "year_built": "1628",
                "description": "UNESCO World Heritage Site featuring well-preserved British colonial architecture and the Parliament Buildings.",
                "coordinates": "13.0969,-59.6145",
                "image_url":"https://i.pinimg.com/originals/88/eb/ea/88ebea285b2b366ddc4bac36b162ae37.jpg",
            },
            "garrison": {
                "title": "The Garrison",
                "location": "St. Michael Parish",
                "year_built": "1780s",
                "description": "UNESCO World Heritage Site - largest and most intact historic garrison in the Caribbean, showcasing British military heritage.",
                "coordinates": "13.0840,-59.6202",
                "image_url":"https://www.bookislandtours.com/images/Barbados/Garrison/Historic_Garrison_Tour_ITP_740_X497_2.png",
            },
            "st_nicholas_abbey": {
                "title": "St. Nicholas Abbey",
                "location": "St. Peter Parish",
                "year_built": "1658",
                "description": "One of the oldest plantation houses in the Caribbean, featuring Jacobean architecture and rum production facilities.",
                "coordinates": "13.2847,-59.6234",
                "image_url":"https://www.fleewinter.com/wp-content/uploads/2018/05/St-Nicholas-Abbey-Barbados-1.jpg",
            },
            "mount_gay_distillery": {
                "title": "Mount Gay Distillery",
                "location": "St. Michael Parish",
                "year_built": "1703",
                "description": "The world's oldest rum distillery, offering insights into Caribbean rum production and trade history.",
                "coordinates": "13.1776,-59.5412",
                "image_url":"https://www.thewanderlusteffect.com/wp-content/uploads/2019/02/rsz_10785931840_img_0841.jpg",
            }
        }
    },
    
    "Trinidad and Tobago": {
        "flag": "🇹🇹",
        "capital": "Port of Spain",
        "sites": {
            "fort_george": {
                "title": "Fort George",
                "location": "Port of Spain",
                "year_built": "1804",
                "description": "Historic fort offering panoramic views of Port of Spain and the Gulf of Paria, built during the British colonial period.",
                "coordinates": "10.6918,-61.5281",
                "image_url":"https://www.destinationtnt.com/wp-content/uploads/fs_fort-king-george-P10305981.jpg",
            },
            "red_house": {
                "title": "Red House",
                "location": "Port of Spain",
                "year_built": "1907",
                "description": "The seat of Parliament, rebuilt after the 1903 water riots. An important symbol of Trinidad's political development.",
                "coordinates": "10.6522,-61.5053",
                "image_url":"https://s1.stabroeknews.com/images/2020/01/redhouse.jpg",
            },
            "pitch_lake": {
                "title": "Pitch Lake",
                "location": "La Brea",
                "description": "The world's largest natural asphalt lake, used by indigenous peoples for centuries and later by colonial powers.",
                "coordinates": "10.2329,-61.6275",
                "image_url":"https://www.destinationtnt.com/wp-content/uploads/fs_pitch-lake-5308162890_63c497fb5c_o.jpg",
            },
            "temple_sea": {
                "title": "Temple in the Sea",
                "location": "Waterloo",
                "year_built": "1947",
                "description": "A Hindu temple built in the sea by one man as a labor of love, representing the Indo-Caribbean cultural heritage.",
                "coordinates": "10.5167,-61.6000",
                "image_url":"https://ourplanetimages.com/wp-content/uploads/2020/06/Temple-in-the-Sea-Waterloo-Trinidad-2.jpg",
            }
        }
    },
    
    "Dominican Republic": {
        "flag": "🇩🇴",
        "capital": "Santo Domingo",
        "sites": {
            "zona_colonial": {
                "title": "Zona Colonial",
                "location": "Santo Domingo",
                "year_built": "1496",
                "description": "UNESCO World Heritage Site - the first permanent European settlement in the Americas, featuring the oldest cathedral and university in the New World.",
                "coordinates": "18.4734,-69.8786",
                "image_url":"https://i.pinimg.com/originals/0d/7a/2e/0d7a2ec91daa86364a05af4e8121ddc8.jpg",
            },
            "alcazar_colon": {
                "title": "Alcázar de Colón",
                "location": "Santo Domingo",
                "year_built": "1514",
                "description": "Former residence of Diego Columbus, son of Christopher Columbus. Now a museum showcasing colonial life.",
                "coordinates": "18.4741,-69.8822",
                "image_url":"https://i.pinimg.com/originals/da/2a/8f/da2a8f64646458e5683f9b7c4a7d6afc.jpg",
            },
            "fortaleza_ozama": {
                "title": "Fortaleza Ozama",
                "location": "Santo Domingo",
                "year_built": "1502",
                "description": "The oldest fortress in the Americas, built to protect the entrance to the Ozama River and Santo Domingo.",
                "coordinates": "18.4732,-69.8794",
                "image_url":"https://thumbs.dreamstime.com/b/fortaleza-ozama-fortress-santo-domingo-dominican-republic-52630038.jpg",
            },
            "cathedral_primada": {
                "title": "Catedral Primada",
                "location": "Santo Domingo",
                "year_built": "1540",
                "description": "The oldest cathedral in the Americas, where Christopher Columbus's remains were once housed.",
                "coordinates": "18.4737,-69.8816",
                "image_url":"https://photos.wikimapia.org/p/00/03/30/67/26_full.jpg",
            }
        }
    },
    
    "Cuba": {
        "flag": "🇨🇺",
        "capital": "Havana",
        "sites": {
            "old_havana": {
                "title": "Old Havana",
                "location": "Havana",
                "year_built": "1519",
                "description": "UNESCO World Heritage Site featuring the largest and best-preserved colonial center in Latin America.",
                "coordinates": "23.1367,-82.3589",
                "image_url":"https://havanatourcompany.com/wp-content/uploads/2016/06/morro-castle-cuba-1.jpg",
            },
            "el_morro": {
                "title": "El Morro Castle",
                "location": "Havana",
                "year_built": "1589",
                "description": "Fortress guarding the entrance to Havana Bay, part of the Old Havana UNESCO World Heritage Site.",
                "coordinates": "23.1514,-82.3670",
                "image_url":"https://boricuaonline.com/wp-content/uploads/2020/09/ElMorroSanJuan05.jpg",
            },
            "trinidad": {
                "title": "Trinidad",
                "location": "Sancti Spíritus Province",
                "year_built": "1514",
                "description": "UNESCO World Heritage Site - a perfectly preserved colonial city with cobblestone streets and pastel buildings.",
                "coordinates": "21.8020,-79.9847",
                "image_url":"https://expertvagabond.com/wp-content/uploads/trinidad-cuba-travel-guide.jpg",
            },
            "valley_ingenios": {
                "title": "Valley of the Sugar Mills",
                "location": "Near Trinidad",
                "year_built": "18th-19th century",
                "description": "UNESCO World Heritage Site showcasing the remains of sugar plantations and slave quarters.",
                "coordinates": "21.8333,-79.9167",
                 "image_url":"https://lacgeo.com/sites/default/files/valle_de_los_ingenios_trinidad_cuba_opt%20(1).jpg",
            }
        }
    },
    
    "Puerto Rico": {
        "flag": "🇵🇷",
        "capital": "San Juan",
        "sites": {
            "old_san_juan": {
                "title": "Old San Juan",
                "location": "San Juan",
                "year_built": "1521",
                "description": "UNESCO World Heritage Site featuring colorful colonial buildings, forts, and the oldest executive mansion in continuous use in the New World.",
                "coordinates": "18.4655,-66.1057",
                "image_url":"https://drscdn.500px.org/photo/8775729/q%3D80_m%3D2000/v2?webp=true&sig=7c0aa3b6230ca23cc63801605ff86a8beaf951f93aebf83348594a4450ff5a34",
            },
            "el_morro_pr": {
                "title": "Castillo San Felipe del Morro",
                "location": "San Juan",
                "year_built": "1539",
                "description": "UNESCO World Heritage Site - a 16th-century fortress protecting San Juan Bay.",
                "coordinates": "18.4708,-66.1239",
                "image_url":"https://boricuaonline.com/wp-content/uploads/2020/09/ElMorroSanJuan05.jpg",
            },
            "san_cristobal": {
                "title": "Castillo San Cristóbal",
                "location": "San Juan",
                "year_built": "1783",
                "description": "UNESCO World Heritage Site - the largest fortification built by the Spanish in the New World.",
                "coordinates": "18.4697,-66.1017",
                "image_url":"https://img.marinas.com/v2/1a6d2f666463e4912e0f4ebfe451bb91c81a3f861421b14a02639607839a1e6a.jpg",
            },
            "camuy_caves": {
                "title": "Camuy Caves",
                "location": "Camuy",
                "description": "Ancient cave system used by the Taíno people, featuring impressive stalactites and underground rivers.",
                "coordinates": "18.4833,-66.8667",
                "image_url":"https://live.staticflickr.com/6220/6326192725_19bd53da44_b.jpg",
            }
        }
    },
    
    "Haiti": {
        "flag": "🇭🇹",
        "capital": "Port-au-Prince",
        "sites": {
            "citadelle_laferriere": {
                "title": "Citadelle Laferrière",
                "location": "Nord Department",
                "year_built": "1805",
                "description": "UNESCO World Heritage Site - massive fortress built by Henri Christophe after Haitian independence, symbol of freedom.",
                "coordinates": "19.5833,-72.2333",
                "image_url":"https://www.lunionsuite.com/wp-content/uploads/2015/07/citadelle_laferriere_haiti__3_.jpg",
            },
            "sans_souci_palace": {
                "title": "Sans-Souci Palace",
                "location": "Milot",
                "year_built": "1813",
                "description": "UNESCO World Heritage Site - ruins of the royal palace of King Henri Christophe, showcasing post-independence grandeur.",
                "coordinates": "19.6167,-72.2167",
                "image_url":"https://visithaiti.com/wp-content/uploads/2019/04/ruins-sans-souci-palace-milot-angelo-miramonti.jpg",
            },
            "jacmel": {
                "title": "Jacmel Historic District",
                "location": "Jacmel",
                "year_built": "18th-19th century",
                "description": "Well-preserved colonial architecture with Victorian-era iron balconies and colorful buildings.",
                "coordinates": "18.2347,-72.5342",
                "image_url":"https://i.pinimg.com/originals/3e/6a/05/3e6a05268b08b3c65f22a3656ff06fe5.jpg",
            }
        }
    },
    
    "Bahamas": {
        "flag": "🇧🇸",
        "capital": "Nassau",
        "sites": {
            "fort_charlotte": {
                "title": "Fort Charlotte",
                "location": "Nassau",
                "year_built": "1787",
                "description": "The largest fort in Nassau, built by Lord Dunmore and named after Queen Charlotte. Features dungeons and historical exhibits.",
                "coordinates": "25.0661,-77.3744",
                "image_url":"https://l450v.alamy.com/450v/gegg3r/view-of-fort-george-st-georges-grenada-gegg3r.jpg",
            },
            "queens_staircase": {
                "title": "Queen's Staircase",
                "location": "Nassau",
                "year_built": "1790s",
                "description": "66-step limestone staircase carved by slaves, leading to Fort Fincastle and named in honor of Queen Victoria.",
                "coordinates": "25.0778,-77.3361",
                "image_url":"https://l450v.alamy.com/450v/gegg3r/view-of-fort-george-st-georges-grenada-gegg3r.jpg",
            },
            "pompey_museum": {
                "title": "Pompey Museum",
                "location": "Nassau",
                "year_built": "1769",
                "description": "Former slave market turned museum documenting the history of slavery and emancipation in the Bahamas.",
                "coordinates": "25.0811,-77.3425",
                "image_url":"https://l450v.alamy.com/450v/gegg3r/view-of-fort-george-st-georges-grenada-gegg3r.jpg",
            }
        }
    },
    
    "Antigua and Barbuda": {
        "flag": "🇦🇬",
        "capital": "St. John's",
        "sites": {
            "nelsons_dockyard": {
                "title": "Nelson's Dockyard",
                "location": "English Harbour",
                "year_built": "1725",
                "description": "UNESCO World Heritage Site - the world's only continuously working Georgian dockyard, named after Admiral Horatio Nelson.",
                "coordinates": "17.0057,-61.7609",
                "image_url":"https://c8.alamy.com/comp/M62YN6/nelsons-dockyard-antigua-M62YN6.jpg",
            },
            "shirley_heights": {
                "title": "Shirley Heights",
                "location": "English Harbour",
                "year_built": "1787",
                "description": "Military fortification offering spectacular views and hosting famous Sunday sunset parties with live music.",
                "coordinates": "17.0072,-61.7544",
                "image_url":"https://www.sandals.com/blog/content/images/2023/05/Shirley-Heights-Antigua-Top-View.jpg",
            },
            "st_johns_cathedral": {
                "title": "St. John's Cathedral",
                "location": "St. John's",
                "year_built": "1847",
                "description": "Anglican cathedral built with baroque twin towers, replacing earlier churches destroyed by earthquakes.",
                "coordinates": "17.1210,-61.8449",
                "image_url":"https://www.encirclephotos.com/wp-content/uploads/Antigua-St-John-s-St-John-s-Cathedral.jpg",
            }
        }
    },
    
    "Grenada": {
        "flag": "🇬🇩",
        "capital": "St. George's",
        "sites": {
            "fort_george": {
                "title": "Fort George",
                "location": "St. George's",
                "year_built": "1705",
                "description": "Historic fort overlooking St. George's harbour, built by the French and later expanded by the British.",
                "coordinates": "12.0571,-61.7549",
                "image_url":"https://l450v.alamy.com/450v/gegg3r/view-of-fort-george-st-georges-grenada-gegg3r.jpg",

            },
            "grand_etang": {
                "title": "Grand Etang National Park",
                "location": "Interior Grenada",
                "description": "Crater lake surrounded by rainforest, significant to indigenous Carib culture and biodiversity.",
                "coordinates": "12.0942,-61.7300",
                "image_url":"https://i.pinimg.com/originals/c1/8e/29/c18e29dd06d5c1ac52d7359746ce6e6e.jpg",

            }
        }
    },
    
    "St. Vincent and the Grenadines": {
        "flag": "🇻🇨",
        "capital": "Kingstown",
        "sites": {
            "fort_charlotte_svg": {
                "title": "Fort Charlotte",
                "location": "Kingstown",
                "year_built": "1806",
                "description": "Hilltop fortress built by the British, offering panoramic views and housing a museum of Black Carib history.",
                "coordinates": "13.1567,-61.2278",
                "image_url":"https://i.pinimg.com/originals/80/25/35/802535921bc1d1534d8ba38da7fe0d46.jpg",

            },
            "botanical_gardens": {
                "title": "St. Vincent Botanical Gardens",
                "location": "Kingstown",
                "year_built": "1765",
                "description": "One of the oldest botanical gardens in the Western Hemisphere, featuring breadfruit trees from Captain Bligh's voyage.",
                "coordinates": "13.1561,-61.2244",
                "image_url":"https://media-cdn.tripadvisor.com/media/photo-s/17/d7/71/eb/botanical-gardens.jpg",

            }
        }
    },
    
    "St. Kitts and Nevis": {
        "flag": "🇰🇳",
        "capital": "Basseterre",
        "sites": {
            "brimstone_hill": {
                "title": "Brimstone Hill Fortress",
                "location": "St. Kitts",
                "year_built": "1690-1790",
                "description": "UNESCO World Heritage Site - the 'Gibraltar of the West Indies', a massive fortress complex built by enslaved Africans.",
                "coordinates": "17.3667,-62.8000",
                "image_url":"https://image.yachtcharterfleet.com/w1200/h779/qh/ca/keb9bc319/directory/profile/photo/1027132.jpg",
            },
            "independence_square": {
                "title": "Independence Square",
                "location": "Basseterre",
                "year_built": "1790s",
                "description": "Historic town square originally used for slave auctions, now a symbol of freedom and independence.",
                "coordinates": "17.2955,-62.7258",
                "image_url": "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/06/1e/b6/48/independence-square.jpg?w=1200&h=-1&s=1",
            }
        }
    },
    
    "Dominica": {
        "flag": "🇩🇲",
        "capital": "Roseau",
        "sites": {
            "carib_territory": {
                "title": "Kalinago Territory",
                "location": "Eastern Dominica",
                "description": "Home to the Kalinago (Carib) people, the last remaining indigenous community in the Caribbean, preserving ancient traditions.",
                "coordinates": "15.3833,-61.2000",
                "image_url": "https://www.onair.news/wp-content/uploads/2022/09/domv2-2-800x534.jpg",
            },
            "fort_shirley": {
                "title": "Fort Shirley",
                "location": "Portsmouth",
                "year_built": "1774",
                "description": "Restored 18th-century British garrison within Cabrits National Park, offering insights into colonial military history.",
                "coordinates": "15.5833,-61.4667",
                "image_url": "https://c8.alamy.com/comp/D6KCW7/old-british-fort-shirley-dominica-west-indies-caribbean-central-america-D6KCW7.jpg",
            }
        }
    },
    
    "Martinique": {
        "flag": "🇫🇷",
        "capital": "Fort-de-France",
        "sites": {
            "saint_pierre": {
                "title": "Saint-Pierre",
                "location": "Northern Martinique",
                "year_built": "1635",
                "description": "Former 'Paris of the Caribbean' destroyed by Mount Pelée in 1902, now a museum city showcasing volcanic archaeology.",
                "coordinates": "14.7500,-61.1667",
                "image_url": "https://cdn1.matadornetwork.com/blogs/1/2019/07/Saint-Pierre-panorama-1-1200x853.jpg",
            },
            "fort_saint_louis": {
                "title": "Fort Saint-Louis",
                "location": "Fort-de-France",
                "year_built": "1640",
                "description": "Active French naval base and historic fort protecting the capital's harbor for over 380 years.",
                "coordinates": "14.6058,-61.0639",
                "image_url": "https://carnetdetipiment.com/wp-content/uploads/fort7.png",
            }
        }
    },
    
    "Guadeloupe": {
        "flag": "🇫🇷",
        "capital": "Basse-Terre",
        "sites": {
            "fort_delgres": {
                "title": "Fort Delgrès",
                "location": "Basse-Terre",
                "year_built": "1650",
                "description": "Historic fort named after Louis Delgrès, who fought against the reestablishment of slavery in 1802.",
                "coordinates": "15.9950,-61.7319",
                "image_url": "https://www.cg971.fr/wp-content/uploads/2017/06/maxresdefault-1024x576.jpg",
            },
            "memorial_acte": {
                "title": "Mémorial ACTe",
                "location": "Pointe-à-Pitre",
                "year_built": "2015",
                "description": "Caribbean Center of Expression and Memory of Slave Trade and Slavery, built on the site of a former sugar factory.",
                "coordinates": "16.2333,-61.5333",
                "image_url": "https://www.lebleulagon.com/wp-content/uploads/2015/05/memorial-acte-vacance-guadeloupe-960x636.jpg",
            }
        }
    },
    
    "Aruba": {
        "flag": "🇦🇼",
        "capital": "Oranjestad",
        "sites": {
            "alto_vista_chapel": {
                "title": "Alto Vista Chapel",
                "location": "Noord",
                "year_built": "1750",
                "description": "Historic Catholic chapel built by Spanish missionaries, rebuilt in 1952, symbolizing Aruba's religious heritage.",
                "coordinates": "12.5667,-70.0333",
                "image_url": "https://b2090723.smushcdn.com/2090723/wp-content/uploads/2018/05/AUAaltovista_H.jpg?lossy=0&strip=0&webp=1",
            },
            "fort_zoutman": {
                "title": "Fort Zoutman",
                "location": "Oranjestad",
                "year_built": "1798",
                "description": "Oldest structure in Aruba, built by the Dutch for defense and now housing the Historical Museum.",
                "coordinates": "12.5167,-70.0333",
                "image_url": "https://cdn.fischer.cz/Images/000417/fort-zoutman-0_1200x0.jpg",
            }
        }
    },
    
    "Curaçao": {
        "flag": "🇨🇼",
        "capital": "Willemstad",
        "sites": {
            "willemstad": {
                "title": "Historic Willemstad",
                "location": "Willemstad",
                "year_built": "1634",
                "description": "UNESCO World Heritage Site featuring colorful Dutch colonial architecture and the famous floating bridge.",
                "coordinates": "12.1091,-68.9320",
                "image_url": "https://travelingcanucks.com/wp-content/uploads/2017/04/willemstad-curacao-24.jpg",
            },
            "kura_hulanda": {
                "title": "Kura Hulanda Museum",
                "location": "Willemstad",
                "year_built": "1999",
                "description": "Museum documenting the African diaspora and slave trade history in restored 18th-century buildings.",
                "coordinates": "12.1167,-68.9333",
                "image_url": "https://www.kurahulandavillage.com/wp-content/uploads/2023/05/kura-hulanda-museum.webp",
            }
        }
    },
    
    "Bonaire": {
        "flag": "🇧🇶",
        "capital": "Kralendijk",
        "sites": {
            "slave_huts": {
                "title": "Salt Slave Huts",
                "location": "Southern Bonaire",
                "year_built": "1850s",
                "description": "Small stone huts where enslaved workers lived while harvesting salt, now preserved as a memorial to their suffering.",
                "coordinates": "12.0167,-68.2833",
                "image_url": "https://lh4.ggpht.com/-At8CAXcXx-o/VNh9ZYGWhEI/AAAAAAAA_TM/ffOUHoEuXi4/bonaire-slave-huts-2%25255B2%25255D.jpg?imgmax=800",
            },
            "rincon": {
                "title": "Rincon Village",
                "location": "Central Bonaire",
                "year_built": "1527",
                "description": "Oldest settlement in Bonaire, showcasing traditional Caribbean architecture and cultural heritage.",
                "coordinates": "12.1500,-68.3333",
                "image_url": "https://3.bp.blogspot.com/-9BxxHxsr3d8/WWi0bSbA9KI/AAAAAAAAONY/-0ALjv-DmHo9LiJ1jE0ESNUbGf3ohZLcwCLcBGAs/s1600/Rincon%2BBON%2B2017%2B%25284%2529%2BBlog.jpg",
            }
        }
    }
}

# --- PAGE FUNCTIONS ---
def show_island_selector():
    """Display island selection interface with stats."""
    st.markdown("### 🏝️ Select a Caribbean Island to Explore")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        island_names = list(caribbean_islands_data.keys())
        selected_island = st.selectbox(
            "Choose an island:",
            island_names,
            index=island_names.index(st.session_state.selected_island) if st.session_state.selected_island in island_names else 0,
            key="island_selector"
        )
        
        if selected_island != st.session_state.selected_island:
            st.session_state.selected_island = selected_island
            st.rerun()
    
    with col2:
        island_data = caribbean_islands_data[st.session_state.selected_island]
        st.markdown(f"""
        <div class="stats-card">
            <h2>{island_data['flag']}</h2>
            <h4>{st.session_state.selected_island}</h4>
            <p><strong>Capital:</strong> {island_data['capital']}</p>
            <p><strong>Heritage Sites:</strong> {len(island_data['sites'])}</p>
        </div>
        """, unsafe_allow_html=True)

def show_explore_page():
    """Displays the main explore page with island selector and site cards."""
    st.markdown("""
    <h1>🌴 Caribbean Cultural Heritage Explorer 🏛️</h1>
    <p style='text-align: center; font-size: 1.3rem; color: #059669; font-style: italic; margin-bottom: 2rem;'>
    Discover the rich history, culture, and natural beauty across all Caribbean islands
    </p>
    """, unsafe_allow_html=True)
    
    create_caribbean_divider()
    
    # Island selector
    show_island_selector()
    
    create_caribbean_divider()
    
    # Display sites for selected island
    selected_island_data = caribbean_islands_data[st.session_state.selected_island]
    
    st.markdown(f"""
    <h2>🏛️ Heritage Sites in {st.session_state.selected_island} {selected_island_data['flag']}</h2>
    <p style='font-size: 1.1rem; color: #374151; text-align: center; margin-bottom: 2rem;'>
    Explore {len(selected_island_data['sites'])} carefully curated cultural heritage sites
    </p>
    """, unsafe_allow_html=True)
    
    # Create cards for all sites
    for site_key, site_data in selected_island_data['sites'].items():
        display_site_card(site_data, st.session_state.selected_island)

def show_site_details_page(site_data):
    """Displays the details page for a specific site with actual images."""
    # Back button
    if st.button("← Back to Heritage Explorer", key="back_button"):
        go_to_explore()
    
    # Page header with island context
    island_data = caribbean_islands_data[site_data['island']]
    st.markdown(f"""
    <h1>🏛️ {site_data['title']}</h1>
    <p style='text-align: center; font-size: 1.4rem; color: #059669; font-weight: bold; margin-bottom: 1rem;'>
    📍 {site_data['location']}, {site_data['island']} {island_data['flag']}
    </p>
    """, unsafe_allow_html=True)
    
    if 'year_built' in site_data:
        st.markdown(f"""
        <p style='text-align: center; font-size: 1.1rem; color: #374151; margin-bottom: 2rem;'>
        🗓️ Built: <strong>{site_data['year_built']}</strong>
        </p>
        """, unsafe_allow_html=True)
    
    create_caribbean_divider()
    
    # Site image - Load actual image
    if 'image_url' in site_data and site_data['image_url']:
        try:
            img = load_image_from_url(site_data['image_url'])
            if img:
                st.image(img, caption=f"{site_data['title']} - {site_data['location']}", use_column_width=True)
            else:
                # Fallback to placeholder if image fails to load
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #0ea5e9, #10b981, #f59e0b); 
                            color: white; padding: 4rem; text-align: center; 
                            border-radius: 15px; font-size: 1.5rem; font-weight: bold;
                            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2); margin: 2rem 0;'>
                    🏛️<br>{site_data['title']}<br>
                    <small style='font-size: 1rem; opacity: 0.9;'>📍 {site_data['location']}, {site_data['island']}</small>
                </div>
                """, unsafe_allow_html=True)
        except:
            # Fallback to placeholder if there's any error
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #0ea5e9, #10b981, #f59e0b); 
                        color: white; padding: 4rem; text-align: center; 
                        border-radius: 15px; font-size: 1.5rem; font-weight: bold;
                        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2); margin: 2rem 0;'>
                🏛️<br>{site_data['title']}<br>
                <small style='font-size: 1rem; opacity: 0.9;'>📍 {site_data['location']}, {site_data['island']}</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        # Default placeholder when no image URL is available
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #0ea5e9, #10b981, #f59e0b); 
                    color: white; padding: 4rem; text-align: center; 
                    border-radius: 15px; font-size: 1.5rem; font-weight: bold;
                    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2); margin: 2rem 0;'>
            🏛️<br>{site_data['title']}<br>
            <small style='font-size: 1rem; opacity: 0.9;'>📍 {site_data['location']}, {site_data['island']}</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Site description
    st.markdown("### 📖 About This Heritage Site")
    st.write(site_data["description"])
    
    create_caribbean_divider()
    
    # Navigation button
    if 'coordinates' in site_data:
        coords = site_data['coordinates']
        map_url = f"https://www.google.com/maps/search/{site_data['title']}/@{coords},15z"
        st.link_button("🗺️ Get Directions to Site", map_url, use_container_width=True)

# --- MAIN APP LOGIC ---
def main():
    """Main application logic controlling page navigation."""
    if st.session_state.page == 'explore':
        show_explore_page()
    elif st.session_state.page == 'site_details':
        if st.session_state.current_site_data:
            show_site_details_page(st.session_state.current_site_data)
        else:
            go_to_explore()

# Run the application
if __name__ == "__main__":
    main()