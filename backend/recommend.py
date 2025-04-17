import pandas as pd
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load data
movies = pd.read_csv('dataset/tmdb_5000_movies.csv')
credits = pd.read_csv('dataset/tmdb_5000_credits.csv')
credits.columns = ['id', 'title', 'cast', 'crew']
movies = movies.merge(credits, on='title')

# Rename the id_x column to movie_id
movies.rename(columns={'id_x': 'movie_id'}, inplace=True)

# Select relevant columns
movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
movies.dropna(inplace=True)

# Functions to extract information
def convert(obj):
    return [i['name'] for i in ast.literal_eval(obj)]

def convert_cast(obj):
    return [i['name'] for i in ast.literal_eval(obj)[:3]]

def fetch_director(obj):
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            return [i['name']]
    return []

# Apply preprocessing
movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)
movies['cast'] = movies['cast'].apply(convert_cast)
movies['crew'] = movies['crew'].apply(fetch_director)
movies['overview'] = movies['overview'].apply(lambda x: x.split())

# Combine all tags
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
new_df = movies[['movie_id', 'title', 'tags']]
new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x).lower())

# Vectorize tags
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(new_df['tags']).toarray()

# Calculate cosine similarity
similarity = cosine_similarity(vectors)

# Function to get all unique genres
def get_all_genres():
    genres = set()
    for g_list in movies['genres']:
        genres.update(g_list)
    return sorted(list(genres))

# Recommend function with optional genre filter
def recommend(movie, selected_genre=None):
    movie = movie.lower()
    if movie not in new_df['title'].str.lower().values:
        return ["Movie not found!"]
    
    index = new_df[new_df['title'].str.lower() == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), key=lambda x: x[1], reverse=True)

    recommendations = []
    for i in distances[1:]:
        title = new_df.iloc[i[0]].title
        original_index = movies[movies['title'] == title].index[0]
        movie_genres = movies.iloc[original_index].genres
        
        if selected_genre:
            if selected_genre in movie_genres:
                recommendations.append(title)
        else:
            recommendations.append(title)
        
        if len(recommendations) == 5:
            break

    return recommendations
