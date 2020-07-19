from blog_app.models import BlogPost
from flask import render_template, request,Blueprint


main = Blueprint('main',__name__)

@main.route('/')
def hello():
    posts = BlogPost.query.order_by(BlogPost.date_posted.desc()).limit(3)
    return render_template('index.html',posts=posts)

@main.route('/posts', methods=['GET', 'POST'])
def posts():
    page = request.args.get('page',1, type=int)
    all_posts = BlogPost.query.order_by(BlogPost.date_posted.desc()).paginate(page=page,per_page=5)
    return render_template('posts.html', posts=all_posts)