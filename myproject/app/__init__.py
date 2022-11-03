from flask import Flask
import os

### Program starts here ###

# Implemeted Functions
# 1. Register as a new user     (v)
#   - register user id and user name
#   - register password
#   - password is stored encrypted
#   - under user_management.py, function register
#   
# 2. Login                      (v)
#   - login if registered
#   - redirect to register page if not registered
#   - under user_management.py, function login
#
# 3. Write a post               (v)
#   - write a post only if logged in
#   - not able to write if logged out or not registered
#   - under main_view.py, function post
#
# 4. Read a post                (v)
#   - read a post only if logged in
#   - under main_view.py, function detail
# 
# 5. Edit a post                (v)
#   - edit a post only if logged in
#   - you have to be the writer of the post to edit
#   - or you are a admin
#   - under main_view.py, function edit
#
# 6. View a list of posts       (v)
#   - view a list of posts' title and author
#   - doesn't matter if you are logged in or not
#   - each titles are linked to corresponding post
#   - but you have to log in to read the post
#   - under main_view.py, function index
#
# 7. Delete a post              (v)
#   - delete a post only if logged in
#   - you can delete a post only if you are the author

# sorry for my short English


# using application factory
def create_app():

    app = Flask(__name__)
    # using key in order to use session
    app.secret_key = os.urandom(24)
    
    # using bluprint
    from views import main_views
    from views import user_management
    app.register_blueprint(main_views.blueprint)
    app.register_blueprint(user_management.blueprint)

    return app

if __name__ == "__main__":

    app = create_app()
    app.run()
