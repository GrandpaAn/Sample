# -*- coding:utf-8 -*-
from flask import render_template, request, redirect, url_for, make_response, abort, flash
from flask_login import login_required, current_user, login_user, logout_user
from . import main
from .. import db
from ..models import Post, Comment
from .forms import CommentForm, PostForm

@main.route('/')
def index():
	# response = make_response(render_template('index.html', title="Welcome to Grandpaan's Blog", body='# Header1'))
	# response.set_cookie('username', '')
	return render_template('index.html', 
							title=u"Welcome to Grandpaan's Blog") #

@main.route('/serivce')
def serivce():
	return 'Serivce'

@main.route('/about')
def about():
	return render_template('about.html')
	#路由
# @main.route('/user/<regex("[a-z]{3}"):user_id>')
# def user(user_id):
# 	return 'User %s' % user_id

@main.route('/admin')
@login_required
def admin():
	return 'Admin'

@main.route('/projects/')
@main.route('/project-page/')
def projects():
	return 'The project page'



@main.route('/upload', methods=['GET','POST'])
def upload():
		if request.method == 'POST':
			f = request.files['file']
			basepath = path.abspath(path.dirname(__file__))
			upload_path = path.join(basepath, 'static/uploads', secure_filename(f.filename))
			f.save(upload_path)
			return redirect(url_for('upload'))
		return render_template('upload.html')

@main.errorhandler(404)
def page_not_found(error):
	return render_template('404.html')

@main.route('/posts/<int:id>', methods=['GET', 'POST'])
def post(id):
	post = Post.query.get_or_404(id)
	# 评论窗体
	form = CommentForm()
	# 保存评论
	if form.validate_on_submit():
		comment = Comment(author = current_user, body = form.body.data, post = post)
		db.session.add(comment)
		db.session.comment()

	return render_template('posts/detail.html',
							title=post.title,
							form=form,
							post=post)

@main.route('/edit')
@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id=0):
	# post = None
	form = PostForm()

	if id == 0:
		post = Post(author=current_user)
	else:
		post = Post.query.get_or_404(id)

	if form.validate_on_submit():
		post.body = form.body.data
		post.title = form.title.data

		db.session.add(post)
		db.session.comment()

	mode = u'添加'
	if id>0:
		mode = u'编辑'
	return render_template('posts/edit.html',
							title=u'title -- %s' % post.title,
							form=form,
							post=post)

	# @app.template_filter('md')
	# def markdown_to_html(txt):
	# 	from markdown import markdown
	# 	return markdown(txt)

	# def read_md(filename):
	# 	with open(filename) as md_file:
	# 		content = reduce(lambda x, y: x + y, md_file.readlines())
	# 		return content.decode('utf-8')

	# @app.context_processor
	# def inject_methods():
	# 	return dict(read_md = read_md)