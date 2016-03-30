from . import main

@main.route('/', methods=['GET'])
def hello():
	return "hello world!"
