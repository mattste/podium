from flask import render_template, current_app

from . import main

@main.route('/', methods=['GET'])
def hello():
	current_db = current_app.config['RETHINKDB_DB']
	return render_template("hello.html", username="TheBigKahuna", current_db=current_db)
