from flask import Blueprint, render_template, request

from werkzeug.utils import redirect

import sqlite3 as sql
from . import database_manager as dbm
from . import nohack

## user management ##
# has functions about user
# 1. function register
# 2. function login
# 3. function logout

blueprint = Blueprint('user', __name__, url_prefix = '/user')

@blueprint.route('/register/', methods = ("GET", "POST"))
def register():

    error_msg = ""
    
    userListRaw = dbm.select_all_db("user")
    useridList = [u[0] for u in userListRaw]
    usernameList = [u[1] for u in userListRaw]

    print("user list : ", userListRaw)
    print("user id list : ", useridList)
    print("user name list : ", usernameList)

    
    if request.method == "GET":
        return render_template("/login/register.html", error_msg = error_msg)
    else:
        userid = request.form.get("userid")
        username = request.form.get("username")
        password = request.form.get("password")
        password2 = request.form.get("password2")

        if not (userid and username and password and password2):
            return render_template("/login/register.html", error_msg = "please input values")
    
        # check 1 : is user id unique
        if userid in useridList:
            error_msg = f"user id '{userid}' already exists"
            return render_template("/login/register.html", error_msg = error_msg)
        
        # check 2 : is user name unique
        if username in usernameList:
            error_msg = f"user name '{username}' already exists"
            return render_template("/login/register.html", error_msg = error_msg)

        # check 3 : password 1 is same as password 2
        if password != password2:
            error_msg = "please check password again"
            return render_template("/login/register.html", error_msg = error_msg)

        # check 4 : no hack!
        if nohack.filter(username) != username or nohack.filter(userid) != userid:
            error_msg = "invalid string used"
            return render_template("/login/register.html", error_msg = error_msg)

        # encrypt password
        password = nohack.hash_password(password)
    
        user = (userid, username, password)
        print(user)
    
        dbm.insert_db("USER", user)

    return redirect("/home")
