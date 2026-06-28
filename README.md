# **Masterblog api**

---

Api application for a Blog built with Python using Flask.

## **Description**

___

This project was developed as a practice assessment for a Software Engineering Bootcamp in Masterschool.
It demonstrates:

- Flask concepts such as:
  - routing
  - basic CRUD (Create, Read, Update, Delete) operations

- FrontEnd application was provided by Masterschool.

## **Overview**

Masterblog-api provides the structure of an API with different endpoints that
perform the operations.
The posts' information of the blog is stored in variable.

## **Features**

___

- List all posts
- Sort posts by title or content (through query parameters)
- Create new posts
- Delete posts
- Update posts
- search posts by title or content (through query parameters)

## Technologies Used

___

| Technology       | Purpose                              |
|:-----------------|:-------------------------------------|
| Python           | Core application                     |
| Flask            | Web framework                        |
| flask_cors       | andles Cross-Origin Resource Sharing |
| Json             | Json data process support            |
| HTML             | Generated blog website               |
| CSS              | Style content of webpage             |
| JavaScript       | Dynamically generation of HTML       |
| flask_swagger_ui | API documentation                    |


## **Installation**

___

1. Clone the repository:

```
git clone https://github.com/esterplaza/masterblog-api.git
```


5. Change git remote url to avoid accidental pushes to base project

```
   git remote set-url origin github_username/repo_name
   git remote -v # confirm the changes
```

### Required Packages

```
pip install flask
pip install flask_cors
pip install flask_swagger_ui
```


## **Running the Application**

___

Start the program:

```
python backend/backend_app.py
python frontend/frontend_app.py
```

## **Data Structure**

___

The data structure looks like this:

[
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]

## **Usage**

___


## Acknowledgments

___

- Built using Flask.

## **Contact**

___

Ester Plaza Fernández - esterplaza@gmail.com

Project Link: https://github.com/esterplaza/masterblog-api.git

