from flask import Blueprint, render_template, url_for, request, session
from werkzeug.utils import redirect

from datetime import datetime
from . import database_manager as dbm
from . import nohack

### main view ###
# has functions about post and general
# 1. home
#   - show "Hello, {username}" string if logged in
#
# 2. post
#   - upload a new post to db
#   - only able when logged in
#   - input title and content
#   - filter out some strings before uploading
#   - redirect to its detailed content if uploaded successfully
#
# 3. index
#   - browse posts from db
#   - show title, author(username) and time created
#   - list is opened to users who are not logged in
#   - each titles are linked to its detailed content
#
# 4. detail
#   - show detailed content of the post
#   - show title, author(username), time created and content
#   - only able to access this page when logged in
#
# 5. edit
#
# 6. delete

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
    post_list = [[p[1][0], p[1][1], p[1][2][:19], p[0]] for p in enumerate(postListRaw)]
    for i, post in enumerate(post_list):
        if len(post[1]) > 60:
            post_list[i][1] = post_list[i][1][:60] + "..."
            
    return render_template("post/post_list.html", post_list = post_list)


@blueprint.route('/detail/')
def detail_default():
    return redirect(url_for("main.index"))

@blueprint.route('/detail/<int:post_id>/')
def detail(post_id):

    # can see content only if logged in

    isAuthor = False
    
    if "username" in session:
        postRaw = list(dbm.select_all_db("post")[post_id])
        postRaw[-1] = postRaw[-1].split("\n")

        if session["username"] == postRaw[0]:
            isAuthor = True
            # print("can edit")
        
    else:
        postRaw = "please log in first"
        
    return render_template("post/post_detail.html", post = postRaw, post_id = post_id,isAuthor = isAuthor)
    

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

            usernames = [x[0] for x in dbm.select_all_db("user")]
            if not session["username"] in usernames:
                return redirect(url_for("main.index"))
            
            postList = dbm.select_all_db("POST")
            
            username = session["username"]
            title = request.form.get("title")
            content = request.form.get("content")

            title = nohack.replace_string(title)        #filter
            content = nohack.replace_string(content)    #filter
            
            time = str(datetime.now())
            post = (username, title, time, content)
            dbm.insert_db("POST", post)

            
            return redirect(f"/detail/{len(postList)}/")
        else:
            return render_template("/post/post.html", error_msg = error_msg)



@blueprint.route('/edit/')
def edit_default():
    return redirect(url_for("main.index"))

@blueprint.route('/edit/<int:post_id>/', methods = ["GET", "POST"])
def edit(post_id):

    postRaw = list(dbm.select_all_db("post")[post_id])
    postUser = postRaw[0]
    postTitle = postRaw[1]
    postContent = postRaw[3]
    postTime = postRaw[2]
    usernames = [x[0] for x in dbm.select_all_db("user")]

    if "username" in session:
        if session["username"] in usernames and session["username"] == postUser:
            
            if request.method == "GET":
                return render_template("/post/edit.html", title = postTitle, content = postContent)

            else:
                newtitle = request.form.get("title")
                newcontent = request.form.get("content")

                # print(newtitle, newcontent)
                
                newtitle = nohack.replace_string(newtitle)
                newcontent = nohack.replace_string(newcontent)

                time = str(datetime.now())
                newpost = (newtitle, time, newcontent, session["username"], postTime)
                # print(newpost)
                dbm.update_post_db(newpost)

                return redirect(f"/detail/{post_id}/")
            
        else:
            return redirect(url_for("main.index"))
    else:
        return redirect(url_for("main.index"))


@blueprint.route('/delete/')
def delete_default():
    return redirect(url_for("main.index"))

    
@blueprint.route('/delete/<int:post_id>')
def delete_post(post_id):

    postRaw = list(dbm.select_all_db("post")[post_id])
    postValue = (session["username"], postRaw[2])

    if postValue[0] == session["username"]:
        dbm.delete_post_db(postValue)

    return redirect(url_for("main.index"))


@blueprint.route('/home')
def home():

    # home page
    # show "Hello, {username}" if logged in
    
    username = ""
    if "username" in session:
        username = session["username"]
    return render_template("/home/home.html", username = username)
