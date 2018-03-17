# -*- coding:utf-8 -*-
from flask import render_template, request, redirect, url_for, flash
from . import auth

@auth.route('/login', methods=['GET', 'POST'])
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

@auth.route('/logout')
def logout():
	if current_user.is_authenticated():
		logout_user()
	return redirect('login')

@auth.route('/register', methods=['GET', 'POST'])
def register():
	return render_template('register.html', title=u'用户注册')