# coding: utf-8
from flask import Flask, render_template, request, redirect, url_for, make_response, abort
from werkzeug.routing import BaseConverter
from werkzeug.utils import secure_filename
from os import path


class RegexConverter(object):
	"""docstring for RegexConverter"""
	def __init__(self, url_map, *items):
		super(RegexConverter,self).__init__()
		self.regex=items[0]

app = Flask(__name__)
app.url_map.converters['regex'] = RegexConverter

@app.route('/')
def index():
	response = make_response(render_template('index.html', title='Welcome'))
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
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
	else:
		username = request.args['username']
	return render_template('login.html', method=request.method)

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
 
if __name__ == '__main__':
	app.run(debug=True)