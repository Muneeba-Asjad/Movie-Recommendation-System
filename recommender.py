import pickle
import os

# Models Folder
MODEL_PATH = "models"

# Load Models
with open(os.path.join(MODEL_PATH, "svd_model.pkl"), "rb") as f:
    svd_model = pickle.load(f)

with open(os.path.join(MODEL_PATH, "movies.pkl"), "rb") as f:
    movies = pickle.load(f)

with open(os.path.join(MODEL_PATH, "movie_id_to_title.pkl"), "rb") as f:
    movie_id_to_title = pickle.load(f)

with open(os.path.join(MODEL_PATH, "title_to_movie_id.pkl"), "rb") as f:
    title_to_movie_id = pickle.load(f)

with open(os.path.join(MODEL_PATH, "tfidf.pkl"), "rb") as f:
    tfidf = pickle.load(f)

with open(os.path.join(MODEL_PATH, "cosine_similarity.pkl"), "rb") as f:
    cosine_sim = pickle.load(f)


# -------------------------------
# Collaborative Recommendation
# -------------------------------
def collaborative_recommend(user_id, top_n=10):

    all_items = movies["item_id"].unique()

    watched = []

    recommendations = []

    for item in all_items:

        if item not in watched:

            pred = svd_model.predict(user_id, item)

            recommendations.append((item, pred.est))

    recommendations.sort(key=lambda x: x[1], reverse=True)

    output = []

    for item_id, score in recommendations[:top_n]:

        movie = movie_id_to_title.get(item_id, "Unknown Movie")

        output.append({
            "movie": movie,
            "score": round(score, 2)
        })

    return output


# -------------------------------
# Content Based Recommendation
# -------------------------------
def content_recommend(movie_name, top_n=10):

    if movie_name not in movies["movie_title"].values:
        return []

    indices = dict(zip(movies["movie_title"], movies.index))

    idx = indices[movie_name]

    similarity = list(enumerate(cosine_sim[idx]))

    similarity = sorted(similarity, key=lambda x: x[1], reverse=True)

    similarity = similarity[1:top_n + 1]

    result = []

    for i, score in similarity:

        result.append({
            "movie": movies.iloc[i]["movie_title"],
            "score": round(float(score), 2)
        })

    return result


# -------------------------------
# Hybrid Recommendation
# -------------------------------
def hybrid_recommend(user_id, movie_name, top_n=10):

    collab = collaborative_recommend(user_id, top_n=50)

    if movie_name not in movies["movie_title"].values:
        return collab[:top_n]

    indices = dict(zip(movies["movie_title"], movies.index))

    idx = indices[movie_name]

    final = []

    for item in collab:

        title = item["movie"]

        if title not in indices:
            continue

        idx2 = indices[title]

        content_score = cosine_sim[idx][idx2]

        score = (0.7 * item["score"]) + (0.3 * content_score)

        final.append({
            "movie": title,
            "score": round(float(score), 2)
        })

    final.sort(key=lambda x: x["score"], reverse=True)

    return final[:top_n]