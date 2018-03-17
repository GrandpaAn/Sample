# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(Form):
	# """docstring for LoginForm"""
	# def __init__(self, arg):
	# 	super(LoginForm, self).__init__()
	# 	self.arg = arg
	username = StringField(label=u'用户名/邮箱', validators=[DataRequired()])
	password = PasswordField(label=u'密码', validators=[DataRequired()])
	submit = SubmitField(label='Login')
