from flask import Blueprint, render_template, url_for
from app.models import Post
from werkzeug.utils import redirect

from datetime import datetime
from app import db

## main view ##
# has functions about post and general
# 1. home
# 2. post
# 3. 


blueprint = Blueprint('main', __name__, url_prefix = '/')


@blueprint.route('/')
def default():
    return redirect(url_for('user.register'))


@blueprint.route('/posts')
def index():
    post_list = Post.query.order_by(Post._time.desc())
    return render_template("post/post_list.html", post_list = post_list)

@blueprint.route('/detail/<int:post_id>/')
def detail(post_id):
    post = Post.query.get_or_404({"_id" : post_id})
    return render_template("post/post_detail.html", post = post)


@blueprint.route('/hello')
def hello_cykor():
    return 'hello, cykor!'


@blueprint.route('/home', methods = ["GET", "POST"])
def home():
    return render_template("/home/home.html")
