import subprocess, os
basedir = os.path.abspath(os.path.dirname(__file__))


def shell_source(script):
	"""
	Sometime you want to emulate the action of "source" in bash,
	settings some environment variables. Here is a way to do it.
	Referenced from http://stackoverflow.com/a/12708396
	"""
	env_source_cmd = "source %s; env" % os.path.join('envs', script)
	command = ['bash', '-c', env_source_cmd]
	pipe = subprocess.run(command, stdout=subprocess.PIPE)
	output = pipe.stdout
	env = dict((line.decode().split("=", 1) for line in output.splitlines()))
	os.environ.update(env)

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32)
	TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID') or ''
	TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN') or ''

	@staticmethod
	def init_app(app):
		pass

	
class DevelopmentConfig(Config):
	DEBUG = True

	@classmethod
	def init_app(cls, app):
		shell_source('.env-dev')

class TestingConfig(Config):

	@classmethod
	def init_app(cls, app):
		shell_source('.env-testing')


class ProductionConfig(Config):

	@classmethod
	def init_app(cls, app):
		shell_source('.env-production')


config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,

	'default': DevelopmentConfig
}
