from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)

# Load ML model files
movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/recommend", methods=["GET"])
def recommend():

    movie = request.args.get("movie", "").strip()

    if not movie:
        return jsonify({
            "error": "Please enter a movie name."
        }), 400

    # Convert titles to lowercase
    titles = movies["title"].astype(str).str.lower()

    # Exact match
    matching = titles[titles == movie.lower()]

    if matching.empty:
        return jsonify({
            "error": "Movie not found. Try another movie from the dataset."
        }), 404

    # Original movie index
    index = matching.index[0]

    # Similarity scores
    distances = similarity[index]

    # Sort recommendations
    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommendations = []

    for movie_index, score in movie_list:

        title = movies.iloc[movie_index]["title"]

        recommendations.append({
            "title": title,
            "score": round(float(score) * 100, 1)
        })

    return jsonify({
        "movie": movies.iloc[index]["title"],
        "recommendations": recommendations
    })


if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )