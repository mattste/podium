import random
import time

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

	@staticmethod
	def random_phone_number():
		return ''.join(["%s" % random.randint(0, 9) for num in range(0, 10)])

	@staticmethod
	def random_poll_response_option():
		options = ["A", "B", "C", "D"]
		return random.choice(options)

	def populate_with_mock(self, db):
		self.init_db(db)
		self.create_podium(title='Tutorial', creator={"name": "Podium"}, podium_number="5861231234", 
			description="Interested in learning how Podium works? Subscribe to the tutorial and we'll guide you through the steps!")
		betty_podium_number = "5863172914"
		self.create_podium(title='BettyCSG', creator={"name": "Betty Blue"}, podium_number=betty_podium_number, 
			description="I'm an elected member of @umich CSG. Subscribe to my podium for polls and shouts relevant to you. Let your voice be heard.")
		self.subscribe_to_podium(subscriber_number="1234567899", podium_number=betty_podium_number)
		self.send_shout(shout_message="Thanks for all of your support! I can't wait to vote on issues important to my fellow students!", podium_number=betty_podium_number)
		self.create_poll(question="How often do you ride the bus to North Campus per week?", options=["A. 1", "B. 3", "C. 5", "D. 7+"], podium_number=betty_podium_number)

		taylor_phone_number = "3982482000"
		self.create_podium(title='TaylorSwift', creator={"name": "Taylor Swift"}, podium_number=taylor_phone_number, 
			description="I make music and always have a broken heart.")
		self.subscribe_to_podium(subscriber_number="1234567899", podium_number=taylor_phone_number)
		self.send_shout(shout_message="I can't believe Kanye just did that to me!", podium_number=taylor_phone_number)
		self.create_poll(question="Are you a Kanye West fan after what he just did to me?", options=["A. Yes", "B. No"], podium_number=taylor_phone_number)

		bernie_sanders_number = "4824814882"
		self.create_podium(title='FeelTheBern', creator={"name": "Bernie Sanders"}, podium_number=bernie_sanders_number, 
			description="I am starting a political revolution. I want to hear your voice on the issues.")
		self.subscribe_to_podium(subscriber_number="1234567899", podium_number=bernie_sanders_number)
		self.send_shout(shout_message="We just won in Wisconsin! I'll be coming to New York next. Sign-up to volunteer at berniesanders.com", podium_number=bernie_sanders_number)
		self.create_poll(question="What is the most important issue to New Yorkers?", options=["A. Income inequality", "B. Rigged elections", "C. Universal healthcare", "D. Free tuition"], podium_number=bernie_sanders_number)
		
		for i in range(0, 10):
			subscriber_number = Database.random_phone_number()
			self.subscribe_to_podium(subscriber_number, bernie_sanders_number)
			response = {
				"subscriber_number": subscriber_number, 
				"option": Database.random_poll_response_option(),
				"response_datetime": time.time()
			}
			self.respond_to_latest_podium_poll(response=response, podium_number=bernie_sanders_number)

		

	def send_shout(self, shout_message, podium_number):
		""" Sends `shout_message` to all subscribers of the podium that is retrieved using kwargs.
			Args:
				shout_message: string
				kwargs: any valid keys on a podium
		"""
		r.table('podiums').filter({"podium_number": podium_number}).update({
				"shouts": r.row["shouts"].append(shout_message)
			}).run(self.connection)


	def create_podium(self, title, creator, podium_number, description):
		""" Creates a podium with `title`, `creator` is 
			a dict of info on podium creator.
			Args:
				title: string,
				podium_number: string,
				creator: dict,
				description: string
		""" 
		r.table('podiums').insert({
				"title": title,
				"podium_number": podium_number,
				"creator": creator,
				"description": description	
			}).run(self.connection)

	def subscribe_to_podium(self, subscriber_number, podium_number):
		""" Subscribes `subscriber_number` to podium with search based on kwargs
			Args:
				podium_title: string,
				subscriber_number: string
		"""
		r.table('podiums').filter({"podium_number": podium_number}).update({
				"subscribers": r.row["subscribers"].append(subscriber_number).default([subscriber_number])
			}).run(self.connection)

	def get_podium(self, podium_title):
		""" Retrieves podium with title `podium_title`.
			Args:
				podium_title: string
		"""
		return r.table('podiums').filter({"title": podium_title}).run(self.connection).next()

	def create_poll(self, question, options, podium_number):
		""" Creates a poll for `podium_number` with `question` as the sent message
			Args:
				podium_number: string,
				question: string,
				options: array of strings
		""" 
		cursor = r.table('podiums').filter({"podium_number": podium_number}).pluck('id').run(self.connection)
		podium = cursor.next()		
		r.table('polls').insert({"question": question, "options": options, "podium_id": podium["id"]}).run(self.connection)

	def polls_podium_join(self, query, podium_filters):
		""" Equality joins `polls` and `podiums` tables based on podium keys passed in """
		return query.table('polls').eq_join('podium_id', r.table('podiums')) \
			.filter({"right": podium_filters})

	def respond_to_latest_podium_poll(self, response, podium_number):
		""" Stores a response for `podium_number` latest poll. 
			Args:
				response: {
					subscriber_number: string,
					option: string
				},
				subscriber_number: string
		"""
		# add uuid to passed in response
		response["id"] = r.uuid().run(self.connection)

		query = r
		poll_id = self.polls_podium_join(query, {"podium_number": podium_number}) \
			.run(self.connection) \
			.next()["left"]["id"]
		r.table('polls').get(poll_id).update({
				"responses": r.row["responses"].append(response).default([response])
			}) \
			.run(self.connection)

	def get_shouts(self, limit=10):
		""" Gets 10 podiums and their latest shouts """
		podiums = list(r.table('podiums').has_fields('shouts').pluck('title','shouts').limit(10).run(self.connection))
		return [{"podium_title": podium["title"], "shout_message": podium["shouts"][0]} for podium in podiums]

	def get_latest_podium_poll(self, podium_title):
		""" Gets the latest poll for podium with `podium_title` """
		query = r
		return self.polls_podium_join(query, {"title": podium_title}) \
			.without("right", {"left": ["podium_id", "id"]}) \
			.run(self.connection).next()["left"]

	def get_podiums(self):
		""" Retrieves all podiums """
		return r.table('podiums').run(self.connection)



