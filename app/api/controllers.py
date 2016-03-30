from . import api

@api.route('/', methods=['GET'])
def hello_api():
	return "hello world api!"
