import streamlit as st
from recommend import recommend

st.set_page_config(page_title="🎬 Movie Recommender", page_icon="🎥", layout="wide")

# --- Dark Theme Styling ---
st.markdown("""
    <style>
    body {
        background-color: #121212;
        color: #ffffff;
    }
    .stApp {
        background-color: #121212;
    }
    .title-style {
        color: #ffffff;
        font-size: 42px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 0.3em;
    }
    .subtitle-style {
        color: #bbbbbb;
        font-size: 18px;
        text-align: center;
        margin-top: -1em;
        margin-bottom: 1.5em;
    }
    .movie-box {
        background-color: #1f1f1f;
        padding: 1.2em;
        border-radius: 10px;
        margin-bottom: 10px;
        border: 1px solid #333;
        box-shadow: 0px 0px 10px rgba(255,255,255,0.05);
    }
    .stTextInput > div > div > input {
        background-color: #2c2c2c;
        color: #ffffff;
        border: 1px solid #444;
    }
    .stButton>button {
        background-color: #444444;
        color: white;
        border-radius: 8px;
        border: none;
    }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown('<div class="title-style">🎬 Movie Recommendation System</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-style">Enter a movie you like, and get 5 similar ones recommended instantly!</div>', unsafe_allow_html=True)

# --- Input Section ---
movie_name = st.text_input('🔍 Enter a Movie Name', placeholder="e.g. Inception, Titanic, The Matrix")
col1, col2 = st.columns([1, 5])
with col1:
    recommend_clicked = st.button("🚀 Recommend")

# --- Output Section ---
if recommend_clicked:
    if movie_name:
        with st.spinner("🔎 Finding similar movies..."):
            recommendations = recommend(movie_name)

        if recommendations[0] == "Movie not found!":
            st.error("❌ Movie not found! Please try a different title.")
        else:
            st.markdown("---")
            st.success(f"🎉 Top 5 Recommendations for **'{movie_name.title()}'**:")
            for idx, title in enumerate(recommendations, 1):
                st.markdown(f"""<div class="movie-box">
                    <h5>🎬 {idx}. {title}</h5>
                </div>""", unsafe_allow_html=True)
    else:
        st.warning("⚠️ Please enter a movie name to get recommendations.")
