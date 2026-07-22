from flask import Flask, render_template, request, jsonify
import pickle
import os

app = Flask(__name__)

# BASE DIR Fix for Vercel Serverless File Reading
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_pickle(filename):
    filepath = os.path.join(BASE_DIR, 'models', filename)
    if os.path.exists(filepath):
        try:
            with open(filepath, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            return None
    return None

# Safe Models Loading
svd_model = load_pickle('svd_model.pkl')
nmf_model = load_pickle('nmf_model.pkl')
cosine_sim = load_pickle('cosine_similarity.pkl') or load_pickle('cosine_similarity.pk1')
tfidf_vectorizer = load_pickle('tfidf_vectorizer.pkl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id', 'U001')
        algorithm = data.get('algorithm', 'SVD')
        top_k = int(data.get('top_k', 5))

        mock_movies = [
            {"name": "Inception", "score": 98},
            {"name": "Interstellar", "score": 95},
            {"name": "The Dark Knight", "score": 92},
            {"name": "Pulp Fiction", "score": 89},
            {"name": "The Matrix", "score": 86},
            {"name": "Fight Club", "score": 84}
        ]

        results = mock_movies[:top_k]

        return jsonify({
            'status': 'success',
            'algorithm_used': algorithm,
            'data': results
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)