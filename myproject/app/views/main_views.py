from flask import Blueprint, render_template, url_for, request, session
from werkzeug.utils import redirect

from datetime import datetime
from . import database_manager as dbm
from . import nohack

## main view ##
# has functions about post and general
# 1. home
# 2. post
# 3. index
# 4. detail
# 5. edit


blueprint = Blueprint('main', __name__, url_prefix = '/')


@blueprint.route('/')
def default():

    return redirect(url_for('main.home'))



@blueprint.route('/post_list')
def index():
    
    # view list of posts
    # show title, author (user name), time
    # title is linked to corresponding post
    
    postListRaw = dbm.select_all_db("post")
    post_list = [(p[1][0], p[1][1], p[1][2][:19], p[0]) for p in enumerate(postListRaw)]
    return render_template("post/post_list.html", post_list = post_list)


@blueprint.route('/detail')
def detail_default():
    return redirect(url_for("index"))

@blueprint.route('/detail/<int:post_id>/')
def detail(post_id):

    # can see content only if logged in
    
    if "username" in session:
        postRaw = dbm.select_all_db("post")[post_id]
    else:
        postRaw = "please log in first"
    return render_template("post/post_detail.html", post = postRaw)
    
@blueprint.route('/post', methods = ["GET", "POST"])
def post():

    # post a new post
    # input title and content
    # only able when logged in
    
    error_msg = ""
    if not "username" in session:
        error_msg = "please log in first"
        return render_template("/post/post.html", error_msg = error_msg)
    else:
        if request.method == "POST":

            postList = dbm.select_all_db("POST")
            
            username = session["username"]
            title = request.form.get("title")
            content = request.form.get("content")

            title = nohack.replace_string(title)
            content = nohack.replace_string(content)
                        
            time = str(datetime.now())
            post = (username, title, time, content)
            dbm.insert_db("POST", post)
            
            return redirect(f"/detail/{len(postList)}/")
        else:
            return render_template("/post/post.html", error_msg = error_msg)
            


@blueprint.route('/home')
def home():

    # home page
    # show "Hello, {username}" if logged in
    
    username = ""
    if "username" in session:
        username = session["username"]
    return render_template("/home/home.html", username = username)
