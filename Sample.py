# coding: utf-8
from flask import Flask, render_template, request
from werkzeug.routing import BaseConverter

class RegexConverter(object):
	"""docstring for RegexConverter"""
	def __init__(self, url_map, *items):
		super(RegexConverter,self).__init__()
		self.regex=items[0]

app = Flask(__name__)
app.url_map.converters['regex'] = RegexConverter

@app.route('/')
def index():
	return render_template('index.html', title='Welcome')

@app.route('/serivce')
def serivce():
	return 'Serivce'

@app.route('/about')
def about():
	return 'About'
#路由
# @app.route('/user/<regex("[a-z]{3}"):user_id>')
# def user(user_id):
# 	return 'User ID %s' % user_id

@app.route('/projects/')
@app.route('/project-page/')
def projects():
	return 'The project page'

@app.route('/login', methods=['GET', 'POST'])
def login():
	return render_template('login.html', method=request.method)

if __name__ == '__main__':
	app.run(debug=True)