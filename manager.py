from werkzeug.utils import secure_filename
from flask_script import Manager
from app import create_app, db
from flask_migrate import Migrate, MigrateCommand, upgrade

app = create_app()
manager = Manager(app)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

@manager.command 
def dev():
	from livereload import Server
	live_server = Server(app.wsgi_app)
	live_server.watch('**/*.*')
	live_server.serve(open_url=True)

def test():
	pass

@manager.command
def deploy():
	from app.models import Role
	upgrade()
	Role.seed()

if __name__ == '__main__':
# 	dev()
	# app.run(debug=True)
	manager.run()
	# live_server = Server(app.wsgi_app)
	# live_server.watch('**/*.*')
	# live_server.serve(open_url=True)
