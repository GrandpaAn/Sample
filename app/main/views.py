# -*- coding:utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, make_response, abort, flash, current_app#, send_static_file
from flask_login import login_required, current_user, login_user, logout_user
from . import main
from .. import db
from ..models import Post, Comment
from .forms import CommentForm, PostForm
from flask_babel import gettext as _

@main.route('/')
def index():
	# response = make_response(render_template('index.html', title="Welcome to Grandpaan's Blog", body='# Header1'))
	# response.set_cookie('username', '')
	# posts = Post.query.all()
	# print posts
	page_index = request.args.get('page', 1, type=int)

	query = Post.query.order_by(Post.created.desc())

	pagination = query.paginate(page_index, per_page=20, error_out=False)

	posts = pagination.items	
	return render_template('index.html', 
							title=u"Welcome to Grandpaan's Blog",
							posts=posts,
							pagination=pagination)

@main.route('/serivce')
def serivce():
	return render_template('service.html',
							title="Serivce")

@main.route('/about')
def about():
	return render_template('about.html',
							title="About me")
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
			upload_path = path.join(basepath, 'static\uploads', secure_filename(f.filename))
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
		db.session.commit()

	return render_template('posts/detail.html',
							title=post.title,
							form=form,
							post=post)

@main.route('/edit', methods=['GET', 'POST'])
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
		db.session.commit()
		return redirect(url_for('.post', id=post.id))

	form.title.data = post.title
	form.body.data = post.body

	title = _(u'添加新文章')
	if id > 0:
		title = _(u'编辑 - %(title)', title=post.title)

	return render_template('posts/edit.html',
							title=title,
							form=form,
							post=post)

# @main.route('/shutdown')
# def shutdown():
# 	if not current_app.testing:
# 		abort(404)

# 	shutdown = request.environ.get('werkzeug,server.shutdown')
# 	if not shutdown:
# 		abort(500)

# 	shutdown()
# 	return u'正在关闭服务器端进程......'
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