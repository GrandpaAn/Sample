# -*- coding: utf-8 -*-
from flask import Flask
from werkzeug.routing import BaseConverter
from werkzeug.utils import secure_filename
from os import path
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import *
from flask_sqlalchemy import SQLAlchemy
# from .views import init_views
from flask_login import LoginManager
from flask_pagedown import PageDown
from flask_gravatar import Gravatar

class RegexConverter(object):
	"""docstring for RegexConverter"""
	def __init__(self, url_map, *items):
		super(RegexConverter,self).__init__()
		self.regex=items[0]


basedir = path.abspath(path.dirname(__file__))
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
nav = Nav()
db = SQLAlchemy()

def create_app():
	app = Flask(__name__)
	app.url_map.converters['regex'] = RegexConverter
	app.config.from_pyfile('config')
	app.config['SQLALCHEMY_DATABASE_URI'] =\
		'sqlite:///' + path.join(basedir, 'data.sqlite')
	app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
	# nav.register_element('top', Navbar("Grandpaan's Blog",
	# 								View('Home', 'index'),
	# 								View('About', 'about'),
	# 								View('Serivce', 'serivce'),
	# 								Subgroup('Project',
	# 									View('Project1', 'projects'),
	# 									Separator(),
	# 									View('Project2', 'projects'),)
	# 								))
	db.init_app(app)
	bootstrap.init_app(app)
	login_manager.init_app(app)
	nav.init_app(app)
	Gravatar(app, size=64)
	# init_views(app)

	from auth import auth as auth_blueprint
	from main import main as main_blueprint

	app.register_blueprint(auth_blueprint, url_prefix='/auth')
	app.register_blueprint(main_blueprint, static_folder='static')

	@app.template_test('current_link')
	def is_current_link(link):
		return link == request.path
	return app
