from flask import Flask

### Program starts here ###

# Implemeted Functions
# 1. Register as a new user     (v)
#   - register user id and user name
#   - register password
#   - password is stored encrypted
#   - under user_management.py, function register
#   
# 2. Login and Logout           ( )
#   - login if registered
#   - redirect to register page if not registered
#   - under user_management.py, function login
#   - logout under user_management.py, function logout
#
# 3. Write a post               ( )
#   - write a post only if logged in
#   - not able to write if logged out or not registered
#   - under main_view.py, function post
#
# 4. Read a post                ( )
#   - read a post only if logged in
#   - under main_view.py, function read (?)
#
# sorry for my short English


# using application factory
def create_app():

    app = Flask(__name__)

    
    # using bluprint
    from views import main_views
    from views import user_management
    app.register_blueprint(main_views.blueprint)
    app.register_blueprint(user_management.blueprint)

    return app

if __name__ == "__main__":

    app = create_app()
    app.run()
