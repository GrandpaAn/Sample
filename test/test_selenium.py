# -*- coding: utf-8 -*-
import unittest
import threading
from selenium import webdriver
from app import create_app, db
from app.models import Role, User
import re 
from forgrey_py import internet

class SeleniumTest(unittest.TestCase):
	client = None
	app_ctx = None
	@classmethod
	def setUpClass(cls):
		try:
			cls.client = webdriver.Firefox()
		except:
			pass

		if cls.client:
			cls.app = create_app('testing')
			cls.app_ctx = cls.app.app_context()
			cls.app_ctx.push()

			db.drop_all()
			db.create_all()
			Role.seed()
			threading.Thread(target=cls.app.run).start()

	@classmethod
	def tearDownClass(cls):
		cls.client.get('http://localhost/shutdown')
		cls.client.close()
		cls.app_ctx.pop()
		
		db.session.remove()

	def setUp(self):
		if self.client is None:
			self.skipTest(u'略过测试')

	def tearDown(self):
		pass

	def test_user_login(self):
		from login_page import LoginPage
		new_user = User(name=internet.user_name(),
						email=internet.email_address(),
						password=basic.text())
		db.session.add(new_user)
		db.session.commit()


		page = LoginPage(self.client)
		self.client.get('http://localhost:5000/auth/login')
		self.assertTrue(u'登录' in self.client.title)

		page.set_user_name(new_user.name)
		page.set_pwd(new_user.password)
		page.submit()

		# user_input = self.client.find_element_by_name('user')
		# user_input.send_keys(new_user.name)
		# # self.client.
		# pwd_input = self.client.find_element_by_name('password')
		# pwd_input.send_keys(new_user.password)

		# submit = self.client.find_element_by_name('submit')
		# submit.click()

		self.assertTrue(re.search(u"Welcome to Grandpaan's Blog", self.client.page_source))