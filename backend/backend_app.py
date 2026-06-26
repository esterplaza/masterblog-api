from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


def find_post_by_id(post_id):
    """searchs for the post with the id: post_id
    Args:
        post_id (int): id of the blog_post
    """
    for post in POSTS:
        if post.get("id") == post_id:
            return post
    return None


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """Displays the posts in json format.

        Returns:
        return a JSON object with the following structure:
        [{
        "id": "<id of post>",
        "title": "<title  post>",
        "content": "<content of post>"
        }, {  ...  other post with same format... }, ...]
    """
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


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Deletes a blog post by its ID.

    Searches in the json object for a post matching the provided ID.
    If found, the post is removed from the list, the updated list is saved.

    Args:
        post_id (int): The identifier of the blog post to delete.

    Returns:
        It the post with the given id exists, the endpoint deletes the post and
        return a JSON object with the following structure:
         {
        "message": "Post with id <id> has been deleted successfully."
        }.
    """
    post = find_post_by_id(post_id)
    if post is None:
        return jsonify({"error": "Post not found"}), 404
    POSTS.remove(post)
    return jsonify({"message": f"Post with id {post_id} has been deleted successfully."})


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """Updates a new blog post.
    PUT request: expect a JSON object in the body of the request with the
    following structure:
    {
    "title": "<title of the new post>",
    "content": "<content of the new post>"
    }

    Returns:
        return a JSON object with the following structure:
        {
        "id": "<id of the updated post>",
        "title": "<new title or old title if not provided>",
        "content": "<new content or old content if not provided>"
        }
    """
    post = find_post_by_id(post_id)
    if post is None:
        return jsonify({"error": "Post not found"}), 404
    new_post = request.get_json()
    post.update(new_post)
    return jsonify(post), 200


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """search for posts by their title or content
    Input to this endpoint will be provided as query parameters in the URL.
    query parameters:
        title: post title to search
        content: post content to search

    Returns:
        A json object with the list of posts that match the search criteria,
         in the same format as the “list” endpoint.
        If no posts match the search criteria, it returns an empty list
    """
    title = request.args.get("title")
    content = request.args.get("content")
    filtered_posts = []
    if title:
        filtered_posts = [post for post in POSTS if title in post.get("title")]
    if content:
        filtered_posts = [post for post in POSTS if content in post.get("content")]
    return jsonify(filtered_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
