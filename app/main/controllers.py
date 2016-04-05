from flask import render_template, current_app, render_template, request, redirect

from . import main

@main.route('/', methods=['GET'])
def index():
	current_db = current_app.config['RETHINKDB_DB']
	return render_template("hello.html", username="TheBigKahuna", current_db=current_db)

@main.route('/apply', methods=['GET'])
def apply():
	current_db = current_app.config['RETHINKDB_DB']
	return render_template("hello.html")

@main.route('/podiums', methods=['GET'])
def podiums():
	current_db = current_app.config['RETHINKDB_DB']
	return render_template("hello.html")

#Receive podium responses for main Podium Number
@main.route('/podiumReceive', methods=['GET', 'POST'])
def podiumReceive():
	#Options for main Podium number
		#Start: Gives "Welcome to Podium Message"
		#Help: Displays "Help" message
		#'Podium Name': Subscribes to specific podium
		#Stop: Unsubscribes user from all podiums
		#Else: Please send valid command to Podium

	message = request.values.get('Body');
	print(message)
	return render_template("hello.html")

@main.route('/podiums/test-podium', methods=['GET'])
def testPodium():
	return render_template("test-podium.html")
