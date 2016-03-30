import unittest

from app import create_app
from app.db.database import Database

class DatabaseTestCase(unittest.TestCase):

	def setUp(self):
		self.app = create_app('testing')
		
	def test_init_db(self):
		with self.app.app_context() as c:
			db = Database()
			db.init_db('testing1')
			db.drop_db('testing1')

	
