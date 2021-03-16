from models import AdminUserModel
from flask_script import Command, Option


class CreateUserCommand(Command):
	option_list = (
		Option('--username', '-u', dest='_username'),
		Option('--password', '-p', dest='_password')
	)

	def run(self, _username, _password):
		user = AdminUserModel()
		user.username = _username
		user.set_password(_password)
		user.save_to_db()
		