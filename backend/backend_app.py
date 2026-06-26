from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_posts():
    """Adds a new blog post.

    POST request: expect a JSON object in the body of the request with the
    following structure:
    {
    "title": "<title of the new post>",
    "content": "<content of the new post>"
    }

    Returns:
        return a JSON object with the following structure:
        {
        "id": "<id of the new post>",
        "title": "<title of the new post>",
        "content": "<content of the new post>"
        }
    """
    new_post = request.get_json()
    if not new_post:
        return jsonify({"error": "Missing post"}), 400
    if "title" not in new_post:
        return jsonify({"error": "Missing title"}), 400
    if "content" not in new_post:
        return jsonify({"error": "Missing content"}), 400
    new_post["id"] = max((post["id"] for post in POSTS), default=0) + 1
    POSTS.append(new_post)
    return jsonify(new_post), 201


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
