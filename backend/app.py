import streamlit as st
from recommend import recommend, get_all_genres

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

st.title('🎬 Movie Recommendation System')
st.subheader("Welcome! Enter a movie you like and discover similar ones.")

# Input movie name
movie_name = st.text_input('🔍 Enter a Movie Name:', placeholder="e.g. Inception")

# Genre dropdown
genres = get_all_genres()
selected_genre = st.selectbox("🎯 Filter by Genre (Optional):", options=["All"] + genres)

# Recommend button
if st.button("Recommend"):
    if movie_name:
        with st.spinner("Fetching recommendations..."):
            genre_filter = None if selected_genre == "All" else selected_genre
            recommendations = recommend(movie_name, selected_genre=genre_filter)

        if recommendations[0] == "Movie not found!":
            st.error("❌ Movie not found! Please try a different title.")
        else:
            st.success(f"💡 Top 5 movies similar to '{movie_name.title()}'" +
                       (f" in genre '{selected_genre}'" if genre_filter else "") + ":")
            cols = st.columns(2)
            for idx, title in enumerate(recommendations, 1):
                with cols[idx % 2]:
                    st.markdown(f"**{idx}. {title}**")
    else:
        st.warning("Please enter a movie name to get recommendations.")
