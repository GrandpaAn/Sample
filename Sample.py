# coding: utf-8
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html', title='Welcome')

@app.route('/serivce')
def serivce():
	return 'Serivce'

@app.route('/about')
def about():
	return 'About'

if __name__ == '__main__':
	app.run(debug=True)