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

	def init_db(self, db):
		self.drop_db(db)
		self.create_db(db)
		self.connection.use(db)
		self.create_tables()

	def query_test_db(self):
		cur = r.table('tv_shows').run(self.connection)
		for doc in cur:
			print(doc)
		return

	def create_podium(self, title, creator):
		""" Creates a podium with `title`, `creator` is 
			a dict of info on podium creator.
			Args:
				title: string,
				creator: dict
		""" 
		r.table('podiums').insert({
				"title": title,
				"creator": creator	
			}).run(self.connection)

	def subscribe_to_podium(self, podium_title, phone_number):
		""" Subscribes `phone_number` to podium with `podium_title`
			Args:
				podium_title: string,
				phone_number: string
		"""
		r.table('podiums').get({
				"title": podium_title
			}).update({
				"subscribers": [phone_number]
			}).run(self.connection)

