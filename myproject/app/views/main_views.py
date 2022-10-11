from flask import Blueprint, render_template
from app.models import Post

blueprint = Blueprint('main', __name__, url_prefix = '/')


@blueprint.route('/')
def index():
    post_list = Post.query.order_by(Post._time.desc())
    return render_template("post/post_list.html", post_list = post_list)

@blueprint.route('/detail/<int:post_id>')
def detail():
    post = Post.query.get_or_404(post_id)
    return render_template("post/post_detail.html", post = post)


@blueprint.route('/hello')
def hello_cykor():
    return 'hello, cykor!'
