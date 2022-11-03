from flask import Blueprint, render_template, request, session, url_for

from werkzeug.utils import redirect

import sqlite3 as sql
from . import database_manager as dbm
from . import nohack

## user management ##
# has functions about user
# 1. register
#   - register as a new user
#   - input user id, user name
#   - check if user id or user name already exist
#   - filter out some characters that might cause problems to sql
#   - input password twice and check if they match
#
# 2. login
#   - input user id, user name
#   - validate user id and user name
#   - input password
#   - check password
#   - this html page has a button that is linked to register page
#


blueprint = Blueprint('user', __name__, url_prefix = '/user')

@blueprint.route('/register', methods = ("GET", "POST"))
def register():

    error_msg = ""
    
    userListRaw = dbm.select_all_db("user")
    useridList = [u[0] for u in userListRaw]
    usernameList = [u[1] for u in userListRaw]

    # print("user list : ", userListRaw)
    # print("user id list : ", useridList)
    # print("user name list : ", usernameList)

    
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
        if nohack.filter_string(username) != username or nohack.filter_string(userid) != userid:
            error_msg = "invalid string used"
            return render_template("/login/register.html", error_msg = error_msg)

        # encrypt password
        password = nohack.hash_password(password)
    
        user = (userid, username, password)
        # print(user)
    
        dbm.insert_db("USER", user)

    return redirect(url_for("user.login"))


@blueprint.route('/login',  methods = ("GET", "POST"))
def login():

    userListRaw = dbm.select_all_db("user")
    useridList = [u[0] for u in userListRaw]
    usernameList = [u[1] for u in userListRaw]

    # print("user list : ", userListRaw)
    # print("user id list : ", useridList)
    # print("user name list : ", usernameList)


    error_msg = ""
    if request.method == "GET":
        return render_template("/login/login.html", error_msg = error_msg)
    else:

        userid = request.form.get("userid")
        username = request.form.get("username")
        password = request.form.get("password")

        # check 1 : is user id registered
        if not userid in useridList:
            error_msg = "user id not registered"
            return render_template("/login/login.html", error_msg = error_msg)
        # check 2 : is user name registered
        if not username in usernameList:
            error_msg = "user name not registered"
            return render_template("/login/login.html", error_msg = error_msg)
        # check 3 : does user id match user name
        if useridList.index(userid) != usernameList.index(username):
            error_msg = "user id doesn't match with user name"
            return render_template("/login/login.html", error_msg = error_msg)
        # check 4 : password
        idx = useridList.index(userid)
        password = nohack.hash_password(password)
        if userListRaw[idx][2] != password: 
            error_msg = "wrong password"
            return render_template("/login/login.html", error_msg = error_msg)

        session["username"] = username

    return redirect("/home")
