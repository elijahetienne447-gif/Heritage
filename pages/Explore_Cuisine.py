import streamlit as st
import pandas as pd
from typing import Dict, List, Any

# Configure Streamlit page
st.set_page_config(
    page_title="Complete Caribbean Culinary Heritage",
    page_icon="🌴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #ff6b35, #e74c3c, #e91e63);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .dish-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #ff6b35;
    }
    .dish-image {
        width: 100%;
        height: 200px;
        object-fit: cover;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .national-dish {
        background: linear-gradient(135deg, #dc3545, #c82333);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 1rem;
    }
    .ingredient-tag {
        background: #e8f5e8;
        color: #2d5a2d;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        margin: 0.2rem;
        display: inline-block;
    }
    .cooking-step {
        background: #f8f9fa;
        border-left: 4px solid #ff6b35;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 5px;
    }
    .cultural-note {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 8px;
        padding: 1rem;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

class CompleteCaribbeanCuisineApp:
    def __init__(self):
        self.cuisine_data = {
            'jamaica': {
                'name': 'Jamaica',
                'flag': '🇯🇲',
                'region': 'Greater Antilles',
                'cultural_intro': "Jamaican cuisine reflects our motto 'Out of Many, One People' through bold flavors and vibrant spices.",
                'dishes': {
                    'jerk_chicken': {
                        'name': 'Jerk Chicken',
                        'description': "Jamaica's most iconic dish featuring scotch bonnet peppers, allspice, and aromatic spices.",
                        'ingredients': ['Chicken', 'Scotch bonnet peppers', 'Allspice', 'Thyme', 'Garlic', 'Ginger', 'Brown sugar'],
                        'cooking_instructions': ['Blend spices into marinade', 'Marinate chicken overnight', 'Grill over pimento wood'],
                        'cultural_note': "Developed by Maroons, represents resistance and survival.",
                        'meal_type': 'Main Course', 'difficulty': 'Moderate', 'is_national': True,
                        'image_url': 'https://www.sandals.com/blog/content/images/2020/04/Jamaican-Jerk-Chicken.jpg'
                    },
                    'ackee_saltfish': {
                        'name': 'Ackee and Saltfish',
                        'description': "National dish combining ackee fruit with salted cod.",
                        'ingredients': ['Ackee', 'Salt cod', 'Onions', 'Tomatoes', 'Scotch bonnet pepper'],
                        'cooking_instructions': ['Boil and flake salt cod', 'Clean and boil ackee', 'Sauté vegetables', 'Combine gently'],
                        'cultural_note': "Ackee brought from West Africa, now synonymous with Jamaican identity.",
                        'meal_type': 'Breakfast', 'difficulty': 'Moderate', 'is_national': True,
                        'image_url': 'https://i0.wp.com/chinese-jamaicangirl.com/wp-content/uploads/2018/07/image-2.jpeg?fit=3264%2C2448&ssl=1'
                    },
                    'curry_goat': {
                        'name': 'Curry Goat',
                        'description': "Tender goat meat slow-cooked in aromatic curry spices.",
                        'ingredients': ['Goat meat', 'Curry powder', 'Onions', 'Garlic', 'Ginger', 'Scotch bonnet'],
                        'cooking_instructions': ['Season and brown meat', 'Add curry powder', 'Slow cook until tender'],
                        'cultural_note': "Brought by Indian indentured workers, now a Jamaican staple.",
                        'meal_type': 'Main Course', 'difficulty': 'Moderate', 'is_national': False,
                        'image_url': 'https://travelandmunchies.com/wp-content/uploads/2022/11/IMG_4514.jpg'
                    }
                }
            },
            'trinidad_tobago': {
                'name': 'Trinidad and Tobago',
                'flag': '🇹🇹',
                'region': 'Lesser Antilles',
                'cultural_intro': "Trinidadian cuisine celebrates multicultural fusion with vibrant street food culture.",
                'dishes': {
                    'doubles': {
                        'name': 'Doubles',
                        'description': "Iconic street food with curried chickpeas between fried bread.",
                        'ingredients': ['Chickpeas', 'Flour', 'Turmeric', 'Curry powder', 'Yeast'],
                        'cooking_instructions': ['Make bara dough', 'Cook spiced chickpeas', 'Fry bara', 'Assemble sandwich'],
                        'cultural_note': "Created by Indian immigrants, became Trinidad's most iconic street food.",
                        'meal_type': 'Breakfast', 'difficulty': 'Moderate', 'is_national': True,
                        'image_url': 'https://www.vmcdn.ca/f/files/guelphtoday/images/community-leaders-program-clp/20210527-doubles-of-trinidad-submitted.jpg;w=960'
                    },
                    'pelau': {
                        'name': 'Pelau',
                        'description': "One-pot rice dish with pigeon peas and caramelized sugar.",
                        'ingredients': ['Rice', 'Pigeon peas', 'Chicken', 'Coconut milk', 'Brown sugar'],
                        'cooking_instructions': ['Caramelize sugar', 'Brown meat', 'Add rice and peas', 'Simmer until tender'],
                        'cultural_note': "Sunday tradition showcasing African 'burning sugar' technique.",
                        'meal_type': 'Main Course', 'difficulty': 'Moderate', 'is_national': False,
                        'image_url': 'https://cookingwithria.com/wp-content/uploads/2015/02/Trinidad-Pelau.jpg'
                    },
                    'roti': {
                        'name': 'Roti and Curry',
                        'description': "Indian flatbread served with various curried meats and vegetables.",
                        'ingredients': ['Flour', 'Baking powder', 'Curry chicken', 'Potatoes', 'Channa'],
                        'cooking_instructions': ['Make roti dough', 'Roll and cook on tawa', 'Prepare curry filling', 'Wrap and serve'],
                        'cultural_note': "Brought by Indian indentured laborers, adapted with local ingredients.",
                        'meal_type': 'Main Course', 'difficulty': 'Moderate', 'is_national': False,
                        'image_url': 'https://i.pinimg.com/originals/93/fd/67/93fd67bd8dca1b24af7b45d8db61d2d9.jpg'
                    }
                }
            },
            'barbados': {
                'name': 'Barbados',
                'flag': '🇧🇧',
                'region': 'Lesser Antilles',
                'cultural_intro': "Bajan cuisine blends British colonial influences with African traditions and fresh seafood.",
                'dishes': {
                    'cou_cou_flying_fish': {
                        'name': 'Cou-Cou and Flying Fish',
                        'description': "National dish with cornmeal-okra pudding and seasoned flying fish.",
                        'ingredients': ['Flying fish', 'Cornmeal', 'Okra', 'Onions', 'Lime juice'],
                        'cooking_instructions': ['Season fish', 'Steam okra', 'Cook cornmeal mixture', 'Fry fish and serve'],
                        'cultural_note': "Celebrates seasonal flying fish migration through Barbadian waters.",
                        'meal_type': 'Main Course', 'difficulty': 'Moderate', 'is_national': True,
                        'image_url': 'https://www.sandals.com/blog/content/images/2018/06/10985177_456624651157268_1207301172591549039_n.jpg'
                    },
                    'fish_cakes': {
                        'name': 'Fish Cakes',
                        'description': "Popular street food fritters made with salted cod.",
                        'ingredients': ['Salt cod', 'Flour', 'Baking powder', 'Onions', 'Scotch bonnet'],
                        'cooking_instructions': ['Soak and flake fish', 'Make batter', 'Deep fry until golden'],
                        'cultural_note': "Traditional breakfast food enjoyed at local festivals.",
                        'meal_type': 'Snack', 'difficulty': 'Easy', 'is_national': False,
                        'image_url': 'https://loopbarbados.com/sites/default/files/styles/blog_temporary_670/public/blogimages/Fish%20Cakes%20Barbados.jpg?itok=fLexmoqT'
                    }
                }
            },
            'cuba': {
                'name': 'Cuba',
                'flag': '🇨🇺',
                'region': 'Greater Antilles',
                'cultural_intro': "Cuban cuisine blends Spanish colonial, African, and indigenous Taíno influences.",
                'dishes': {
                    'ropa_vieja': {
                        'name': 'Ropa Vieja',
                        'description': "National dish of shredded beef in tomato-based sauce.",
                        'ingredients': ['Flank steak', 'Tomatoes', 'Bell peppers', 'Onions', 'Garlic'],
                        'cooking_instructions': ['Slow-cook beef until tender', 'Shred meat', 'Sauté vegetables', 'Combine and simmer'],
                        'cultural_note': "Legend of a man whose wife transformed leftover scraps into delicious meal.",
                        'meal_type': 'Main Course', 'difficulty': 'Moderate', 'is_national': True,
                        'image_url': 'https://www.lemonblossoms.com/wp-content/uploads/2020/09/Cuban-Ropa-Vieja-S2.jpg'
                    },
                    'moros_y_cristianos': {
                        'name': 'Moros y Cristianos',
                        'description': "Black beans and rice symbolizing cultural harmony.",
                        'ingredients': ['Black beans', 'White rice', 'Onions', 'Garlic', 'Bay leaves'],
                        'cooking_instructions': ['Cook beans with aromatics', 'Make sofrito', 'Combine with rice'],
                        'cultural_note': "Represents unity and blending of cultures.",
                        'meal_type': 'Main Course', 'difficulty': 'Easy', 'is_national': False,
                        'image_url':'https://dfcasacubana.com/wp-content/uploads/2023/09/moros-y-cristianos.jpg'
                    },
                    'lechon': {
                        'name': 'Lechón',
                        'description': "Whole roasted pig seasoned with mojo marinade.",
                        'ingredients': ['Whole pig', 'Garlic', 'Sour orange juice', 'Oregano', 'Cumin'],
                        'cooking_instructions': ['Marinate overnight', 'Slow roast over coals', 'Baste regularly'],
                        'cultural_note': "Centerpiece of Cuban celebrations and festivals.",
                        'meal_type': 'Main Course', 'difficulty': 'Challenging', 'is_national': False,
                        'image_url': 'https://www.formerchef.com/wp-content/uploads/2011/05/cubanporkshredded2.jpg'
                    }
                }
            },
            'puerto_rico': {
                'name': 'Puerto Rico',
                'flag': '🇵🇷',
                'region': 'Greater Antilles',
                'cultural_intro': "Puerto Rican cocina criolla fuses Taíno, Spanish, and African influences.",
                'dishes': {
                    'mofongo': {
                        'name': 'Mofongo',
                        'description': "Fried plantains mashed with garlic and chicharrón.",
                        'ingredients': ['Green plantains', 'Garlic', 'Chicharrón', 'Olive oil', 'Salt'],
                        'cooking_instructions': ['Fry plantains', 'Mash with garlic in pilón', 'Form bowl shape', 'Fill with protein'],
                        'cultural_note': "Pilón connects to Taíno ancestors and food preparation methods.",
                        'meal_type': 'Main Course', 'difficulty': 'Moderate', 'is_national': True,
                        'image_url': 'https://www.thespruceeats.com/thmb/sfQuxa_mlgakbvyHJJZ6oiRfKTU=/4133x3000/filters:no_upscale():max_bytes(150000):strip_icc()/traditional-mofongo-recipe-2138186-hero-02-34e5355c68b34f4ab0e1d797cc9d18cf.jpg'
                    },
                    'pasteles': {
                        'name': 'Pasteles',
                        'description': "Traditional tamales made with plantain and root vegetables.",
                        'ingredients': ['Green plantains', 'Yautía', 'Pork', 'Sofrito', 'Plantain leaves'],
                        'cooking_instructions': ['Grate vegetables', 'Season filling', 'Wrap in leaves', 'Boil for hours'],
                        'cultural_note': "Christmas tradition requiring family cooperation to prepare.",
                        'meal_type': 'Main Course', 'difficulty': 'Challenging', 'is_national': False,
                        'image_url': 'https://i.pinimg.com/originals/b8/3f/ff/b83fff248e900aea1e613f3610ec163d.jpg'
                    }
                }
            },
            'dominican_republic': {
                'name': 'Dominican Republic',
                'flag': '🇩🇴',
                'region': 'Greater Antilles',
                'cultural_intro': "Dominican cuisine blends Taíno, Spanish, and African heritage with fresh ingredients.",
                'dishes': {
                    'la_bandera': {
                        'name': 'La Bandera',
                        'description': "National dish of rice, red beans, and meat representing the flag.",
                        'ingredients': ['White rice', 'Red beans', 'Chicken', 'Onions', 'Garlic'],
                        'cooking_instructions': ['Cook beans until tender', 'Season meat', 'Prepare rice', 'Serve together'],
                        'cultural_note': "Daily meal representing national identity and balanced nutrition.",
                        'meal_type': 'Main Course', 'difficulty': 'Easy', 'is_national': True,
                        'image_url': 'https://s.yimg.com/ny/api/res/1.2/PTkOJPwV2I_D2RJCifrEuw--/YXBwaWQ9aGlnaGxhbmRlcjt3PTEyNDI7aD02OTk-/https://media.zenfs.com/en/travel_noire_articles_954/8f16e24c6f0cb98a21567ee746cbbf6d'
                    },
                    'mangu': {
                        'name': 'Mangú',
                        'description': "Creamy mashed plantains topped with caramelized onions.",
                        'ingredients': ['Green plantains', 'Onions', 'Olive oil', 'Salt', 'Butter'],
                        'cooking_instructions': ['Boil plantains', 'Mash with butter', 'Caramelize onions', 'Top and serve'],
                        'cultural_note': "Rooted in Taíno heritage, beloved breakfast tradition.",
                        'meal_type': 'Breakfast', 'difficulty': 'Easy', 'is_national': False,
                        'image_url': 'https://aseasonedgreeting.com/wp-content/uploads/2020/03/Mangu-with-pickled-red-onions.jpg'
                    }
                }
            },
            'haiti': {
                'name': 'Haiti',
                'flag': '🇭🇹',
                'region': 'Greater Antilles',
                'cultural_intro': "Haitian cuisine reflects revolutionary spirit and African heritage with French influences.",
                'dishes': {
                    'griot': {
                        'name': 'Griot',
                        'description': "Marinated pork shoulder, slow-cooked then fried until crispy.",
                        'ingredients': ['Pork shoulder', 'Sour orange juice', 'Garlic', 'Thyme', 'Scotch bonnet'],
                        'cooking_instructions': ['Marinate overnight', 'Slow cook until tender', 'Fry until crispy'],
                        'cultural_note': "Represents French influence while maintaining Haitian flavors.",
                        'meal_type': 'Main Course', 'difficulty': 'Moderate', 'is_national': True,
                        'image_url': 'https://travelandmunchies.com/wp-content/uploads/2023/04/IMG_9311-scaled.jpg'
                    },
                    'soup_joumou': {
                        'name': 'Soup Joumou',
                        'description': "Independence soup with pumpkin, traditionally eaten on New Year's Day.",
                        'ingredients': ['Pumpkin', 'Beef', 'Pasta', 'Cabbage', 'Carrots'],
                        'cooking_instructions': ['Cook and puree pumpkin', 'Prepare beef broth', 'Combine with vegetables', 'Add pasta'],
                        'cultural_note': "UNESCO heritage soup symbolizing freedom from slavery.",
                        'meal_type': 'Main Course', 'difficulty': 'Moderate', 'is_national': False,
                        'image_url': 'https://www.newsamericasnow.com/wp-content/uploads/2018/08/Soup-Joumou-recipe-haiti.jpg'
                    }
                }
            },
            'saint_lucia': {
                'name': 'Saint Lucia',
                'flag': '🇱🇨',
                'region': 'Lesser Antilles',
                'cultural_intro': "Saint Lucian cuisine fuses Kalinago, African, French, and British influences.",
                'dishes': {
                    'green_fig_saltfish': {
                        'name': 'Green Fig and Saltfish',
                        'description': "National dish combining green bananas with flaked salt cod.",
                        'ingredients': ['Green bananas', 'Salt cod', 'Onions', 'Bell peppers', 'Thyme'],
                        'cooking_instructions': ['Soak and flake cod', 'Boil bananas', 'Sauté aromatics', 'Combine ingredients'],
                        'cultural_note': "Reflects island resourcefulness and fishing heritage.",
                        'meal_type': 'Main Course', 'difficulty': 'Moderate', 'is_national': True,
                        'image_url': 'https://www.196flavors.com/wp-content/uploads/2015/10/Green-fig-and-saltfish-2-FP.jpg'
                    },
                    'bouyon': {
                        'name': 'Bouyon',
                        'description': "One-pot stew with mixed meats, ground provisions, and dumplings.",
                        'ingredients': ['Mixed meats', 'Ground provisions', 'Dumplings', 'Carrots', 'Herbs'],
                        'cooking_instructions': ['Brown meats', 'Add provisions', 'Include vegetables', 'Drop dumplings'],
                        'cultural_note': "Sunday family gathering dish representing communal spirit.",
                        'meal_type': 'Main Course', 'difficulty': 'Moderate', 'is_national': False,
                        'image_url': 'https://travelfoodatlas.com/wp-content/uploads/2023/05/Bouyon.jpg.webp'
                    }
                }
            },
            'grenada': {
                'name': 'Grenada',
                'flag': '🇬🇩',
                'region': 'Lesser Antilles',
                'cultural_intro': "Grenadian cuisine is known as the 'Spice Isle' cuisine, featuring nutmeg and other aromatic spices.",
                'dishes': {
                    'oil_down': {
                        'name': 'Oil Down',
                        'description': "National dish cooked in coconut milk until liquid is absorbed.",
                        'ingredients': ['Breadfruit', 'Salted meat', 'Coconut milk', 'Callaloo', 'Dumplings'],
                        'cooking_instructions': ['Layer ingredients in pot', 'Add coconut milk', 'Cook until oil separates', 'Stir gently'],
                        'cultural_note': "Represents unity as all ingredients cook together harmoniously.",
                        'meal_type': 'Main Course', 'difficulty': 'Moderate', 'is_national': True,
                        'image_url': 'https://i.pinimg.com/originals/d1/29/98/d129987ae4212b1fde5bab78ce39b772.jpg'
                    },
                    'nutmeg_ice_cream': {
                        'name': 'Nutmeg Ice Cream',
                        'description': "Creamy ice cream infused with fresh local nutmeg.",
                        'ingredients': ['Heavy cream', 'Sugar', 'Fresh nutmeg', 'Vanilla', 'Egg yolks'],
                        'cooking_instructions': ['Heat cream with nutmeg', 'Whisk egg mixture', 'Combine and cook', 'Churn in ice cream maker'],
                        'cultural_note': "Showcases Grenada's famous nutmeg production.",
                        'meal_type': 'Dessert', 'difficulty': 'Moderate', 'is_national': False,
                        'image_url': 'https://cdn.tasteatlas.com/images/dishes/31903663bba54584abb71798f0e26ad5.jpg'
                    }
                }
            },
            'antigua_barbuda': {
                'name': 'Antigua and Barbuda',
                'flag': '🇦🇬',
                'region': 'Lesser Antilles',
                'cultural_intro': "Antiguan cuisine emphasizes fresh seafood and local provisions with British and African influences.",
                'dishes': {
                    'fungee_pepperpot': {
                        'name': 'Fungee and Pepperpot',
                        'description': "National dish of cornmeal dumpling with spicy meat stew.",
                        'ingredients': ['Cornmeal', 'Okra', 'Mixed meats', 'Spinach', 'Hot peppers'],
                        'cooking_instructions': ['Cook cornmeal with okra', 'Prepare meat stew', 'Season with peppers', 'Serve together'],
                        'cultural_note': "Fungee technique brought from Africa, adapted with local ingredients.",
                        'meal_type': 'Main Course', 'difficulty': 'Moderate', 'is_national': True,
                        'image_url': 'https://exceptionalcaribbean.com/wp-content/uploads/2021/02/Screenshot-77.png'
                    },
                    'ducana': {
                        'name': 'Ducana',
                        'description': "Sweet potato dumpling wrapped in banana leaf.",
                        'ingredients': ['Sweet potato', 'Flour', 'Sugar', 'Spices', 'Banana leaves'],
                        'cooking_instructions': ['Grate sweet potato', 'Mix with dry ingredients', 'Wrap in leaves', 'Boil until cooked'],
                        'cultural_note': "Traditional preparation method preserving African cooking techniques.",
                        'meal_type': 'Side Dish', 'difficulty': 'Moderate', 'is_national': False,
                        'image_url': 'https://eatyourworld.com/images/content_images/images/ducana-antigua-recipe-post.jpg'
                    }
                }
            },
            'st_kitts_nevis': {
                'name': 'Saint Kitts and Nevis',
                'flag': '🇰🇳',
                'region': 'Lesser Antilles',
                'cultural_intro': "Kittitian cuisine combines British colonial heritage with African traditions and local seafood.",
                'dishes': {
                    'stewed_saltfish': {
                        'name': 'Stewed Saltfish',
                        'description': "National dish of salted cod cooked with local vegetables and spices.",
                        'ingredients': ['Salt cod', 'Tomatoes', 'Onions', 'Sweet peppers', 'Thyme'],
                        'cooking_instructions': ['Soak and boil saltfish', 'Sauté vegetables', 'Add fish and simmer', 'Season to taste'],
                        'cultural_note': "Reflects the island's historical dependence on preserved fish.",
                        'meal_type': 'Main Course', 'difficulty': 'Easy', 'is_national': True,
                        'image_url': 'https://c1.staticflickr.com/6/5088/5380185701_ddc29b0637.jpg'
                    },
                    'goat_water': {
                        'name': 'Goat Water',
                        'description': "Hearty stew that's actually a soup, despite the name.",
                        'ingredients': ['Goat meat', 'Breadfruit', 'Onions', 'Thyme', 'Hot peppers'],
                        'cooking_instructions': ['Brown goat meat', 'Add vegetables', 'Simmer until tender', 'Season with herbs'],
                        'cultural_note': "Traditional comfort food for special occasions and gatherings.",
                        'meal_type': 'Main Course', 'difficulty': 'Moderate', 'is_national': False,
                        'image_url': 'https://explorers.kitchen/wp-content/uploads/2016/03/St.-Kitts-and-Nevis-Goat-Water-Stew-8.jpg'
                    }
                }
            },
            'dominica': {
                'name': 'Dominica',
                'flag': '🇩🇲',
                'region': 'Lesser Antilles',
                'cultural_intro': "Dominican cuisine features strong Kalinago influences with abundant use of local provisions and river fish.",
                'dishes': {
                    'mountain_chicken': {
                        'name': 'Mountain Chicken',
                        'description': "Traditional dish made from large local frogs (crapaud).",
                        'ingredients': ['Crapaud legs', 'Lime juice', 'Garlic', 'Thyme', 'Hot peppers'],
                        'cooking_instructions': ['Clean and season frog legs', 'Marinate in lime', 'Sauté with aromatics', 'Serve hot'],
                        'cultural_note': "Once abundant, now protected species. Historical delicacy of the island.",
                        'meal_type': 'Main Course', 'difficulty': 'Moderate', 'is_national': True,
                        'image_url': 'https://jadarecipes.com/wp-content/uploads/2024/12/hfpfY1r8QPqtlYUSX4Sffw_11zon.webp'
                    },
                    'callaloo': {
                        'name': 'Callaloo Soup',
                        'description': "Creamy soup made from callaloo leaves and coconut milk.",
                        'ingredients': ['Callaloo leaves', 'Coconut milk', 'Crab', 'Okra', 'Onions'],
                        'cooking_instructions': ['Sauté aromatics', 'Add callaloo and coconut milk', 'Include seafood', 'Simmer until creamy'],
                        'cultural_note': "Showcases indigenous Kalinago cooking methods and local ingredients.",
                        'meal_type': 'Main Course', 'difficulty': 'Easy', 'is_national': False,
                        'image_url': 'https://i.pinimg.com/originals/9d/31/0f/9d310f794e8afe09c7684875d8b48327.jpg'
                    }
                }
            },
            'st_vincent_grenadines': {
                'name': 'Saint Vincent and the Grenadines',
                'flag': '🇻🇨',
                'region': 'Lesser Antilles',
                'cultural_intro': "Vincentian cuisine emphasizes fresh seafood, tropical fruits, and ground provisions.",
                'dishes': {
                    'roasted_breadfruit_jackfish': {
                        'name': 'Roasted Breadfruit and Jackfish',
                        'description': "Traditional combination of roasted breadfruit with seasoned fish.",
                        'ingredients': ['Breadfruit', 'Jackfish', 'Garlic', 'Thyme', 'Lime'],
                        'cooking_instructions': ['Roast breadfruit over fire', 'Season and grill fish', 'Serve together hot'],
                        'cultural_note': "Captain Bligh brought breadfruit to feed enslaved people; now a staple.",
                        'meal_type': 'Main Course', 'difficulty': 'Moderate', 'is_national': True,
                        'image_url': 'https://ourbigescape.com/wp-content/uploads/2023/03/7.-Roasted-Breadfruit-Jackfish-Saint-Vincent-Recipes.jpg'
                    },
                    'arrowroot_cookies': {
                        'name': 'Arrowroot Cookies',
                        'description': "Light, crispy cookies made from locally grown arrowroot starch.",
                        'ingredients': ['Arrowroot starch', 'Butter', 'Sugar', 'Vanilla', 'Nutmeg'],
                        'cooking_instructions': ['Cream butter and sugar', 'Add arrowroot starch', 'Form cookies', 'Bake until golden'],
                        'cultural_note': "Saint Vincent is famous for arrowroot production, exported worldwide.",
                        'meal_type': 'Dessert', 'difficulty': 'Easy', 'is_national': False,
                        'image_url': 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEirCmf4eVutwnOgsB0G6l1FkPt0YeWbmuGBq95IpQ33HwIPRfYrE20dwTYOZqX2HtiQWgWUDs4KNYjgIsLva1hTzEH-1Ffgu23HGDn15mRgze1xruhson2dg5O77INpeRO7041G5T4OBFj9/s1600/12.jpeg'
                    }
                }
            }
        }

    def display_header(self):
        """Display the main header with Caribbean theme"""
        st.markdown("""
        <div class="main-header">
            <h1>🌴 Complete Caribbean Culinary Heritage 🌴</h1>
            <p>Explore the rich flavors and cultural stories of Caribbean cuisine from across the islands</p>
        </div>
        """, unsafe_allow_html=True)

    def display_country_selector(self):
        """Create country selection interface"""
        st.sidebar.title("🏝️ Select Caribbean Country")
        
        country_options = {
            country_data['name']: key 
            for key, country_data in self.cuisine_data.items()
        }
        
        selected_country_name = st.sidebar.selectbox(
            "Choose a country to explore:",
            options=list(country_options.keys()),
            index=0
        )
        
        return country_options[selected_country_name]

    def display_filters(self):
        """Create filtering options"""
        st.sidebar.title("🍽️ Filter Dishes")
        
        # Meal type filter
        meal_types = set()
        difficulties = set()
        
        for country_data in self.cuisine_data.values():
            for dish in country_data['dishes'].values():
                meal_types.add(dish['meal_type'])
                difficulties.add(dish['difficulty'])
        
        selected_meal_types = st.sidebar.multiselect(
            "Meal Types:",
            options=sorted(meal_types),
            default=sorted(meal_types)
        )
        
        selected_difficulties = st.sidebar.multiselect(
            "Difficulty Levels:",
            options=sorted(difficulties),
            default=sorted(difficulties)
        )
        
        show_national_only = st.sidebar.checkbox("Show National Dishes Only", False)
        
        return selected_meal_types, selected_difficulties, show_national_only

    def display_country_info(self, country_key):
        """Display country information and cultural context"""
        country = self.cuisine_data[country_key]
        
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown(f"## {country['flag']}")
        with col2:
            st.markdown(f"## {country['name']}")
            st.markdown(f"**Region:** {country['region']}")
        
        st.markdown(f"### Cultural Heritage")
        st.markdown(country['cultural_intro'])

    def display_dish_card(self, dish_data, dish_key):
        """Display individual dish card with styling"""
        st.markdown(f"""
        <div class="dish-card">
            <img src="{dish_data['image_url']}" class="dish-image" alt="{dish_data['name']}">
            <h3>{dish_data['name']}</h3>
            {f'<div class="national-dish">🏆 National Dish</div>' if dish_data['is_national'] else ''}
            <p><strong>Meal Type:</strong> {dish_data['meal_type']} | <strong>Difficulty:</strong> {dish_data['difficulty']}</p>
            <p>{dish_data['description']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Expandable sections
        with st.expander(f"🥘 Ingredients for {dish_data['name']}"):
            for ingredient in dish_data['ingredients']:
                st.markdown(f'<span class="ingredient-tag">{ingredient}</span>', unsafe_allow_html=True)
        
        with st.expander(f"👨‍🍳 Cooking Instructions"):
            for i, step in enumerate(dish_data['cooking_instructions'], 1):
                st.markdown(f"""
                <div class="cooking-step">
                    <strong>Step {i}:</strong> {step}
                </div>
                """, unsafe_allow_html=True)
        
        with st.expander(f"🏛️ Cultural Significance"):
            st.markdown(f"""
            <div class="cultural-note">
                <strong>Cultural Note:</strong> {dish_data['cultural_note']}
            </div>
            """, unsafe_allow_html=True)

    def filter_dishes(self, country_key, meal_types, difficulties, national_only):
        """Filter dishes based on selected criteria"""
        dishes = self.cuisine_data[country_key]['dishes']
        filtered_dishes = {}
        
        for dish_key, dish_data in dishes.items():
            # Apply filters
            if dish_data['meal_type'] not in meal_types:
                continue
            if dish_data['difficulty'] not in difficulties:
                continue
            if national_only and not dish_data['is_national']:
                continue
            
            filtered_dishes[dish_key] = dish_data
        
        return filtered_dishes

    def display_statistics(self, country_key, filtered_dishes):
        """Display statistics about the cuisine"""
        total_dishes = len(self.cuisine_data[country_key]['dishes'])
        filtered_count = len(filtered_dishes)
        national_dishes = sum(1 for dish in self.cuisine_data[country_key]['dishes'].values() if dish['is_national'])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Dishes", total_dishes)
        with col2:
            st.metric("Showing", filtered_count)
        with col3:
            st.metric("National Dishes", national_dishes)

    def run(self):
        """Main application runner"""
        self.display_header()
        
        # Sidebar controls
        selected_country = self.display_country_selector()
        meal_types, difficulties, national_only = self.display_filters()
        
        # Main content
        self.display_country_info(selected_country)
        
        # Filter and display dishes
        filtered_dishes = self.filter_dishes(selected_country, meal_types, difficulties, national_only)
        
        if filtered_dishes:
            self.display_statistics(selected_country, filtered_dishes)
            st.markdown("---")
            
            # Display filtered dishes
            for dish_key, dish_data in filtered_dishes.items():
                self.display_dish_card(dish_data, dish_key)
                st.markdown("---")
        else:
            st.warning("No dishes match your current filter criteria. Please adjust your selections.")

        # Footer
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #666; padding: 2rem;">
            <p>🌴 Celebrating the rich culinary heritage of the Caribbean islands 🌴</p>
            <p>Each dish tells a story of culture, history, and tradition</p>
        </div>
        """, unsafe_allow_html=True)

# Run the application
if __name__ == "__main__":
    app = CompleteCaribbeanCuisineApp()
    app.run()