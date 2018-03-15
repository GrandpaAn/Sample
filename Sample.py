# coding: utf-8
from flask import flask

app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello world'

if __name__ == '__main__':
	app.run()