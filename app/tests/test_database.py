import unittest
import sys
import time

from app import create_app
from app.db.database import Database

class DatabaseTestCase(unittest.TestCase):

	taylor_phone_number = "3982482000"
	bernie_sanders_number = "+12673544273"
	betty_podium_number = "+12014823312"

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

	def mock_response(self, subscriber_number):
		response = {
			"subscriber_number": subscriber_number, 
			"option": Database.random_poll_response_option()
		}
		return response

	def test_get_latest_podium_poll(self):
		with self.app.app_context() as c:
			db = Database()
			db.connection.use('podium')
			# db.populate_with_mock('podium')
			subscriber_number = Database.random_phone_number()
			db.subscribe_to_podium(subscriber_number, self.taylor_phone_number)
			db.subscriber_number(subscriber_number, self.bernie_sanders_number)
			
			db.respond_to_latest_podium_poll(response=self.mock_response(subscriber_number), podium_number=self.bernie_sanders_number)
			db.respond_to_latest_podium_poll(response=self.mock_response(subscriber_number), podium_number=self.taylor_phone_number)

	def test_phone_number_is_subscribed_to_podium(self):
		with self.app.app_context() as c:
			db = Database()
			db.connection.use('podium')

			subscriber_number = Database.random_phone_number()
			print("subscriber_number: {}".format(subscriber_number))

			db.phone_number_is_subscribed_to_podium(subscriber_number, self.betty_podium_number)
			self.assertFalse(db.phone_number_is_subscribed_to_podium(subscriber_number, self.taylor_phone_number))
			db.subscribe_to_podium(subscriber_number, self.taylor_phone_number)
			self.assertTrue(db.phone_number_is_subscribed_to_podium(subscriber_number, self.taylor_phone_number))

