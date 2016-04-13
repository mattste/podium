import unittest
import sys
import time

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
			podiums = db.get_podiums()

	def test_get_latest_podium_poll(self):
		with self.app.app_context() as c:
			db = Database()
			db.connection.use('podium')
			# db.populate_with_mock('podium')
			subscriber_number = Database.random_phone_number()
			bernie_sanders_number = "4824814882"
			db.subscribe_to_podium(subscriber_number, bernie_sanders_number)
			response = {
				"subscriber_number": subscriber_number, 
				"option": Database.random_poll_response_option()
			}
			db.respond_to_latest_podium_poll(response=response, podium_number=bernie_sanders_number)

