import os

from flask.ext.script import Manager

from app import create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)

@manager.command
def test(coverage=False):
	"""Run the unit tests."""
	raise NotImplemented


@manager.command
def profile(length=25, profile_dir=None):
	"""Start the application under the code profiler."""
	raise NotImplemented


@manager.command
def deploy():
	"""Run deployment tasks."""
	raise NotImplemented


if __name__ == '__main__':
	manager.run()
