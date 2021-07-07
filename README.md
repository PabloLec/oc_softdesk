# oc_softdesk

:books: Made for an [OpenClassrooms](https://openclassrooms.com) studies project.  
`oc_softdesk` is a back-end Django REST API for a project management platform.

# Features

`oc_softdesk` uses a SQLite DB to store users and their created content.

A user can create a project to which he can add contributors whom will create related issues and comments.

A registered user can only access to projects of which he is a contributor. Hence, the project creator has to decide so. In the same way, a user can only edit and delete content (project, issue or comment) of which he is the creator.

# Documentation

See full Postman documentation:  
https://documenter.getpostman.com/view/16341824/Tzm2Ldwb

# Setup

- First clone this repository and navigate to downloaded folder:
  ``` bash
  git clone https://github.com/PabloLec/oc_softdesk.git
  cd oc_softdesk
  ```

- Then, start a virtual environment:
  ``` bash
  python3 -m venv env
  source env/bin/activate
  ```

- Before running, install the project requirements with:
  ``` bash
  python3 -m pip install -r requirements.txt
  ```

- Finally, you can navigate to Django project directory and run the server:
  ``` bash
  cd oc_softdesk
  python3 -m manage runserver
  ```

- Website should be served at `127.0.0.1:8000`.

# Usage

- First, create a superuser with:
  ``` bash
  python3 -m manage createsuperuser
  ```
- You can then manage your database on `127.0.0.1:8000/admin`  

- Create your first user with `127.0.0.1:8000/signup` endpoint.
- To access the platform, send your credentials to `http://127.0.0.1:8000/login` endpoint. The token you should receive will be your access token.
