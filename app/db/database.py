from flask import current_app
import rethinkdb as r

from . import rethinkdb

class Database(object):

	def __init__(self):
		self.connection = rethinkdb.conn

	def drop_db(self, db, silent=True):
		try:
			r.db_drop(db).run(self.connection)
		except r.errors.ReqlOpFailedError as err:
			if not silent:
				raise err

	def create_db(self, db):
		r.db_create(db).run(self.connection)

	def create_tables(self):
		r.table_create('podiums').run(self.connection)
		r.table_create('polls').run(self.connection)

	def init_db(self, db):
		self.drop_db(db)
		self.create_db(db)
		self.connection.use(db)
		self.create_tables()

	def populate_with_mock(self, db):
		self.init_db(db)
		self.create_podium(title='Tutorial', creator={"name": "Podium"}, podium_number="5861231234", 
			summary="Interested in learning how Podium works? Subscribe to the tutorial and we'll guide you through the steps!")
		betty_podium_number = "5863172914"
		self.create_podium(title='BettyCSG', creator={"name": "Betty Blue"}, podium_number=betty_podium_number, 
			summary="I'm an elected member of @umich CSG. Subscribe to my podium for polls and shouts relevant to you. Let your voice be heard.")
		self.subscribe_to_podium(subscriber_number="1234567899", podium_number=betty_podium_number)
		self.send_shout(shout_message="Thanks for all of your support! I can't wait to vote on issues important to my fellow students!", podium_number=betty_podium_number)
		self.create_poll(question="How often do you ride the bus to North Campus per week? A. 1, B. 3, C. 5, D. 7+", podium_number=betty_podium_number)

	def send_shout(self, shout_message, podium_number):
		""" Sends `shout_message` to all subscribers of the podium that is retrieved using kwargs.
			Args:
				shout_message: string
				kwargs: any valid keys on a podium
		"""
		r.table('podiums').filter({"podium_number": podium_number}).update({
				"shouts": [shout_message]
			}).run(self.connection)


	def create_podium(self, title, creator, podium_number, summary):
		""" Creates a podium with `title`, `creator` is 
			a dict of info on podium creator.
			Args:
				title: string,
				podium_number: string,
				creator: dict,
				summary: string
		""" 
		r.table('podiums').insert({
				"title": title,
				"podium_number": podium_number,
				"creator": creator,
				"summary": summary	
			}).run(self.connection)

	def subscribe_to_podium(self, subscriber_number, podium_number):
		""" Subscribes `subscriber_number` to podium with search based on kwargs
			Args:
				podium_title: string,
				subscriber_number: string
		"""
		r.table('podiums').filter({"podium_number": podium_number}).update({
				"subscribers": [subscriber_number]
			}).run(self.connection)

	def get_podium(self, podium_number):
		""" Retrieves podium with kwargs dict variables.
			Args:
				podium_title: string
		"""
		r.table('podiums').filter({"podium_number": podium_number}).run(self.connection)

	def create_poll(self, question, podium_number):
		""" Creates a poll for `podium_number` with `question` as the sent message
			Args:
				podium_number: string,
				question: string
		""" 
		cursor = r.table('podiums').filter({"podium_number": podium_number}).pluck('id').run(self.connection)
		podium = cursor.next()		
		r.table('polls').insert({"question": question, "podium_id": podium["id"]}).run(self.connection)


