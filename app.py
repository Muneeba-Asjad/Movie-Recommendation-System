import streamlit as st
import pickle
import os

# Page Config
st.set_page_config(page_title="Movie Recommendation System", page_icon="🎬", layout="wide")

st.title("🎬 Movie Recommendation System")
st.write("Find your next favorite movie using AI!")

# Safe Model Loading Function
@st.cache_resource
def load_model(filename):
    filepath = os.path.join(os.path.dirname(__file__), 'models', filename)
    if os.path.exists(filepath):
        try:
            with open(filepath, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            st.warning(f"Could not load {filename}: {e}")
            return None
    return None

# Load Models
svd_model = load_model('svd_model.pkl')
nmf_model = load_model('nmf_model.pkl')

# Sidebar Controls
st.sidebar.header("User Settings")
user_id = st.sidebar.text_input("User ID", value="U001")
algorithm = st.sidebar.selectbox("Select Algorithm", ["SVD", "NMF", "Cosine Similarity"])
top_k = st.sidebar.slider("Number of Recommendations", min_value=1, max_value=10, value=5)

if st.sidebar.button("Get Recommendations", type="primary"):
    st.subheader(f"Top {top_k} Recommendations ({algorithm}) for User: {user_id}")
    
    # Mock / Sample Recommendations (Replace with your model prediction logic)
    mock_movies = [
        {"name": "Inception", "genre": "Sci-Fi", "rating": "9.8/10"},
        {"name": "Interstellar", "genre": "Sci-Fi", "rating": "9.5/10"},
        {"name": "The Dark Knight", "genre": "Action", "rating": "9.2/10"},
        {"name": "Pulp Fiction", "genre": "Crime", "rating": "8.9/10"},
        {"name": "The Matrix", "genre": "Sci-Fi", "rating": "8.6/10"},
        {"name": "Fight Club", "genre": "Drama", "rating": "8.4/10"}
    ]
    
    results = mock_movies[:top_k]
    
    cols = st.columns(len(results))
    for idx, movie in enumerate(results):
        with cols[idx % 3]:
            st.info(f"**{movie['name']}**\n\nGenre: {movie['genre']}\n\nRating: {movie['rating']}")