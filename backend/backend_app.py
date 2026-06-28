from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


SWAGGER_URL = "/api/docs"  # (1) swagger endpoint e.g. HTTP://localhost:5002/api/docs
API_URL = "/static/masterblog.json"  # (2) ensure you create this dir and file

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Masterblog API'  # (3) You can change this if you like
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


def find_post_by_id(post_id):
    """searchs for the post with the id: post_id
    Args:
        post_id (int): id of the blog_post
    """
    for post in POSTS:
        if post.get("id") == post_id:
            return post
    return None


def sort_function(sort_type, sort_direction):
    """sorts the POSTS list according to the arguments sort_type and
    sort_direction.
    Args:
        sort_type (str): key of the dictionary to be sorted
        sort_direction (str): direction of the sorting (ascending or descending)
    """
    if sort_direction == "desc":
        sorted_posts = sorted(POSTS, key=lambda k: k[sort_type].lower(), reverse=True)
    else:
        sorted_posts = sorted(POSTS, key=lambda k: k[sort_type].lower())
    return sorted_posts


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """Displays the posts in json format.

    Parameters (optional):
        sort: specifies the field by which posts should be sorted.
            It should accept the values title or content
        direction: Specifies the sort order.
            It should accept asc for ascending order
            and desc for descending order.

    Returns:
    return a JSON object with the following structure:
        [{
        "id": "<id of post>",
        "title": "<title  post>",
        "content": "<content of post>"
        }, {  ...  other post with same format... }, ...]
    If the optional parameters are used, the returned JSON object will be sorted
    according these parameters.
    """
    valid_sort_values = ["title", "content"]
    valid_direction_values = ["asc", "desc"]
    sort = request.args.get("sort")
    direction = request.args.get("direction")
    if not sort and not direction:
        return jsonify(POSTS)
    if sort not in valid_sort_values or direction not in valid_direction_values:
        return jsonify({"error": "Bad request"}), 400
    sorted_posts = sort_function(sort, direction)
    return jsonify(sorted_posts)


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
    query_parameters = {}
    if title:
        query_parameters["title"] = title.lower()
    if content:
        query_parameters["content"] = content.lower()
    filtered_posts = []
    for post in POSTS:
        matches = True
        for key, value in query_parameters.items():
            if not matches:
                break
            if post.get(key):
                post_item = post.get(key)
                post_item_low = post_item.lower()
                if value not in post_item_low:
                    matches = False
            else:
                matches = False
        if matches:
            filtered_posts.append(post)
    return jsonify(filtered_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
