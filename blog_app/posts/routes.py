from flask import Blueprint
from flask import render_template, redirect,request,flash,url_for,abort
from blog_app.models import BlogPost
from blog_app import db
from blog_app.posts.forms import PostForm
from flask_login import current_user,login_required

posts = Blueprint('posts',__name__)

@posts.route('/posts/delete/<int:id>', methods=['GET','POST'])
@login_required
def delete(id):
   post = BlogPost.query.get_or_404(id)
   if post.author != current_user:
       abort(403)
   db.session.delete(post)
   db.session.commit()
   flash('Your post deleted','danger')
   return redirect('/posts')


@posts.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = BlogPost.query.get_or_404(id)
    form = PostForm()
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!','success')
        return redirect(url_for('posts.read_more', id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html',  form=form, legend='Update Post')

@posts.route('/posts/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = BlogPost(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created','success')
        return redirect(url_for('main.posts'))
    return render_template('create_post.html',  form=form,  legend='New Post')


@posts.route('/posts/read_more/<int:id>')
def read_more(id):
    post = BlogPost.query.get_or_404(id)
    return render_template('read_more.html',post=post)
