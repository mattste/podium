import unittest
import sys

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

	def test_populate_with_mock(self):
		with self.app.app_context() as c:
			db = Database()
			db.populate_with_mock('podium')
	
	def test_get_latest_podium_poll(self):
		with self.app.app_context() as c:
			db = Database()
			db.populate_with_mock('podium')
			latest_poll = db.get_latest_podium_poll('FeelTheBern')
