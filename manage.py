from app import app

from flask_script import Manager
manager = Manager(app)

from flask_migrate import MigrateCommand
manager.add_command('db', MigrateCommand)

from commands.create_user import CreateUserCommand
manager.add_command('create_user', CreateUserCommand)


if __name__ == '__main__':
	manager.run()