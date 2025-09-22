import streamlit as st
import random
from typing import Dict, List, Any

# Country flag mapping - moved to global scope
country_flag = {
    'Jamaica': '🇯🇲', 
    'Trinidad and Tobago': '🇹🇹', 
    'Barbados': '🇧🇧',
    'Cuba': '🇨🇺', 
    'Puerto Rico': '🇵🇷', 
    'Dominican Republic': '🇩🇴',
    'Haiti': '🇭🇹', 
    'Guadeloupe': '🇬🇵', 
    'Martinique': '🇲🇶',
    'Saint Lucia': '🇱🇨', 
    'Curaçao': '🇨🇼', 
    'Aruba': '🇦🇼',
    'Antigua and Barbuda': '🇦🇬', 
    'Saint Vincent and the Grenadines': '🇻🇨',
    'Grenada': '🇬🇩', 
    'Montserrat': '🇲🇸', 
    'Belize': '🇧🇿',
    'Bahamas': '🇧🇸', 
    'Bermuda': '🇧🇲', 
    'Puerto Rico/USA': '🇵🇷🇺🇸',
    'Guadeloupe/Martinique': '🇬🇵🇲🇶', 
    'Aruba/Curaçao': '🇦🇼🇨🇼'
}

# Comprehensive Caribbean music and instruments database
CARIBBEAN_MUSIC_AND_INSTRUMENTS = {
    # JAMAICA
    "reggae": {
        "image": "https://www.worldmusic.net/assets/images/news/reggae-month-feb-2017.jpg",
        "description": "A music genre that originated in Jamaica in the late 1960s, characterized by a distinctive rhythm and often associated with Rastafarian culture.",
        "origin": "Developed in Jamaica from ska and rocksteady, with influences from American jazz and rhythm and blues.",
        "cultural_significance": "Symbol of Jamaican identity and resistance, spreading Rastafarian philosophy worldwide.",
        "category": "popular_music",
        "era": "Modern (1960s-Present)",
        "country": "Jamaica",
        "instruments_used": ["guitar", "bass", "drums", "organ", "percussion"],
        "occasions": ["concerts", "festivals", "spiritual gatherings", "international events"],
        "key_artists": ["Bob Marley", "Jimmy Cliff", "Dennis Brown", "Burning Spear"]
    },
    "dancehall": {
        "image": "https://www.dancehallmag.com/wp-content/uploads/2020/08/dancehall-culture.jpg",
        "description": "A genre of Jamaican popular music that originated in the late 1970s, known for its digital rhythms and DJ-style vocals.",
        "origin": "Evolved from reggae in Jamaica, incorporating digital production and sound system culture.",
        "cultural_significance": "Represents modern Jamaican urban culture and has influenced global hip-hop.",
        "category": "popular_music",
        "era": "Contemporary (1970s-Present)",
        "country": "Jamaica",
        "instruments_used": ["digital drums", "synthesizers", "bass", "microphone"],
        "occasions": ["dance parties", "sound system sessions", "clubs", "festivals"]
    },
    "mento": {
        "image": "https://www.jamaicans.com/wp-content/uploads/2016/07/mento-band.jpg",
        "description": "A style of Jamaican folk music that predates and has influenced ska and reggae.",
        "origin": "Traditional Jamaican folk music with African and European influences.",
        "cultural_significance": "Preserved Jamaican rural traditions and storytelling through music.",
        "category": "folk_music",
        "era": "Traditional",
        "country": "Jamaica",
        "instruments_used": ["banjo", "guitar", "rumba box", "maracas"],
        "occasions": ["folk festivals", "cultural events", "storytelling"]
    },

    # TRINIDAD AND TOBAGO
    "calypso": {
        "image": "https://www.nalis.gov.tt/wp-content/uploads/2018/01/Calypso-Tent.jpg",
        "description": "A style of Afro-Caribbean music that originated in Trinidad and Tobago, known for its witty, satirical lyrics.",
        "origin": "Developed by enslaved Africans in Trinidad, blending African musical traditions with French and Spanish influences.",
        "cultural_significance": "Vehicle for social commentary and political satire in Caribbean society.",
        "category": "folk_music",
        "era": "Traditional to Modern",
        "country": "Trinidad and Tobago",
        "instruments_used": ["guitar", "cuatro", "maracas", "conga drums"],
        "occasions": ["carnival", "calypso competitions", "social gatherings"]
    },
    "soca": {
        "image": "https://www.triniview.com/wp-content/uploads/2019/02/soca-music.jpg",
        "description": "A genre of music that originated in Trinidad and Tobago, blending calypso with Indian musical instruments and rhythms.",
        "origin": "Created in the 1970s by Lord Shorty, combining calypso with East Indian musical elements.",
        "cultural_significance": "Represents Trinidad's multicultural heritage and carnival spirit.",
        "category": "popular_music",
        "era": "Modern (1970s-Present)",
        "country": "Trinidad and Tobago",
        "instruments_used": ["synthesizers", "drums", "guitar", "dholak", "tassa"],
        "occasions": ["carnival", "fetes", "festivals", "celebrations"]
    },
    "steelpan": {
        "image": "https://www.steelpan.org/images/panorama-2019.jpg",
        "description": "A musical instrument originating from Trinidad and Tobago, made from 55-gallon industrial drums.",
        "origin": "Invented in Trinidad in the 1930s, evolved from traditional percussion instruments.",
        "cultural_significance": "National instrument of Trinidad and Tobago, symbol of creativity and resilience.",
        "category": "percussion_instrument",
        "era": "Modern Innovation",
        "country": "Trinidad and Tobago",
        "used_in": ["steelband music", "calypso", "soca", "classical music"],
        "material": "Steel drums, mallets"
    },
    "chutney": {
        "image": "https://www.guardian.co.tt/sites/default/files/story/2018/05/chutney-music.jpg",
        "description": "A form of music indigenous to Trinidad and Tobago, blending Indian folk music with calypso and soca.",
        "origin": "Developed by Indo-Caribbean community, combining Indian classical and folk music with local Caribbean rhythms.",
        "cultural_significance": "Celebrates Indo-Caribbean heritage and cultural fusion.",
        "category": "fusion_music",
        "era": "Modern (1960s-Present)",
        "country": "Trinidad and Tobago",
        "instruments_used": ["dholak", "harmonium", "guitar", "synthesizer"],
        "occasions": ["weddings", "festivals", "cultural celebrations"]
    },

    # BARBADOS
    "spouge": {
        "image": "https://www.barbadospocketguide.com/wp-content/uploads/2016/07/spouge-music.jpg",
        "description": "A style of music created in Barbados that combines calypso with rhythm and blues.",
        "origin": "Created in the 1960s by Jackie Opel, blending American R&B with Caribbean calypso.",
        "cultural_significance": "Unique Barbadian contribution to Caribbean music, influencing later genres.",
        "category": "popular_music",
        "era": "Modern (1960s-1970s)",
        "country": "Barbados",
        "instruments_used": ["guitar", "bass", "drums", "organ"],
        "occasions": ["festivals", "concerts", "cultural events"]
    },
    "tuk": {
        "image": "https://www.barbados.org/images/tuk-band-barbados.jpg",
        "description": "Traditional Barbadian folk music played by tuk bands, featuring British military band instruments with African rhythms.",
        "origin": "Developed during colonial times, combining British military music with African percussion.",
        "cultural_significance": "Preserves Barbadian folk traditions and community celebrations.",
        "category": "folk_music",
        "era": "Colonial to Present",
        "country": "Barbados",
        "instruments_used": ["snare drum", "bass drum", "penny whistle", "triangle"],
        "occasions": ["crop over festival", "parades", "community events"]
    },

    # CUBA
    "son cubano": {
        "image": "https://www.cubatravel.cu/sites/default/files/son-cubano-music.jpg",
        "description": "A genre of music and dance that originated in eastern Cuba, combining Spanish canción and guitar with African rhythms and percussion.",
        "origin": "Emerged in eastern Cuba in the late 19th century, blending Spanish and African musical traditions.",
        "cultural_significance": "Foundation of modern salsa music and symbol of Cuban musical innovation.",
        "category": "traditional_music",
        "era": "Traditional to Modern",
        "country": "Cuba",
        "instruments_used": ["guitar", "tres", "bongos", "maracas", "bass"],
        "occasions": ["social dancing", "festivals", "cultural events"]
    },
    "rumba": {
        "image": "https://www.cubaabsolutely.com/wp-content/uploads/rumba-dancers-cuba.jpg",
        "description": "A secular genre of Cuban music involving dance, percussion, and song, with strong African roots.",
        "origin": "Developed in Cuba during the 19th century by enslaved and free Africans and their descendants.",
        "cultural_significance": "UNESCO Intangible Cultural Heritage, represents Afro-Cuban identity.",
        "category": "traditional_music",
        "era": "Traditional",
        "country": "Cuba",
        "instruments_used": ["conga drums", "claves", "cajón", "guiro"],
        "occasions": ["community celebrations", "cultural festivals", "spiritual ceremonies"]
    },
    "mambo": {
        "image": "https://www.dancecentral.info/ballroom/mambo/mambo-dance.jpg",
        "description": "A genre of Cuban dance music based on the Cuban contradanza, developed by Pérez Prado in the 1940s.",
        "origin": "Created in Cuba in the 1940s, later popularized in Mexico and the United States.",
        "cultural_significance": "Influenced international Latin dance culture and big band music.",
        "category": "dance_music",
        "era": "Modern (1940s-1960s)",
        "country": "Cuba",
        "instruments_used": ["trumpets", "piano", "bass", "drums", "percussion"],
        "occasions": ["ballroom dancing", "nightclubs", "concerts"]
    },

    # PUERTO RICO
    "salsa": {
        "image": "https://www.salsadancing.co.uk/wp-content/uploads/salsa-musicians.jpg",
        "description": "A popular dance music genre that developed in Puerto Rico and New York, with roots in son cubano and other Latin American music.",
        "origin": "Developed in 1960s New York by Puerto Rican and Cuban musicians, based on earlier Cuban son.",
        "cultural_significance": "Global symbol of Latin culture and community identity.",
        "category": "popular_music",
        "era": "Modern (1960s-Present)",
        "country": "Puerto Rico/USA",
        "instruments_used": ["piano", "trumpets", "trombone", "bass", "timbales", "congas"],
        "occasions": ["social dancing", "festivals", "clubs", "cultural events"]
    },
    "bomba": {
        "image": "https://www.puertoricodaytrips.com/wp-content/uploads/bomba-puerto-rico.jpg",
        "description": "A traditional musical style of Puerto Rico with strong African influences, featuring call-and-response singing and drums.",
        "origin": "Developed by enslaved Africans in Puerto Rico, preserving West African musical traditions.",
        "cultural_significance": "Symbol of Puerto Rican Afro-descendant identity and resistance.",
        "category": "traditional_music",
        "era": "Colonial to Present",
        "country": "Puerto Rico",
        "instruments_used": ["barril drums", "cuá sticks", "maracas"],
        "occasions": ["cultural festivals", "community gatherings", "spiritual ceremonies"]
    },
    "plena": {
        "image": "https://www.discoverpuertorico.com/sites/default/files/plena-music-puerto-rico.jpg",
        "description": "A genre of music and dance native to Puerto Rico, often called 'the singing newspaper' for its narrative lyrics.",
        "origin": "Originated in Ponce, Puerto Rico in the early 20th century, influenced by Caribbean and Spanish music.",
        "cultural_significance": "Serves as oral history and social commentary in Puerto Rican culture.",
        "category": "folk_music",
        "era": "Modern (1900s-Present)",
        "country": "Puerto Rico",
        "instruments_used": ["pandereta", "güiro", "accordion", "guitar"],
        "occasions": ["festivals", "social gatherings", "cultural events"]
    },

    # DOMINICAN REPUBLIC
    "merengue": {
        "image": "https://www.godominicanrepublic.com/wp-content/uploads/merengue-dance.jpg",
        "description": "A type of music and dance originating in the Dominican Republic, characterized by fast-paced rhythm.",
        "origin": "Originated in the Dominican Republic in the mid-19th century, with African and European influences.",
        "cultural_significance": "National dance and music of Dominican Republic, UNESCO Intangible Cultural Heritage.",
        "category": "popular_music",
        "era": "Traditional to Modern",
        "country": "Dominican Republic",
        "instruments_used": ["accordion", "tambora", "güira", "bass"],
        "occasions": ["social dancing", "festivals", "celebrations", "clubs"]
    },
    "bachata": {
        "image": "https://www.dancelifemap.com/wp-content/uploads/bachata-guitar.jpg",
        "description": "A genre of music that originated in the Dominican Republic, characterized by romantic ballads with guitar accompaniment.",
        "origin": "Originated in rural Dominican Republic in the 1960s, initially marginalized but later embraced.",
        "cultural_significance": "Represents Dominican romantic expression and has gained international popularity.",
        "category": "popular_music",
        "era": "Modern (1960s-Present)",
        "country": "Dominican Republic",
        "instruments_used": ["guitar", "bass", "bongos", "güira"],
        "occasions": ["romantic occasions", "social dancing", "clubs", "concerts"]
    },

    # HAITI
    "compas": {
        "image": "https://www.haitilibre.com/images/compas-haiti-music.jpg",
        "description": "A modern méringue-style dance music genre of Haiti, also known as compas direct or konpa dirèk.",
        "origin": "Created in Haiti in the 1950s by Nemours Jean-Baptiste, modernizing traditional méringue.",
        "cultural_significance": "Most popular music genre in Haiti, part of national cultural identity.",
        "category": "popular_music",
        "era": "Modern (1950s-Present)",
        "country": "Haiti",
        "instruments_used": ["guitar", "bass", "drums", "horn section", "keyboard"],
        "occasions": ["dancing", "festivals", "celebrations", "social events"]
    },
    "rara": {
        "image": "https://www.ayitinet.org/wp-content/uploads/rara-haiti-festival.jpg",
        "description": "A form of festival music used for street processions, typically during Easter Week in Haiti.",
        "origin": "Traditional Haitian music with roots in African spiritual practices and Vodou religion.",
        "cultural_significance": "Important spiritual and community bonding practice in Haitian culture.",
        "category": "ceremonial_music",
        "era": "Traditional",
        "country": "Haiti",
        "instruments_used": ["vaksin horns", "drums", "maracas", "metal percussion"],
        "occasions": ["Easter processions", "spiritual ceremonies", "community festivals"]
    },

    # GUADELOUPE & MARTINIQUE
    "zouk": {
        "image": "https://www.antillesexception.com/wp-content/uploads/zouk-antilles.jpg",
        "description": "A style of rhythmic music originating from the French Caribbean islands of Guadeloupe and Martinique.",
        "origin": "Developed in the 1980s in the French Antilles, blending traditional Caribbean music with modern production.",
        "cultural_significance": "Represents French Caribbean identity and has influenced world music.",
        "category": "popular_music",
        "era": "Modern (1980s-Present)",
        "country": "Guadeloupe/Martinique",
        "instruments_used": ["synthesizers", "guitar", "bass", "drums", "percussion"],
        "occasions": ["dancing", "festivals", "clubs", "cultural events"]
    },
    "gwo ka": {
        "image": "https://www.guadeloupe-islands.com/wp-content/uploads/gwo-ka-drums.jpg",
        "description": "Traditional music from Guadeloupe featuring seven distinct rhythms played on drums called ka.",
        "origin": "Developed by enslaved Africans in Guadeloupe, preserving West African musical traditions.",
        "cultural_significance": "UNESCO Intangible Cultural Heritage, symbol of Guadeloupean identity.",
        "category": "traditional_music",
        "era": "Colonial to Present",
        "country": "Guadeloupe",
        "instruments_used": ["ka drums", "chacha", "tibwa"],
        "occasions": ["cultural festivals", "spiritual ceremonies", "community gatherings"]
    },

    # SAINT LUCIA
    "kwadril": {
        "image": "https://www.uncommoncaribbean.com/wp-content/uploads/2016/04/Quadrille.jpg",
        "description": "A traditional Creole folk dance and music style, influenced by European quadrille dances and African rhythms.",
        "origin": "Brought to Saint Lucia during colonial times and adapted into a unique Creole style.",
        "cultural_significance": "Performed during cultural festivals and community gatherings.",
        "category": "folk_music",
        "era": "Colonial Period",
        "country": "Saint Lucia",
        "instruments_used": ["fiddle", "guitar", "banjo"],
        "occasions": ["festivals", "weddings", "community gatherings"]
    },
    "dennery segment": {
        "image": "https://stluciatimes.com/wp-content/uploads/2025/03/DSC06720-1920x1081.jpg",
        "description": "A high-energy electronic soca genre that emerged from Saint Lucia, characterized by rapid beats and Kreyòl lyrics.",
        "origin": "Developed in Saint Lucia in the early 2010s, initially called 'Lucian Kuduro', influenced by Angolan Kuduro.",
        "cultural_significance": "Represents modern Saint Lucian musical innovation and global recognition.",
        "category": "modern_soca",
        "era": "Contemporary (2010s-Present)",
        "country": "Saint Lucia",
        "instruments_used": ["electronic beats", "synthesizers", "drums"],
        "occasions": ["carnival", "street parties", "dance clubs", "festivals"]
    },

    # ARUBA, BONAIRE, CURAÇAO
    "tambú": {
        "image": "https://www.curacao.com/wp-content/uploads/tambu-curacao.jpg",
        "description": "Traditional music and dance from Curaçao, featuring call-and-response singing and African-derived rhythms.",
        "origin": "Brought to Curaçao by enslaved Africans, maintaining West African musical traditions.",
        "cultural_significance": "Important part of Afro-Caribbean heritage in the Dutch Antilles.",
        "category": "traditional_music",
        "era": "Colonial to Present",
        "country": "Curaçao",
        "instruments_used": ["tambú drum", "chapi", "triangle"],
        "occasions": ["cultural festivals", "community celebrations", "spiritual ceremonies"]
    },
    "tumba": {
        "image": "https://www.aruba.com/wp-content/uploads/tumba-carnival-aruba.jpg",
        "description": "A music genre from the Dutch Caribbean islands, especially popular during Carnival season.",
        "origin": "Developed in the Dutch Antilles, combining local rhythms with calypso influences.",
        "cultural_significance": "Central to Carnival celebrations in Aruba and Curaçao.",
        "category": "carnival_music",
        "era": "Modern",
        "country": "Aruba/Curaçao",
        "instruments_used": ["guitar", "bass", "drums", "brass instruments"],
        "occasions": ["carnival", "festivals", "competitions"]
    },

    # ANTIGUA AND BARBUDA
    "steeldrum calypso": {
        "image": "https://www.antigua-barbuda.org/wp-content/uploads/steel-drum-band.jpg",
        "description": "Traditional calypso music played on steel drums, popular in Antigua and Barbuda.",
        "origin": "Adapted from Trinidadian steelpan culture, localized to Antiguan musical traditions.",
        "cultural_significance": "Part of the island's cultural identity and tourist attractions.",
        "category": "folk_music",
        "era": "Modern",
        "country": "Antigua and Barbuda",
        "instruments_used": ["steel drums", "guitar", "bass"],
        "occasions": ["festivals", "cultural events", "tourism entertainment"]
    },

    # SAINT VINCENT AND THE GRENADINES
    "string band": {
        "image": "https://www.discoversvg.com/wp-content/uploads/string-band-svg.jpg",
        "description": "Traditional music featuring string instruments, popular for folk songs and storytelling.",
        "origin": "Developed from European string music traditions adapted to Caribbean cultural context.",
        "cultural_significance": "Preserves local folk traditions and community storytelling.",
        "category": "folk_music",
        "era": "Traditional",
        "country": "Saint Vincent and the Grenadines",
        "instruments_used": ["guitar", "violin", "banjo", "bass"],
        "occasions": ["folk festivals", "storytelling events", "cultural gatherings"]
    },

    # GRENADA
    "big drum": {
        "image": "https://www.grenada.org/wp-content/uploads/big-drum-nation-dance.jpg",
        "description": "Traditional music and dance from Grenada featuring African-derived drumming and ceremonial dances.",
        "origin": "Brought by enslaved Africans to Grenada, maintaining traditional ceremonial practices.",
        "cultural_significance": "Important spiritual and cultural practice connecting to African heritage.",
        "category": "ceremonial_music",
        "era": "Traditional",
        "country": "Grenada",
        "instruments_used": ["big drums", "cut drums", "triangle", "shac-shac"],
        "occasions": ["nation dances", "cultural ceremonies", "festivals"]
    },

    # MONTSERRAT
    "string band music": {
        "image": "https://www.visitmontserrat.com/wp-content/uploads/string-band-montserrat.jpg",
        "description": "Traditional folk music featuring acoustic string instruments, popular for social gatherings.",
        "origin": "Developed from European folk music traditions adapted to Montserratian culture.",
        "cultural_significance": "Maintains local cultural identity and community traditions.",
        "category": "folk_music",
        "era": "Traditional",
        "country": "Montserrat",
        "instruments_used": ["guitar", "ukulele", "bass", "triangle"],
        "occasions": ["festivals", "community events", "cultural celebrations"]
    },

    # BELIZE
    "punta": {
        "image": "https://www.belizetourismboard.org/wp-content/uploads/punta-music-belize.jpg",
        "description": "A cultural music and dance form of the Garífuna people, featuring rapid drumming and energetic dancing.",
        "origin": "Brought to Belize by the Garífuna people from Saint Vincent, with African and indigenous roots.",
        "cultural_significance": "Central to Garífuna cultural identity and spiritual practices.",
        "category": "cultural_music",
        "era": "Traditional",
        "country": "Belize",
        "instruments_used": ["primera drum", "segunda drum", "maracas"],
        "occasions": ["cultural festivals", "spiritual ceremonies", "community celebrations"]
    },
    "brukdown": {
        "image": "https://www.belize.com/wp-content/uploads/brukdown-music-belize.jpg",
        "description": "A genre of Belizean music and dance, featuring accordion and guitar with storytelling lyrics.",
        "origin": "Developed by Creole communities in Belize, blending various musical influences.",
        "cultural_significance": "Represents Belizean Creole culture and community storytelling traditions.",
        "category": "folk_music",
        "era": "Traditional to Modern",
        "country": "Belize",
        "instruments_used": ["accordion", "guitar", "banjo", "drums"],
        "occasions": ["festivals", "social gatherings", "cultural events"]
    },

    # BAHAMAS
    "junkanoo": {
        "image": "https://www.bahamas.com/sites/default/files/junkanoo-festival.jpg",
        "description": "A street parade with music, dance, and costumes, held at Christmas and New Year in the Bahamas.",
        "origin": "Traditional festival with African roots, dating back to the days of slavery in the Bahamas.",
        "cultural_significance": "Most important cultural celebration in the Bahamas, expression of freedom and creativity.",
        "category": "festival_music",
        "era": "Traditional to Present",
        "country": "Bahamas",
        "instruments_used": ["goatskin drums", "cowbells", "whistles", "horns"],
        "occasions": ["Boxing Day parade", "New Year celebration", "cultural festivals"]
    },
    "rake and scrape": {
        "image": "https://www.nassauparadiseisland.com/wp-content/uploads/rake-and-scrape.jpg",
        "description": "Traditional Bahamian music featuring the musical saw ('scrape') and accordion, popular for dancing.",
        "origin": "Developed in the Bahamas from European and African musical influences.",
        "cultural_significance": "Unique to Bahamian culture, important for local identity and tourism.",
        "category": "folk_music",
        "era": "Traditional",
        "country": "Bahamas",
        "instruments_used": ["musical saw", "accordion", "guitar", "drums"],
        "occasions": ["local festivals", "fish fries", "community events"]
    },

    # BERMUDA
    "gombey": {
        "image": "https://www.gotobermuda.com/wp-content/uploads/gombey-dancers.jpg",
        "description": "A colorful blend of African, Native American, Caribbean and British influences expressed through dance, drumming and song.",
        "origin": "Developed by enslaved people in Bermuda, combining multiple cultural traditions.",
        "cultural_significance": "Symbol of Bermudian cultural heritage and resistance against oppression.",
        "category": "cultural_dance",
        "era": "Colonial to Present",
        "country": "Bermuda",
        "instruments_used": ["snare drums", "bass drums", "whistles"],
        "occasions": ["Boxing Day", "New Year", "cultural festivals"]
    }
}

class CaribbeanMusicExplorer:
    """Enhanced class to handle Caribbean-wide music and instrument queries"""
    
    def __init__(self, data):
        self.data = data
    
    def search_items(self, query="", category="all", era="all", country="all"):
        """Enhanced search with multiple filters including country"""
        query = query.lower().strip()
        results = []
        
        for name, info in self.data.items():
            # Text search
            text_match = (
                query in name.lower() or
                query in info['description'].lower() or
                query in info['origin'].lower() or
                query in info['cultural_significance'].lower() or
                (query in info.get('country', '').lower())
            )
            
            # Category filter
            category_match = category == "all" or info['category'] == category
            
            # Era filter
            era_match = era == "all" or info['era'] == era
            
            # Country filter
            country_match = country == "all" or info.get('country', '') == country
            
            if (not query or text_match) and category_match and era_match and country_match:
                results.append({
                    'name': name,
                    'data': info,
                    'relevance': self._calculate_relevance(name, info, query)
                })
        
        # Sort by relevance
        results.sort(key=lambda x: x['relevance'], reverse=True)
        return results
    
    def _calculate_relevance(self, name, info, query):
        """Calculate search relevance score"""
        if not query:
            return 1
        
        score = 0
        if query in name.lower():
            score += 10
        if query in info['description'].lower():
            score += 5
        if query in info['origin'].lower():
            score += 3
        if query in info['cultural_significance'].lower():
            score += 2
        if query in info.get('country', '').lower():
            score += 8
        
        return score
    
    def get_categories(self):
        """Get all unique categories"""
        categories = set()
        for info in self.data.values():
            categories.add(info['category'])
        return sorted(list(categories))
    
    def get_eras(self):
        """Get all unique eras"""
        eras = set()
        for info in self.data.values():
            eras.add(info['era'])
        return sorted(list(eras))
    
    def get_countries(self):
        """Get all unique countries"""
        countries = set()
        for info in self.data.values():
            if 'country' in info:
                countries.add(info['country'])
        return sorted(list(countries))
    
    def get_statistics(self):
        """Get comprehensive statistics about the Caribbean collection"""
        stats = {
            'total_items': len(self.data),
            'countries': len(self.get_countries()),
            'categories': len(self.get_categories()),
            'eras': len(self.get_eras()),
            'popular_music': len([item for item in self.data.values() if item['category'] == 'popular_music']),
            'traditional_music': len([item for item in self.data.values() if 'traditional' in item['category'] or 'folk' in item['category']]),
            'instruments': len([item for item in self.data.values() if 'instrument' in item['category']]),
            'modern_genres': len([item for item in self.data.values() if 'Modern' in item.get('era', '') or 'Contemporary' in item.get('era', '')]),
            'african_influenced': len([item for item in self.data.values() if 'African' in item.get('origin', '') or 'enslaved' in item.get('origin', '')]),
            'european_influenced': len([item for item in self.data.values() if 'European' in item.get('origin', '') or 'Spanish' in item.get('origin', '') or 'British' in item.get('origin', '') or 'French' in item.get('origin', '')]),
            'carnival_related': len([item for item in self.data.values() if 'carnival' in ' '.join(item.get('occasions', [])).lower()]),
            'unesco_heritage': len([item for item in self.data.values() if 'UNESCO' in item.get('cultural_significance', '')])
        }
        return stats
    
    def get_random_item(self):
        """Get a random music/instrument item"""
        name = random.choice(list(self.data.keys()))
        return name, self.data[name]
    
    def get_items_by_instruments(self, instrument_query):
        """Find music genres that use specific instruments"""
        results = []
        instrument_query = instrument_query.lower()
        
        for name, info in self.data.items():
            instruments = info.get('instruments_used', [])
            if any(instrument_query in instrument.lower() for instrument in instruments):
                results.append({
                    'name': name,
                    'data': info,
                    'matching_instruments': [inst for inst in instruments if instrument_query in inst.lower()]
                })
        
        return results
    
    def get_cultural_connections(self, country):
        """Get all music from a specific country or cultural region"""
        results = []
        for name, info in self.data.items():
            if info.get('country', '') == country:
                results.append({'name': name, 'data': info})
        return results

# Initialize the explorer
explorer = CaribbeanMusicExplorer(CARIBBEAN_MUSIC_AND_INSTRUMENTS)

def display_music_card(name, data, show_details=False):
    """Display a music/instrument card with enhanced styling"""
    flag = country_flag.get(data.get('country', ''), '🎵')
    
    with st.container():
        st.markdown(f"""
        <div style="
            border: 2px solid #1f77b4;
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        ">
            <h3 style="color: #1f77b4; margin-bottom: 10px;">
                {flag} {name.title()}
            </h3>
            <p style="margin-bottom: 8px;"><strong>Country:</strong> {data.get('country', 'Unknown')}</p>
            <p style="margin-bottom: 8px;"><strong>Category:</strong> {data['category'].replace('_', ' ').title()}</p>
            <p style="margin-bottom: 8px;"><strong>Era:</strong> {data['era']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write(f"**Description:** {data['description']}")
        
        if show_details:
            st.write(f"**Origin:** {data['origin']}")
            st.write(f"**Cultural Significance:** {data['cultural_significance']}")
            
            if 'instruments_used' in data:
                instruments = ', '.join(data['instruments_used'])
                st.write(f"**Instruments Used:** {instruments}")
            
            if 'occasions' in data:
                occasions = ', '.join(data['occasions'])
                st.write(f"**Typical Occasions:** {occasions}")
            
            if 'key_artists' in data:
                artists = ', '.join(data['key_artists'])
                st.write(f"**Key Artists:** {artists}")
        
        # Try to display image if URL is provided
        if 'image' in data and data['image']:
            try:
                st.image(data['image'], caption=f"{name.title()} - {data.get('country', '')}")
            except:
                st.info("🖼️ Image unavailable")

def main():
    """Main Streamlit application"""
    st.set_page_config(
        page_title="🎵 Caribbean Music Explorer",
        page_icon="🎵",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Header
    st.markdown("""
    <div style="text-align: center; padding: 20px; background: linear-gradient(90deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4, #ffeaa7); border-radius: 10px; margin-bottom: 20px;">
        <h1 style="color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); font-size: 3em;">
            🎵 Caribbean Music & Instruments Explorer 🎵
        </h1>
        <p style="color: white; font-size: 1.2em; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">
            Discover the Rich Musical Heritage of the Caribbean Islands
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar Navigation
    st.sidebar.markdown("## 🎯 Navigation")
    page = st.sidebar.radio(
        "Choose a section:",
        ["🏠 Home & Statistics", "🔍 Search & Explore", "🗺️ By Country", "🎼 By Instruments", "🎲 Random Discovery", "📊 Cultural Analysis"]
    )
    
    if page == "🏠 Home & Statistics":
        st.markdown("## 📈 Collection Overview")
        
        # Display statistics
        stats = explorer.get_statistics()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Items", stats['total_items'], help="Total music genres and instruments")
            st.metric("Countries Covered", stats['countries'], help="Caribbean countries and territories")
        
        with col2:
            st.metric("Categories", stats['categories'], help="Different types of music categories")
            st.metric("Time Periods", stats['eras'], help="Different historical eras represented")
        
        with col3:
            st.metric("Popular Music", stats['popular_music'], help="Modern popular music genres")
            st.metric("Traditional Music", stats['traditional_music'], help="Folk and traditional music forms")
        
        with col4:
            st.metric("Carnival Related", stats['carnival_related'], help="Music associated with carnival")
            st.metric("UNESCO Heritage", stats['unesco_heritage'], help="UNESCO recognized cultural heritage")
        
        # Cultural influence breakdown
        st.markdown("### 🌍 Cultural Influences")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("African Influenced", stats['african_influenced'], help="Music with African roots")
        with col2:
            st.metric("European Influenced", stats['european_influenced'], help="Music with European influences")
        
        # Featured items
        st.markdown("### ⭐ Featured Items")
        featured_items = ["reggae", "steelpan", "salsa", "merengue", "zouk"]
        
        for item_name in featured_items:
            if item_name in CARIBBEAN_MUSIC_AND_INSTRUMENTS:
                with st.expander(f"🎵 {item_name.title()} - {CARIBBEAN_MUSIC_AND_INSTRUMENTS[item_name]['country']}"):
                    display_music_card(item_name, CARIBBEAN_MUSIC_AND_INSTRUMENTS[item_name], show_details=True)
    
    elif page == "🔍 Search & Explore":
        st.markdown("## 🔍 Search Caribbean Music")
        
        # Search controls
        col1, col2 = st.columns([2, 1])
        
        with col1:
            search_query = st.text_input("🔎 Search music, instruments, or descriptions:", placeholder="e.g., drum, dance, Jamaica, spiritual...")
        
        with col2:
            show_details = st.checkbox("Show detailed information", value=False)
        
        # Filter controls
        col1, col2, col3 = st.columns(3)
        
        with col1:
            selected_category = st.selectbox("Category", ["all"] + explorer.get_categories())
        
        with col2:
            selected_era = st.selectbox("Era", ["all"] + explorer.get_eras())
        
        with col3:
            selected_country = st.selectbox("Country", ["all"] + explorer.get_countries())
        
        # Perform search
        results = explorer.search_items(
            query=search_query,
            category=selected_category,
            era=selected_era,
            country=selected_country
        )
        
        # Display results
        st.markdown(f"### Found {len(results)} results")
        
        if results:
            for result in results:
                display_music_card(result['name'], result['data'], show_details=show_details)
        else:
            st.info("No results found. Try different search terms or filters.")
    
    elif page == "🗺️ By Country":
        st.markdown("## 🗺️ Explore by Country")
        
        # Country selector
        countries = explorer.get_countries()
        selected_country = st.selectbox("Select a Caribbean country or territory:", countries)
        
        if selected_country:
            flag = country_flag.get(selected_country, '🏝️')
            st.markdown(f"### {flag} Music from {selected_country}")
            
            country_items = explorer.get_cultural_connections(selected_country)
            
            if country_items:
                st.write(f"Found **{len(country_items)}** musical traditions from {selected_country}:")
                
                for item in country_items:
                    display_music_card(item['name'], item['data'], show_details=True)
            else:
                st.info(f"No items found for {selected_country}")
        
        # Country overview
        st.markdown("### 🌎 Countries in Collection")
        
        countries_with_counts = []
        for country in countries:
            count = len(explorer.get_cultural_connections(country))
            if count > 0:
                flag = country_flag.get(country, '🏝️')
                countries_with_counts.append(f"{flag} {country} ({count} items)")
        
        st.write("**Available countries:**")
        for country_info in countries_with_counts:
            st.write(f"• {country_info}")
    
    elif page == "🎼 By Instruments":
        st.markdown("## 🎼 Explore by Instruments")
        
        # Instrument search
        instrument_query = st.text_input("🥁 Search for music by instrument:", placeholder="e.g., drums, guitar, piano, steel...")
        
        if instrument_query:
            results = explorer.get_items_by_instruments(instrument_query)
            
            if results:
                st.markdown(f"### Found {len(results)} genres using '{instrument_query}':")
                
                for result in results:
                    st.markdown(f"**{result['name'].title()}** ({result['data']['country']})")
                    st.write(f"Matching instruments: {', '.join(result['matching_instruments'])}")
                    st.write(f"Description: {result['data']['description'][:200]}...")
                    st.write("---")
            else:
                st.info(f"No music found using '{instrument_query}'. Try 'drums', 'guitar', or 'steel'.")
        
        # Common instruments overview
        st.markdown("### 🎯 Common Instruments in Caribbean Music")
        
        # Extract all instruments
        all_instruments = []
        for data in CARIBBEAN_MUSIC_AND_INSTRUMENTS.values():
            all_instruments.extend(data.get('instruments_used', []))
        
        # Count instrument frequency
        from collections import Counter
        instrument_counts = Counter(all_instruments)
        
        st.write("**Most common instruments:**")
        for instrument, count in instrument_counts.most_common(10):
            st.write(f"• **{instrument}** - used in {count} genres")
    
    elif page == "🎲 Random Discovery":
        st.markdown("## 🎲 Random Discovery")
        
        st.write("Discover something new about Caribbean music!")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            if st.button("🎲 Get Random Item", type="primary"):
                st.session_state.random_item = explorer.get_random_item()
        
        with col2:
            if st.button("🔄 Another Random Item"):
                st.session_state.random_item = explorer.get_random_item()
        
        # Display random item
        if hasattr(st.session_state, 'random_item'):
            name, data = st.session_state.random_item
            st.markdown("### 🎵 Your Random Discovery:")
            display_music_card(name, data, show_details=True)
        else:
            st.info("Click the button above to discover a random Caribbean music genre or instrument!")
    
    elif page == "📊 Cultural Analysis":
        st.markdown("## 📊 Cultural Analysis")
        
        # Cultural influence analysis
        st.markdown("### 🌍 Cultural Influences")
        
        african_items = [item for item in CARIBBEAN_MUSIC_AND_INSTRUMENTS.values() 
                        if 'African' in item.get('origin', '') or 'enslaved' in item.get('origin', '')]
        
        european_items = [item for item in CARIBBEAN_MUSIC_AND_INSTRUMENTS.values() 
                         if any(word in item.get('origin', '') for word in ['European', 'Spanish', 'British', 'French'])]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🌍 African Influences")
            st.write(f"**{len(african_items)}** items with African roots")
            african_countries = set(item.get('country', '') for item in african_items)
            st.write(f"Spread across **{len(african_countries)}** Caribbean territories")
            
        with col2:
            st.markdown("#### 🏰 European Influences")
            st.write(f"**{len(european_items)}** items with European influences")
            european_countries = set(item.get('country', '') for item in european_items)
            st.write(f"Found in **{len(european_countries)}** Caribbean territories")
        
        # Timeline analysis
        st.markdown("### ⏰ Historical Timeline")
        
        traditional_count = len([item for item in CARIBBEAN_MUSIC_AND_INSTRUMENTS.values() 
                               if 'Traditional' in item.get('era', '')])
        colonial_count = len([item for item in CARIBBEAN_MUSIC_AND_INSTRUMENTS.values() 
                            if 'Colonial' in item.get('era', '')])
        modern_count = len([item for item in CARIBBEAN_MUSIC_AND_INSTRUMENTS.values() 
                          if 'Modern' in item.get('era', '')])
        contemporary_count = len([item for item in CARIBBEAN_MUSIC_AND_INSTRUMENTS.values() 
                                if 'Contemporary' in item.get('era', '')])
        
        timeline_data = {
            "Traditional": traditional_count,
            "Colonial": colonial_count, 
            "Modern": modern_count,
            "Contemporary": contemporary_count
        }
        
        for era, count in timeline_data.items():
            if count > 0:
                st.write(f"**{era}:** {count} items")
        
        # Cultural significance themes
        st.markdown("### 🎭 Cultural Significance Themes")
        
        themes = {
            "Identity": len([item for item in CARIBBEAN_MUSIC_AND_INSTRUMENTS.values() 
                           if 'identity' in item.get('cultural_significance', '').lower()]),
            "Resistance": len([item for item in CARIBBEAN_MUSIC_AND_INSTRUMENTS.values() 
                             if 'resistance' in item.get('cultural_significance', '').lower()]),
            "Heritage": len([item for item in CARIBBEAN_MUSIC_AND_INSTRUMENTS.values() 
                           if 'heritage' in item.get('cultural_significance', '').lower()]),
            "Community": len([item for item in CARIBBEAN_MUSIC_AND_INSTRUMENTS.values() 
                            if 'community' in item.get('cultural_significance', '').lower()]),
            "Spiritual": len([item for item in CARIBBEAN_MUSIC_AND_INSTRUMENTS.values() 
                            if 'spiritual' in item.get('cultural_significance', '').lower()])
        }
        
        for theme, count in themes.items():
            if count > 0:
                st.write(f"**{theme}:** {count} items emphasize this theme")

# Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 20px; color: #666;">
        <p>🎵 Caribbean Music Explorer | Celebrating the Rich Musical Heritage of the Caribbean 🎵</p>
        <p>Educational tool for exploring Caribbean musical traditions and cultural connections</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()