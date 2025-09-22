import os, re, json, time
from datetime import datetime
from typing import List, Optional, Tuple, Dict
from dateutil import parser as dateparser

import pandas as pd
import requests
from bs4 import BeautifulSoup
import streamlit as st
from pydantic import BaseModel, Field, validator
import google.generativeai as genai

# ---------- CONFIG ----------
st.set_page_config(page_title="Caribbean Cultural Events Calendar", layout="wide", page_icon="🏝️")
DATA_PATH = "caribbean_events.csv"

# ---------- API KEY CONFIGURATION ----------
def get_api_key():
    """
    Get API key from multiple sources in order of preference:
    1. Hardcoded key (for quick setup)
    2. Streamlit secrets
    3. Environment variable
    """
    # REPLACE 'your_api_key_here' WITH YOUR ACTUAL GOOGLE GEMINI API KEY
    hardcoded_key = "AIzaSyCyMVeVnNR5I94GgPZalBHPGaeWCiUJLwg"  # PUT YOUR API KEY HERE!
    
    if hardcoded_key and hardcoded_key != "AIzaSyCyMVeVnNR5I94GgPZalBHPGaeWCiUJLwg":
        return hardcoded_key
    
    # Try Streamlit secrets
    try:
        if hasattr(st, 'secrets') and 'AIzaSyCyMVeVnNR5I94GgPZalBHPGaeWCiUJLwg' in st.secrets:
            return st.secrets['AIzaSyCyMVeVnNR5I94GgPZalBHPGaeWCiUJLwg']
    except Exception:
        pass
    
    # Try environment variable
    api_key = os.getenv('AIzaSyCyMVeVnNR5I94GgPZalBHPGaeWCiUJLwg')
    if api_key:
        return api_key
    
    return None

# Initialize API key silently
API_KEY = get_api_key()

# Check for temporary session key
if not API_KEY and 'temp_api_key' in st.session_state:
    API_KEY = st.session_state['temp_api_key']

if API_KEY:
    genai.configure(api_key=API_KEY)
    MODEL_NAME = "gemini-2.5-flash"

# ---------- CARIBBEAN COUNTRIES CONFIG ----------
CARIBBEAN_COUNTRIES = {
    "Antigua and Barbuda": {
        "flag": "🇦🇬",
        "sources": [
            "https://www.antiguanice.com/events/",
            "https://antiguabarbuda.org/events",
            "https://www.antiguacarnivals.com/",
        ]
    },
    "Bahamas": {
        "flag": "🇧🇸",
        "sources": [
            "https://www.bahamas.com/events",
            "https://www.bahamas.gov.bs/news",
            "https://junkanoonews.com/",
        ]
    },
    "Barbados": {
        "flag": "🇧🇧",
        "sources": [
            "https://www.visitbarbados.org/events-and-festivals",
            "https://cropoverworld.com/",
            "https://gisbarbados.gov.bb/news/",
        ]
    },
    "Belize": {
        "flag": "🇧🇿",
        "sources": [
            "https://www.travelbelize.org/events/",
            "https://www.belizenews.com/events/",
            "https://www.government.bz/news/",
        ]
    },
    "Cuba": {
        "flag": "🇨🇺",
        "sources": [
            "https://www.cubatravel.cu/en/events",
            "http://www.cubadebate.cu/",
            "https://www.habanafestival.cu/",
        ]
    },
    "Dominica": {
        "flag": "🇩🇲",
        "sources": [
            "https://dominica.dm/events/",
            "https://www.discoverdominica.com/events",
            "https://gov.dm/news",
        ]
    },
    "Dominican Republic": {
        "flag": "🇩🇴",
        "sources": [
            "https://www.godominicanrepublic.com/events/",
            "https://www.presidencia.gob.do/noticias",
            "https://carnavaldominicano.com/",
        ]
    },
    "Grenada": {
        "flag": "🇬🇩",
        "sources": [
            "https://www.grenadagrenadines.com/events/",
            "https://spicemasgrenada.com/",
            "https://www.gov.gd/news",
        ]
    },
    "Guyana": {
        "flag": "🇬🇾",
        "sources": [
            "https://www.guyana.org/events/",
            "https://dpi.gov.gy/",
            "https://guyanachronicle.com/events/",
        ]
    },
    "Haiti": {
        "flag": "🇭🇹",
        "sources": [
            "https://www.haititourisme.org/events",
            "https://www.haitilibre.com/en/",
            "https://carnavaldehaiti.com/",
        ]
    },
    "Jamaica": {
        "flag": "🇯🇲",
        "sources": [
            "https://www.visitjamaica.com/events/",
            "https://reggaesumfest.com/",
            "https://jis.gov.jm/news/",
        ]
    },
    "Puerto Rico": {
        "flag": "🇵🇷",
        "sources": [
            "https://www.discoverpuertorico.com/events",
            "https://www.sanjuanciudadpatrimonio.com/events",
            "https://www.gobierno.pr/noticias/",
        ]
    },
    "Saint Kitts and Nevis": {
        "flag": "🇰🇳",
        "sources": [
            "https://www.stkittstourism.kn/events/",
            "https://www.gov.kn/news",
            "https://sugarmascarnivals.com/",
        ]
    },
    "Saint Lucia": {
        "flag": "🇱🇨",
        "sources": [
            "https://www.stlucia.org/en/events/",
            "https://www.govt.lc/news",
            "https://www.stluciajazz.org/",
            "https://carnivalsaintlucia.com/events/",
            "https://www.stlucia.org/en/experiences/festivals-events/",
        ]
    },
    "Saint Vincent and the Grenadines": {
        "flag": "🇻🇨",
        "sources": [
            "https://discoversvg.com/events/",
            "https://www.gov.vc/news",
            "https://vincy-mas.com/",
        ]
    },
    "Suriname": {
        "flag": "🇸🇷",
        "sources": [
            "https://www.suriname.nu/events/",
            "https://www.gov.sr/nieuws/",
            "https://surinametourism.sr/events/",
        ]
    },
    "Trinidad and Tobago": {
        "flag": "🇹🇹",
        "sources": [
            "https://www.gotrinidandtobago.com/events/",
            "https://www.ncctt.org/",
            "https://www.gov.tt/news/",
            "https://www.trinidadcarnival.com/",
        ]
    }
}

# ---------- DATA MODEL ----------
class Event(BaseModel):
    name: str
    country: str
    start_date: str
    end_date: Optional[str] = ""
    location: Optional[str] = ""
    description: Optional[str] = ""
    category: Optional[str] = ""
    source_url: Optional[str] = ""
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

    @validator("start_date", "end_date", pre=True, always=True)
    def norm_date(cls, v):
        if not v:
            return ""
        try:
            return dateparser.parse(str(v)).date().isoformat()
        except Exception:
            return ""

# ---------- STORAGE ----------
def events_df() -> pd.DataFrame:
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
    else:
        df = pd.DataFrame()
    expected = ["name","country","start_date","end_date","location","description","category","source_url","created_at"]
    for c in expected:
        if c not in df.columns:
            df[c] = ""
    return df[expected]

def save_events(df: pd.DataFrame):
    df.to_csv(DATA_PATH, index=False)

# ---------- FETCHING ----------
def fetch_text(url: str, timeout: int = 20) -> str:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        r = requests.get(url, timeout=timeout, headers=headers)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        for tag in soup(["script","style","noscript","header","footer","nav"]): 
            tag.extract()
        text = soup.get_text(separator="\n")
        text = re.sub(r"\n{2,}", "\n", text)
        return text[:200000]
    except Exception as e:
        return f"[ERROR fetching {url}: {e}]"

# ---------- AI EXTRACTION ----------
def _try_parse_json_blocks(text: str):
    t = (text or "").strip()
    if t.startswith("```"):
        t = t.strip("`")
        if "\n" in t:
            first, rest = t.split("\n", 1)
            if first.lower().strip() in ("json",""):
                t = rest
    t = t.strip()
    try:
        return json.loads(t)
    except Exception:
        m = re.search(r"\[[\s\S]*\]", t)
        if m:
            try:
                return json.loads(m.group(0))
            except Exception:
                return None
        return None

def gemini_extract_events(raw_text: str, country: str, year: int, source_url: str = "") -> List[Event]:
    if not API_KEY:
        return []  # Silently return empty list if no API key
    
    prompt = f"""
You are an expert extractor for a Caribbean cultural events calendar.

From the text below, extract ONLY real public cultural events in **{country}** that occur in **{year}**.
Focus on festivals, carnivals, cultural celebrations, music events, national holidays, and tourism events.

If an event spans multiple days, include the full range.
If only month/year is present, set start_date to the 1st of that month and leave end_date empty.
Keep description ≤ 280 chars. Do not invent events.

Categorize each event as one of: Festival, Carnival, Music, Cultural, Religious, Sports, National Holiday, Tourism, Other

Return a JSON array of objects with keys:
name, country (use: {country}), start_date (YYYY-MM-DD), end_date (YYYY-MM-DD or empty), location, description, category, source_url (use: {source_url}).

TEXT:
---
{raw_text[:12000]}
---
JSON:
"""
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        resp = model.generate_content(prompt)
        parsed = _try_parse_json_blocks(getattr(resp, "text", "") or "")
        out: List[Event] = []
        if isinstance(parsed, list):
            for item in parsed:
                try:
                    item["source_url"] = source_url or item.get("source_url","")
                    item["country"] = country
                    out.append(Event(**item))
                except Exception:
                    continue
        return out
    except Exception:
        return []  # Silently return empty list on error

# ---------- DEDUP ----------
def _norm_name(n: str) -> str:
    return re.sub(r"\s+", " ", (n or "").strip().lower())

def dedup(existing: pd.DataFrame, new_events: List[Event]) -> Tuple[pd.DataFrame, int]:
    if existing.empty:
        existing_keys = set()
    else:
        existing_keys = set(
            (_norm_name(r["name"]), r["country"], str(r["start_date"])) 
            for _, r in existing.fillna("").iterrows()
        )
    
    add_rows = []
    for ev in new_events:
        key = (_norm_name(ev.name), ev.country, ev.start_date)
        if key in existing_keys:
            continue
        add_rows.append(ev.dict())
        existing_keys.add(key)
    
    if add_rows:
        updated = pd.concat([existing, pd.DataFrame(add_rows)], ignore_index=True)
        return updated, len(add_rows)
    return existing, 0

# ---------- UI ----------
st.title("🏝️ Caribbean Cultural Events Calendar")
st.markdown("Discover cultural events, festivals, and celebrations across the Caribbean islands!")

# Check API key status silently and show appropriate message
if not API_KEY:
    st.info("🔧 **Setup Required**: This app requires a Google Gemini API key to collect events automatically. You can still view existing events below, but collection features will be disabled until an API key is configured.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        **To enable event collection:**
        
        1. **For Streamlit Cloud**: Add `GOOGLE_API_KEY` to your app's secrets
        2. **For Local Development**: Set environment variable: `export GOOGLE_API_KEY=your_key_here`
        
        Get your free API key from: https://makersuite.google.com/app/apikey
        """)
    
    with col2:
        with st.container():
            st.markdown("**🚀 Quick Test**")
            temp_api_key = st.text_input(
                "Enter API Key for this session:",
                type="password",
                help="Temporary key for testing - not saved"
            )
            if temp_api_key and st.button("Apply Key"):
                try:
                    genai.configure(api_key=temp_api_key)
                    # Test the key with a simple request
                    model = genai.GenerativeModel("gemini-2.5-flash")
                    test_response = model.generate_content("Hello")
                    if test_response:
                        st.session_state['temp_api_key'] = temp_api_key
                        st.success("✅ API key works! Refresh page to use.")
                        st.rerun()
                except Exception as e:
                    st.error("❌ Invalid API key")
    
    with st.expander("🔒 Why is an API key needed?"):
        st.markdown("""
        This application uses Google's Gemini AI to automatically extract event information from Caribbean tourism websites. 
        The API key allows the app to:
        - Parse event details from web pages
        - Extract dates, locations, and descriptions
        - Categorize events automatically
        - Ensure high-quality event data
        """)

# Sidebar for controls
with st.sidebar:
    st.header("🎯 Event Collection")
    
    # Country selection
    selected_countries = st.multiselect(
        "Select Caribbean Countries",
        options=list(CARIBBEAN_COUNTRIES.keys()),
        default=["Saint Lucia"],
        help="Choose one or more Caribbean countries to collect events from"
    )
    
    # Year selection
    col1, col2 = st.columns(2)
    target_year = col1.number_input("Target year", min_value=2020, max_value=2100, value=datetime.now().year, step=1)
    include_next = col2.checkbox("Also next year", value=False)
    
    # Collect button - disabled if no API key
    if API_KEY:
        run_collect = st.button("🔄 Collect Events", type="primary", use_container_width=True)
    else:
        st.button("🔄 Collect Events", type="primary", use_container_width=True, disabled=True)
        st.caption("⚠️ API key required for collection")
        run_collect = False
    
    st.divider()
    
    # Manual input section
    st.header("✍️ Manual Entry")
    manual_country = st.selectbox("Country for manual entry", list(CARIBBEAN_COUNTRIES.keys()))
    
    option = st.radio("Method:", ["Paste text", "Fetch URL"], horizontal=True)
    
    raw_text = ""
    manual_source_url = ""
    
    if option == "Paste text":
        raw_text = st.text_area("Event details", height=100)
    else:
        manual_source_url = st.text_input("URL to fetch")
        if manual_source_url and st.button("Fetch"):
            with st.spinner("Fetching..."):
                raw_text = fetch_text(manual_source_url)
                if raw_text and not raw_text.startswith("[ERROR"):
                    st.success("✅ Text fetched!")
                else:
                    st.error("❌ Fetch failed")

# Main content area
if run_collect and selected_countries and API_KEY:
    df = events_df()
    years_to_collect = [int(target_year)]
    if include_next:
        years_to_collect.append(int(target_year) + 1)

    total_found = 0
    total_added = 0
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    total_operations = len(selected_countries) * len(years_to_collect)
    current_operation = 0
    
    for country in selected_countries:
        country_data = CARIBBEAN_COUNTRIES[country]
        flag = country_data["flag"]
        sources = country_data["sources"]
        
        status_text.write(f"🔍 Collecting events for {flag} **{country}**...")
        
        for source_url in sources:
            try:
                text = fetch_text(source_url)
                if not text.startswith("[ERROR"):
                    for year in years_to_collect:
                        extracted = gemini_extract_events(text, country, year, source_url)
                        total_found += len(extracted)
                        df, added = dedup(df, extracted)
                        total_added += added
                        
                        current_operation += 1
                        progress_bar.progress(current_operation / total_operations)
                        
            except Exception as e:
                st.warning(f"⚠️ Failed to process {source_url}: {e}")
            
            time.sleep(0.5)  # Rate limiting
    
    save_events(df)
    status_text.empty()
    progress_bar.empty()
    st.success(f"🎉 Collection complete! Found {total_found} events, added {total_added} new ones after deduplication.")

# Manual processing
if raw_text and API_KEY:
    if st.sidebar.button("Extract Events"):
        with st.spinner("Processing with AI..."):
            manual_events = gemini_extract_events(raw_text, manual_country, target_year, manual_source_url)
            if manual_events:
                st.sidebar.success(f"Found {len(manual_events)} events!")
                if st.sidebar.button("Save Events"):
                    df0 = events_df()
                    df1, added = dedup(df0, manual_events)
                    save_events(df1)
                    st.sidebar.success(f"✅ Saved {added} new events!")
elif raw_text and not API_KEY:
    st.sidebar.button("Extract Events", disabled=True)
    st.sidebar.caption("⚠️ API key required for extraction")

# ---------- DISPLAY CALENDAR ----------
st.header("📅 Caribbean Events Calendar")

df = events_df().copy()

if df.empty:
    st.info("No events yet. Use the sidebar to collect events from Caribbean countries!")
else:
    # Filters
    col1, col2, col3, col4 = st.columns(4)
    
    # Country filter
    available_countries = sorted(df["country"].unique())
    country_filter = col1.selectbox("🏝️ Country", ["All Countries"] + available_countries)
    
    # Year filter
    valid_years = sorted({s[:4] for s in df["start_date"].fillna("") if len(str(s)) >= 4 and str(s)[:4].isdigit()})
    year_filter = col2.selectbox("📅 Year", ["All Years"] + valid_years)
    
    # Category filter
    available_categories = sorted([cat for cat in df["category"].unique() if cat])
    category_filter = col3.selectbox("🎭 Category", ["All Categories"] + available_categories)
    
    # Month filter
    month_filter = "All Months"
    if year_filter != "All Years":
        months_in_year = sorted({
            dateparser.parse(d).month
            for d in df["start_date"].dropna()
            if d.startswith(year_filter)
        })
        month_names = ["All Months"] + [datetime(1900, m, 1).strftime("%B") for m in months_in_year]
        month_filter = col4.selectbox("🗓️ Month", month_names)
    else:
        col4.selectbox("🗓️ Month", ["All Months"], disabled=True)
    
    # Apply filters
    filtered_df = df.copy()
    
    if country_filter != "All Countries":
        filtered_df = filtered_df[filtered_df["country"] == country_filter]
    
    if year_filter != "All Years":
        filtered_df = filtered_df[filtered_df["start_date"].fillna("").str.startswith(year_filter)]
        
        if month_filter != "All Months":
            month_num = datetime.strptime(month_filter, "%B").month
            filtered_df = filtered_df[filtered_df["start_date"].apply(
                lambda d: dateparser.parse(d).month == month_num if d else False
            )]
    
    if category_filter != "All Categories":
        filtered_df = filtered_df[filtered_df["category"] == category_filter]
    
    # Display stats
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Events", len(filtered_df))
    col2.metric("Countries", len(filtered_df["country"].unique()) if not filtered_df.empty else 0)
    col3.metric("Categories", len(filtered_df["category"].unique()) if not filtered_df.empty else 0)
    
    # Display events
    if filtered_df.empty:
        st.info("No events match your current filters.")
    else:
        for _, row in filtered_df.sort_values(["start_date", "name"]).iterrows():
            country_flag = CARIBBEAN_COUNTRIES.get(row["country"], {}).get("flag", "🏝️")
            
            # Category emoji mapping
            category_emoji = {
                "Festival": "🎪", "Carnival": "🎭", "Music": "🎵", "Cultural": "🎨",
                "Religious": "⛪", "Sports": "🏆", "National Holiday": "🇺🇸", 
                "Tourism": "🏖️", "Other": "📅"
            }.get(row.get("category", ""), "📅")
            
            date_range = row['start_date']
            if row['end_date'] and str(row['end_date']).strip():
                date_range += f" - {row['end_date']}"
            
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px; 
                border-radius: 15px; 
                margin-bottom: 15px; 
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                color: white;
            ">
                <div style="display: flex; justify-content: between; align-items: start; margin-bottom: 10px;">
                    <h3 style="margin: 0; color: white;">{category_emoji} {row['name']}</h3>
                    <span style="font-size: 1.5em;">{country_flag}</span>
                </div>
                <p style="margin: 5px 0;"><strong>📅 {date_range}</strong></p>
                <p style="margin: 5px 0;"><strong>🏝️ {row['country']}</strong></p>
                {f"<p style='margin: 5px 0;'><strong>📍 {row['location']}</strong></p>" if row['location'] else ""}
                {f"<p style='margin: 10px 0 0 0;'>{row['description']}</p>" if row['description'] else ""}
                <p style="font-size: 0.85em; margin-top: 10px; opacity: 0.8;">
                    {f"Category: {row['category']}" if row['category'] else ""} 
                    {" | " if row['category'] and row['source_url'] else ""}
                    {f"<a href='{row['source_url']}' style='color: #87CEEB;'>Source</a>" if row['source_url'] else ""}
                </p>
            </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("🏝️ **Caribbean Cultural Events Calendar** - Celebrating the rich cultural heritage of the Caribbean islands!")