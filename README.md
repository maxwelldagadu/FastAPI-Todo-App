# TODO APP

This is a Todo List App I built entirely with FastApi to get hands on experience. It's actually my first project I've coded
from start to finish. Just like any other Todo App that helps you create, edit and delete completed tasks, this one pretty much does the same thing. The codebase has more of Backend logic than Frontend, that's beacause I'm more into Backend development.

# APP FEATURES

- Create, edit and delete todos.
- Marks todos as completed.
- Manage todos in real-time using FastAPI’s async capabilities.
- Uses Authentication and Authorization to manage user activities.

# NOTE

For get_me, update_me, change_password, update_phone and delete_me routes, the endpoints are working just fine. I did not include those in the Frontend.

# CLONE REPO

Feel free to clone this repository.

bash
git clone git https://github.com/maxwelldagadu/FastAPI-Todo-App.git

# PIP INSTALL THE REQUIREMENTS.TXT FILE

bash
pip install requirements.txt

# EXPLORE ALL ENDPOINTS

In your terminal run

uvicorn main:app --reload

- Click this link in the terminal http://127.0.0.1:8000
- Add /docs at the end

The complete url to see all routes is http://127.0.0.1:8000/docs

create an account first with the create_user route. Then explore all routes after you are being authenticted and authorized.

# BUGS

Feel free to submit issues or pull requests to enhance the project.
