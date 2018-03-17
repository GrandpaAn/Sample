# -*- coding:utf-8 -*-
from flask import render_template, request, redirect, url_for, flash
from . import auth
from .forms import LoginForm, RegistrationForm
from ..models import User
from .. import db
from flask_login import login_user, logout_user, current_user

@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(name = form.username.data, password = form.password.data).first()
		if user is not None:
			login_user(user)
			return redirect(url_for('main.index'))

	# flash(u'登录成功')
	return render_template('login.html',title=u'用户登录', form=form) # method=request.method

@auth.route('/logout')
def logout():
	if current_user.is_authenticated():
		logout_user()
	return redirect('login')

@auth.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()

	if form.validate_on_submit():
		user = User(email=form.email.data,
					name=form.username.data,
					password=form.password.data)

		db.session.add(user)
		db.session.submit()
		return redirect(url_for('auth.login'))

	return render_template('register.html',
							title=u'用户注册',
							form=form)