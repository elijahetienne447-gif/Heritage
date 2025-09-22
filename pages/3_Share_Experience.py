import os
import io
import uuid
import shutil
import sqlite3
from datetime import datetime, date
from pathlib import Path
from typing import Optional, List

import streamlit as st
from PIL import Image

# ------------------------------------
# Config & paths
# ------------------------------------
st.set_page_config(page_title="Caribbean Experience Stories", layout="wide")
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

DB_PATH = "experiences.db"

# Caribbean countries and territories
CARIBBEAN_COUNTRIES = {
    "antigua_barbuda": "🇦🇬 Antigua and Barbuda",
    "bahamas": "🇧🇸 Bahamas", 
    "barbados": "🇧🇧 Barbados",
    "belize": "🇧🇿 Belize",
    "dominica": "🇩🇲 Dominica",
    "dominican_republic": "🇩🇴 Dominican Republic",
    "grenada": "🇬🇩 Grenada",
    "guyana": "🇬🇾 Guyana",
    "haiti": "🇭🇹 Haiti",
    "jamaica": "🇯🇲 Jamaica",
    "saint_kitts_nevis": "🇰🇳 Saint Kitts and Nevis",
    "saint_lucia": "🇱🇨 Saint Lucia",
    "saint_vincent_grenadines": "🇻🇨 Saint Vincent and the Grenadines",
    "suriname": "🇸🇷 Suriname",
    "trinidad_tobago": "🇹🇹 Trinidad and Tobago",
    "cuba": "🇨🇺 Cuba",
    "puerto_rico": "🇵🇷 Puerto Rico",
    "martinique": "🇲🇶 Martinique",
    "guadeloupe": "🇬🇵 Guadeloupe",
    "curacao": "🇨🇼 Curaçao",
    "aruba": "🇦🇼 Aruba",
    "bonaire": "🇧🇶 Bonaire"
}

EXPERIENCE_CATEGORIES = {
    "food": "🍽️ Food & Cuisine",
    "culture": "🎭 Culture & Traditions", 
    "adventure": "🏄‍♀️ Adventure & Sports",
    "nature": "🌺 Nature & Wildlife",
    "music": "🎵 Music & Dance",
    "festival": "🎉 Festivals & Celebrations",
    "history": "🏛️ History & Heritage",
    "beach": "🏖️ Beach Life",
    "nightlife": "🌃 Nightlife & Entertainment",
    "local_life": "🏠 Local Life",
    "travel_tips": "✈️ Travel Tips",
    "family": "👨‍👩‍👧‍👦 Family Experiences",
    "romance": "💕 Romance & Couples",
    "solo": "🚶‍♀️ Solo Adventures",
    "business": "💼 Business & Work",
    "education": "📚 Learning & Education",
    "other": "📖 Other Stories"
}

EXPERIENCE_TYPES = {
    "story": "📖 Story",
    "photo": "📸 Photo Story", 
    "tip": "💡 Travel Tip",
    "review": "⭐ Review",
    "guide": "🗺️ Guide"
}

# ------------------------------------
# DB utilities
# ------------------------------------
def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            display_name TEXT NOT NULL,
            bio TEXT,
            home_country TEXT,
            profile_image TEXT,
            created_at TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS experiences (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            country TEXT NOT NULL,
            title TEXT NOT NULL,
            story TEXT,
            category TEXT NOT NULL,
            experience_type TEXT NOT NULL,
            location TEXT,
            visit_date DATE,
            rating INTEGER, -- 1-5 stars
            media_paths TEXT, -- JSON array of image/video paths
            tags TEXT, -- comma-separated tags
            budget_info TEXT,
            duration TEXT,
            best_time TEXT,
            tips TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS experience_reactions (
            user_id TEXT NOT NULL,
            experience_id TEXT NOT NULL,
            reaction_type TEXT DEFAULT 'like', -- 'like', 'love', 'wow', 'helpful'
            created_at TEXT NOT NULL,
            PRIMARY KEY (user_id, experience_id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (experience_id) REFERENCES experiences(id)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS experience_comments (
            id TEXT PRIMARY KEY,
            experience_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            text TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (experience_id) REFERENCES experiences(id)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS saved_experiences (
            user_id TEXT NOT NULL,
            experience_id TEXT NOT NULL,
            created_at TEXT NOT NULL,
            PRIMARY KEY (user_id, experience_id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (experience_id) REFERENCES experiences(id)
        )
    """)
    conn.commit()
    conn.close()

def ensure_user(display_name: str, bio: str = None, home_country: str = None) -> str:
    """Create or load a local pseudo-user stored in session."""
    if "user_id" not in st.session_state:
        user_id = str(uuid.uuid4())
        st.session_state.user_id = user_id
        conn = get_conn()
        conn.execute(
            "INSERT INTO users (id, display_name, bio, home_country, created_at) VALUES (?, ?, ?, ?, ?)",
            (user_id, display_name or "Traveler", bio, home_country, datetime.utcnow().isoformat())
        )
        conn.commit()
        conn.close()
    return st.session_state.user_id

def get_user_info(user_id: str) -> dict:
    conn = get_conn()
    row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    if row:
        return dict(row)
    return {"display_name": "Unknown", "bio": "", "home_country": ""}

# ------------------------------------
# Core actions
# ------------------------------------
def create_experience(user_id: str, experience_data: dict, media_files: List = None) -> Optional[str]:
    import json
    
    media_paths = []
    if media_files:
        for media_file in media_files:
            if media_file:
                ext = Path(media_file.name).suffix.lower()
                safe_name = f"{uuid.uuid4().hex}{ext}"
                out_path = UPLOAD_DIR / safe_name
                with open(out_path, "wb") as f:
                    f.write(media_file.read())
                media_paths.append(str(out_path.as_posix()))

    experience_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()
    
    conn = get_conn()
    conn.execute("""
        INSERT INTO experiences (
            id, user_id, country, title, story, category, experience_type,
            location, visit_date, rating, media_paths, tags, budget_info,
            duration, best_time, tips, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        experience_id, user_id, experience_data["country"], experience_data["title"], 
        experience_data["story"], experience_data["category"], experience_data["experience_type"],
        experience_data.get("location"), experience_data.get("visit_date"), 
        experience_data.get("rating"), json.dumps(media_paths),
        experience_data.get("tags"), experience_data.get("budget_info"),
        experience_data.get("duration"), experience_data.get("best_time"),
        experience_data.get("tips"), now, now
    ))
    conn.commit()
    conn.close()
    return experience_id

def toggle_reaction(user_id: str, experience_id: str, reaction_type: str = "like"):
    conn = get_conn()
    cur = conn.cursor()
    exists = cur.execute(
        "SELECT reaction_type FROM experience_reactions WHERE user_id=? AND experience_id=?", 
        (user_id, experience_id)
    ).fetchone()
    
    if exists:
        if exists["reaction_type"] == reaction_type:
            # Remove if same reaction clicked again
            cur.execute("DELETE FROM experience_reactions WHERE user_id=? AND experience_id=?", 
                       (user_id, experience_id))
        else:
            # Update reaction
            cur.execute(
                "UPDATE experience_reactions SET reaction_type=? WHERE user_id=? AND experience_id=?",
                (reaction_type, user_id, experience_id)
            )
    else:
        cur.execute(
            "INSERT INTO experience_reactions (user_id, experience_id, reaction_type, created_at) VALUES (?, ?, ?, ?)",
            (user_id, experience_id, reaction_type, datetime.utcnow().isoformat())
        )
    conn.commit()
    conn.close()

def toggle_save(user_id: str, experience_id: str):
    conn = get_conn()
    cur = conn.cursor()
    exists = cur.execute(
        "SELECT 1 FROM saved_experiences WHERE user_id=? AND experience_id=?", 
        (user_id, experience_id)
    ).fetchone()
    
    if exists:
        cur.execute("DELETE FROM saved_experiences WHERE user_id=? AND experience_id=?", 
                   (user_id, experience_id))
    else:
        cur.execute(
            "INSERT INTO saved_experiences (user_id, experience_id, created_at) VALUES (?, ?, ?)",
            (user_id, experience_id, datetime.utcnow().isoformat())
        )
    conn.commit()
    conn.close()

def add_comment(user_id: str, experience_id: str, text: str):
    if not text.strip():
        return
    conn = get_conn()
    conn.execute(
        "INSERT INTO experience_comments (id, experience_id, user_id, text, created_at) VALUES (?, ?, ?, ?, ?)",
        (str(uuid.uuid4()), experience_id, user_id, text.strip(), datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()

def get_reaction_counts(experience_id: str) -> dict:
    conn = get_conn()
    reactions = {}
    for reaction in ["like", "love", "wow", "helpful"]:
        count = conn.execute(
            "SELECT COUNT(*) AS n FROM experience_reactions WHERE experience_id=? AND reaction_type=?", 
            (experience_id, reaction)
        ).fetchone()["n"]
        reactions[reaction] = count
    
    saved_count = conn.execute(
        "SELECT COUNT(*) AS n FROM saved_experiences WHERE experience_id=?", 
        (experience_id,)
    ).fetchone()["n"]
    reactions["saved"] = saved_count
    
    conn.close()
    return reactions

def get_comments(experience_id: str):
    conn = get_conn()
    rows = conn.execute("""
        SELECT c.text, c.created_at, u.display_name, u.home_country
        FROM experience_comments c
        JOIN users u ON u.id = c.user_id
        WHERE c.experience_id = ?
        ORDER BY c.created_at DESC
    """, (experience_id,)).fetchall()
    conn.close()
    return rows

def get_experiences(country_filter: Optional[str] = None, category_filter: Optional[str] = None, 
                   type_filter: Optional[str] = None, single_experience_id: Optional[str] = None):
    conn = get_conn()
    
    query = """
        SELECT e.*, u.display_name, u.home_country as author_country
        FROM experiences e
        JOIN users u ON u.id = e.user_id
    """
    params = []
    conditions = []
    
    if single_experience_id:
        conditions.append("e.id = ?")
        params.append(single_experience_id)
    else:
        if country_filter and country_filter != "all":
            conditions.append("e.country = ?")
            params.append(country_filter)
        if category_filter and category_filter != "all":
            conditions.append("e.category = ?")
            params.append(category_filter)
        if type_filter and type_filter != "all":
            conditions.append("e.experience_type = ?")
            params.append(type_filter)
    
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    
    query += " ORDER BY e.created_at DESC"
    
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return rows

# ------------------------------------
# UI helpers
# ------------------------------------
def human_time(ts: str) -> str:
    try:
        dt = datetime.fromisoformat(ts.replace("Z",""))
        return dt.strftime("%b %d, %Y")
    except Exception:
        return ts

def render_rating(rating: int):
    if rating:
        stars = "⭐" * rating + "☆" * (5 - rating)
        return f"{stars} ({rating}/5)"
    return ""

def render_media_gallery(media_paths_json: str):
    if not media_paths_json:
        return
    
    import json
    try:
        media_paths = json.loads(media_paths_json)
        if media_paths:
            # Create columns for multiple images
            if len(media_paths) == 1:
                if Path(media_paths[0]).exists():
                    img = Image.open(media_paths[0])
                    st.image(img, use_container_width=True)
            else:
                cols = st.columns(min(len(media_paths), 3))
                for i, path in enumerate(media_paths[:6]):  # Show max 6 images
                    if Path(path).exists():
                        try:
                            img = Image.open(path)
                            with cols[i % 3]:
                                st.image(img, use_container_width=True)
                        except Exception:
                            continue
    except Exception:
        pass

def format_tags(tags: str) -> str:
    if not tags:
        return ""
    tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
    return " ".join([f"#{tag}" for tag in tag_list])

# ------------------------------------
# App
# ------------------------------------
init_db()

st.title("🏝️ Caribbean Experience Stories")
st.markdown("Share your Caribbean adventures, discover hidden gems, and connect with fellow travelers")

# Sidebar for user profile and story creation
with st.sidebar:
    st.header("👤 Your Profile")
    display_name = st.text_input("Name", value=st.session_state.get("display_name", ""))
    bio = st.text_area("Bio", value=st.session_state.get("bio", ""), 
                       placeholder="Tell us about yourself...")
    home_country = st.selectbox("Home Country/Territory", 
                               options=[""] + list(CARIBBEAN_COUNTRIES.keys()),
                               format_func=lambda x: CARIBBEAN_COUNTRIES[x] if x else "Select...",
                               index=0)
    
    if st.button("Update Profile"):
        st.session_state.display_name = display_name
        st.session_state.bio = bio
        st.session_state.home_country = home_country
        ensure_user(display_name or "Traveler", bio, home_country)
        st.success("Profile updated! 🎉")
    
    user_id = ensure_user(display_name or "Traveler", bio, home_country)
    
    st.markdown("---")
    st.header("🌟 Filters")
    
    # Country filter
    country_options = {"all": "🌎 All Countries"} | CARIBBEAN_COUNTRIES
    selected_country = st.selectbox("Country Visited", 
                                   options=list(country_options.keys()),
                                   format_func=lambda x: country_options[x],
                                   index=0)
    
    # Category filter
    category_options = {"all": "🏝️ All Experiences"} | EXPERIENCE_CATEGORIES
    selected_category = st.selectbox("Experience Type",
                                    options=list(category_options.keys()),
                                    format_func=lambda x: category_options[x],
                                    index=0)
    
    # Experience type filter
    type_options = {"all": "📚 All Formats"} | EXPERIENCE_TYPES
    selected_type = st.selectbox("Story Format",
                                options=list(type_options.keys()),
                                format_func=lambda x: type_options[x],
                                index=0)
    
    st.markdown("---")
    st.header("✍️ Share Your Story")
    
    with st.form("create_experience_form", clear_on_submit=True):
        exp_country = st.selectbox("Which Caribbean destination?", 
                                  options=list(CARIBBEAN_COUNTRIES.keys()),
                                  format_func=lambda x: CARIBBEAN_COUNTRIES[x])
        
        exp_title = st.text_input("Experience Title*", 
                                 placeholder="e.g., Swimming with Stingrays in Grand Cayman")
        
        exp_type = st.selectbox("Story Format",
                               options=list(EXPERIENCE_TYPES.keys()),
                               format_func=lambda x: EXPERIENCE_TYPES[x])
        
        exp_category = st.selectbox("Category",
                                   options=list(EXPERIENCE_CATEGORIES.keys()),
                                   format_func=lambda x: EXPERIENCE_CATEGORIES[x])
        
        exp_story = st.text_area("Your Story*", height=150,
                                placeholder="Share your experience, what made it special, and what others should know...")
        
        col1, col2 = st.columns(2)
        with col1:
            exp_location = st.text_input("Specific Location", placeholder="e.g., Seven Mile Beach")
            exp_visit_date = st.date_input("When did you visit?", value=None)
            exp_rating = st.select_slider("Rate your experience", options=[1,2,3,4,5], value=5)
        
        with col2:
            exp_duration = st.text_input("Duration", placeholder="e.g., 3 days, half day")
            exp_budget = st.text_input("Budget Info", placeholder="e.g., $50 per person, Free")
            exp_best_time = st.text_input("Best time to visit", placeholder="e.g., Early morning, December-April")
        
        exp_tips = st.text_area("Travel Tips", 
                               placeholder="Any tips for future visitors?")
        
        exp_tags = st.text_input("Tags", placeholder="snorkeling, family-friendly, romantic, adventure")
        
        exp_media = st.file_uploader("Upload Photos/Videos", 
                                    type=["jpg","jpeg","png","gif","mp4","mov"],
                                    accept_multiple_files=True)
        
        submitted = st.form_submit_button("🌟 Share Experience")
        
        if submitted and exp_title and exp_story and exp_country:
            experience_data = {
                "country": exp_country,
                "title": exp_title,
                "story": exp_story,
                "category": exp_category,
                "experience_type": exp_type,
                "location": exp_location,
                "visit_date": exp_visit_date.isoformat() if exp_visit_date else None,
                "rating": exp_rating,
                "tags": exp_tags,
                "budget_info": exp_budget,
                "duration": exp_duration,
                "best_time": exp_best_time,
                "tips": exp_tips
            }
            
            exp_id = create_experience(user_id, experience_data, exp_media)
            st.success("Experience shared successfully! 🌟")
            st.rerun()

# Main content area
country_filter = selected_country if selected_country != "all" else None
category_filter = selected_category if selected_category != "all" else None
type_filter = selected_type if selected_type != "all" else None

# Check for single experience view
q = st.query_params
single_experience_id = q.get("story", None)

experiences = get_experiences(country_filter=country_filter, 
                             category_filter=category_filter,
                             type_filter=type_filter,
                             single_experience_id=single_experience_id)

if not experiences:
    st.info("🔍 No stories found matching your criteria. Be the first to share an experience!")
else:
    # Display current filters
    if not single_experience_id:
        filter_text = []
        if country_filter:
            filter_text.append(f"{CARIBBEAN_COUNTRIES[country_filter]}")
        if category_filter:
            filter_text.append(f"{EXPERIENCE_CATEGORIES[category_filter]}")
        if type_filter:
            filter_text.append(f"{EXPERIENCE_TYPES[type_filter]}")
        
        if filter_text:
            st.markdown(f"**Showing {len(experiences)} stories** • {' • '.join(filter_text)}")
        else:
            st.markdown(f"**Showing {len(experiences)} stories from across the Caribbean**")
        st.markdown("---")
    
    for exp in experiences:
        exp_id = exp["id"]
        title = exp["title"]
        story = exp["story"] or ""
        country = exp["country"]
        category = exp["category"]
        exp_type = exp["experience_type"]
        author = exp["display_name"]
        author_country = exp["author_country"]
        location = exp["location"]
        visit_date = exp["visit_date"]
        rating = exp["rating"]
        budget_info = exp["budget_info"]
        duration = exp["duration"]
        best_time = exp["best_time"]
        tips = exp["tips"]
        tags = exp["tags"]
        created_at = human_time(exp["created_at"])
        
        with st.container():
            st.markdown(
                """
                <div style="background:#ffffff;border-radius:20px;padding:24px;margin-bottom:28px;
                            box-shadow:0 6px 16px rgba(0,0,0,.08);border:1px solid #e8e8e8;">
                """,
                unsafe_allow_html=True
            )
            
            # Story header
            col1, col2 = st.columns([0.85, 0.15])
            with col1:
                country_flag = CARIBBEAN_COUNTRIES[country]
                type_icon = EXPERIENCE_TYPES[exp_type]
                category_icon = EXPERIENCE_CATEGORIES[category]
                
                st.markdown(f"## {title}")
                author_info = f"**{author}**"
                if author_country and author_country in CARIBBEAN_COUNTRIES:
                    author_info += f" from {CARIBBEAN_COUNTRIES[author_country]}"
                
                st.markdown(f"{type_icon} • {category_icon} • {country_flag} • {author_info} • {created_at}")
            
            with col2:
                if not single_experience_id:
                    if st.button("🔗", key=f"share_{exp_id}", help="Share this story"):
                        st.query_params["story"] = exp_id
                        st.rerun()
            
            # Experience media
            render_media_gallery(exp["media_paths"])
            
            # Location and rating
            info_items = []
            if location:
                info_items.append(f"📍 **{location}**")
            if visit_date:
                visit_dt = datetime.fromisoformat(visit_date)
                info_items.append(f"📅 Visited {visit_dt.strftime('%B %Y')}")
            if rating:
                info_items.append(f"⭐ {render_rating(rating)}")
            
            if info_items:
                st.markdown(" • ".join(info_items))
            
            # Main story
            st.markdown(f"### {author}'s Experience")
            st.markdown(story)
            
            # Additional info sections
            info_sections = []
            if duration:
                info_sections.append(f"**Duration:** {duration}")
            if budget_info:
                info_sections.append(f"**Budget:** {budget_info}")
            if best_time:
                info_sections.append(f"**Best Time:** {best_time}")
            
            if info_sections:
                st.markdown(" • ".join(info_sections))
            
            if tips:
                st.markdown("### 💡 Travel Tips")
                st.markdown(tips)
            
            if tags:
                st.markdown(f"**Tags:** {format_tags(tags)}")
            
            # Reactions and interactions
            reactions = get_reaction_counts(exp_id)
            
            col_like, col_love, col_wow, col_helpful, col_save, col_comment = st.columns(6)
            
            reaction_buttons = [
                (col_like, "👍", "like", f"Like ({reactions['like']})"),
                (col_love, "❤️", "love", f"Love ({reactions['love']})"),
                (col_wow, "😍", "wow", f"Wow ({reactions['wow']})"),
                (col_helpful, "🙏", "helpful", f"Helpful ({reactions['helpful']})"),
            ]
            
            for col, emoji, reaction_type, label in reaction_buttons:
                with col:
                    if st.button(f"{emoji} {reactions[reaction_type]}", 
                               key=f"{reaction_type}_{exp_id}",
                               help=label):
                        toggle_reaction(user_id, exp_id, reaction_type)
                        st.rerun()
            
            with col_save:
                if st.button(f"🔖 {reactions['saved']}", 
                           key=f"save_{exp_id}",
                           help="Save this story"):
                    toggle_save(user_id, exp_id)
                    st.rerun()
            
            with col_comment:
                st.write("💬 **Comments**")
            
            # Comments section
            comments = get_comments(exp_id)
            if comments:
                st.markdown("### Comments")
                for comment in comments:
                    commenter_info = comment['display_name']
                    if comment['home_country'] and comment['home_country'] in CARIBBEAN_COUNTRIES:
                        commenter_info += f" • {CARIBBEAN_COUNTRIES[comment['home_country']]}"
                    
                    st.markdown(
                        f"<div style='background:#f8f9fa;padding:16px;border-radius:12px;margin:12px 0'>"
                        f"<strong>{commenter_info}</strong> "
                        f"<span style='color:#666;font-size:0.9em'>{human_time(comment['created_at'])}</span><br><br>"
                        f"{comment['text']}</div>", 
                        unsafe_allow_html=True
                    )
            
            # Add comment form
            with st.form(key=f"comment_form_{exp_id}", clear_on_submit=True):
                comment_text = st.text_area("Share your thoughts or ask a question...", 
                                          key=f"comment_text_{exp_id}")
                if st.form_submit_button("💬 Add Comment"):
                    add_comment(user_id, exp_id, comment_text)
                    st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:#888;margin-top:32px;margin-bottom:32px'>"
    "🏝️ Caribbean Experience Stories • Sharing the magic of Caribbean culture and adventures<br>"
    "Built with ❤️ for Caribbean communities worldwide</div>",
    unsafe_allow_html=True
)