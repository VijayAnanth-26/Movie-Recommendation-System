import streamlit as st
from recommend import recommend

# Streamlit App Interface
st.title('🎬 Movie Recommendation System')
st.write("Welcome to the Movie Recommendation System!")

movie_name = st.text_input('Enter a Movie Name', '')

if movie_name:
    recommendations = recommend(movie_name)
    
    if recommendations[0] == "Movie not found!":
        st.write("❌ Movie not found! Try again.")
    else:
        st.write(f"\n💡 Top 5 movies similar to '{movie_name}':")
        for idx, title in enumerate(recommendations, 1):
            st.write(f"{idx}. {title}")
