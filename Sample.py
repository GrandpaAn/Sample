# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, make_response, abort, flash
from werkzeug.routing import BaseConverter
from werkzeug.utils import secure_filename
from flask_script import Manager
from os import path

from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import *
from flask_sqlalchemy import SQLAlchemy

class RegexConverter(object):
	"""docstring for RegexConverter"""
	def __init__(self, url_map, *items):
		super(RegexConverter,self).__init__()
		self.regex=items[0]


basedir = path.abspath(path.dirname(__file__))
app = Flask(__name__)
app.url_map.converters['regex'] = RegexConverter
Bootstrap(app)
nav = Nav()

app.config.from_pyfile('config')
app.config['SQLALCHEMY_DATABASE_URI'] =\
	'sqlite:///' + path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)

manager = Manager(app)

nav.register_element('top', Navbar("Grandpaan's Blog",
									View('Home', 'index'),
									View('About', 'about'),
									View('Serivce', 'serivce'),
									Subgroup('Project',
										View('Project1', 'projects'),
										Separator(),
										View('Project2', 'projects'),
										)

									))
nav.init_app(app)

@app.route('/')
def index():
	response = make_response(render_template('index.html', title="Welcome to Grandpaan's Home", body='# Header1'))
	response.set_cookie('username', '')
	return response

@app.route('/serivce')
def serivce():
	return 'Serivce'

@app.route('/about')
def about():
	return 'About'
#路由
# @app.route('/user/<regex("[a-z]{3}"):user_id>')
# def user(user_id):
# 	return 'User %s' % user_id

@app.route('/projects/')
@app.route('/project-page/')
def projects():
	return 'The project page'

@app.route('/login', methods=['GET', 'POST'])
def login():
	from forms import LoginForm
	form = LoginForm()
	flash(u'登录成功')
	return render_template('login.html',title=u'用户登录', form=form) # method=request.method
	# if request.method == 'POST':
	# 	username = request.form['username']
	# 	password = request.form['password']
	# else:
	# 	username = request.args['username']

@app.route('/upload', methods=['GET','POST'])
def upload():
		if request.method == 'POST':
			f = request.files['file']
			basepath = path.abspath(path.dirname(__file__))
			upload_path = path.join(basepath, 'static/uploads', secure_filename(f.filename))
			f.save(upload_path)
			return redirect(url_for('upload'))
		return render_template('upload.html')

@app.errorhandler(404)
def page_not_found(error):
	return render_template('404.html')

@app.template_test('current_link')
def is_current_link(link):
	return link == request.path

@manager.command 
def dev():
	from livereload import Server
	live_server = Server(app.wsgi_app)
	live_server.watch('**/*.*')
	live_server.serve(open_url=True)

@app.template_filter('md')
def markdown_to_html(txt):
	from markdown import markdown
	return markdown(txt)

def read_md(filename):
	with open(filename) as md_file:
		content = reduce(lambda x, y: x + y, md_file.readlines())
		return content.decode('utf-8')

@app.context_processor
def inject_methods():
	return dict(read_md = read_md)

class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primany_key=True)
	name = db.Column(db.String, nullable=True)
	users = db.relationship('User', bachref='roles')

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primany_key=True)
	name = db.Column(db.String, nullable=True)
	password = db.Column(db.String, nullable=True)
	role_id = db.Column(db.Integer, db.Foreignkey('roles.id'))

if __name__ == '__main__':
	# app.run(debug=True)
	# manager.run()
	dev()
	# live_server = Server(app.wsgi_app)
	# live_server.watch('**/*.*')
	# live_server.serve(open_url=True)
