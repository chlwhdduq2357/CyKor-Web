from flask import Blueprint, render_template, request
from flask_sqlalchemy import SQLAlchemy
from app.models import User
from app import db
from werkzeug.utils import redirect

## user management ##
# has functions about user
# 1. function register
# 2. function login
# 3. function logout

blueprint = Blueprint('user', __name__, url_prefix = '/user')

@blueprint.route('/register/', methods = ("GET", "POST"))
def register():
    if request.method == "GET":
        return render_template("/login/register.html")
    else:
        userid = request.form.get("userid")
        username = request.form.get("username")
        password = request.form.get("password")
    
        ## some kind of validation ##
        # print(userid, username, password)
        user = User(userid, username, password)

        db.session.add(user)
        db.session.commit()

    return redirect("/home")
