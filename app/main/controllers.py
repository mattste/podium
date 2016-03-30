from . import main
from ..db.database import *

@main.route('/', methods=['GET'])
def hello():
	query_test_db()
	return "hello world!"
