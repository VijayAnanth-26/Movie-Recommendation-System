import pandas as pd
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load datasets
movies = pd.read_csv('dataset/tmdb_5000_movies.csv')
credits = pd.read_csv('dataset/tmdb_5000_credits.csv')
credits.columns = ['id', 'title', 'cast', 'crew']
movies = movies.merge(credits, on='title')
movies.rename(columns={'id_x': 'movie_id'}, inplace=True)
movies.columns = movies.columns.str.strip()

# Select necessary columns
movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]

# Helper functions
def convert(obj):
    return [i['name'] for i in ast.literal_eval(obj)]

def convert_cast(obj):
    return [i['name'] for i in ast.literal_eval(obj)[:3]]

def fetch_director(obj):
    return [i['name'] for i in ast.literal_eval(obj) if i['job'] == 'Director']

# Preprocessing
movies.dropna(inplace=True)
movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)
movies['cast'] = movies['cast'].apply(convert_cast)
movies['crew'] = movies['crew'].apply(fetch_director)
movies['overview'] = movies['overview'].apply(lambda x: x.split())
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

new_df = movies[['movie_id', 'title', 'tags', 'genres']]
new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x)).str.lower()

# Vectorization
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(new_df['tags']).toarray()
similarity = cosine_similarity(vectors)

# --- Recommend function ---
def recommend(movie, selected_genre=None):
    movie = movie.lower()
    if movie not in new_df['title'].str.lower().values:
        return ["Movie not found!"]

    index = new_df[new_df['title'].str.lower() == movie].index[0]
    distances = list(enumerate(similarity[index]))
    distances = sorted(distances, key=lambda x: x[1], reverse=True)

    recommendations = []
    for i in distances[1:]:
        title = new_df.iloc[i[0]].title
        genres = new_df.iloc[i[0]].genres
        if selected_genre is None or selected_genre in genres:
            recommendations.append(title)
        if len(recommendations) == 5:
            break
    return recommendations

# --- Get unique genres for dropdown ---
def get_all_genres():
    genre_set = set()
    for g_list in new_df['genres']:
        genre_set.update(g_list)
    return sorted(genre_set)
