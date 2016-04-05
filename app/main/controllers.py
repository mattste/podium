from flask import render_template, current_app, render_template, request, redirect
import re
from . import main
from ..twilioAPI.twilioAPI import TwilioActions

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

	message = request.values.get('Body').lower();
	fromNumber = request.values.get('From')
	print(fromNumber)
	start = re.search(r'start', message)
	stop = re.search(r'stop', message)

	#Get a list of all the podium handles
	#podiumAccounts = getPodiumHandles()

	#Loop thru podium handles and check if user's message matches existing account
		#If we get a result, subscribe user to podium (add their number to specific podium account's subscriber list)
		#subscribeName = 'name of account subscribing to'

	if(start):
		#Send start message
		twilioClient = TwilioActions()
		TwilioActions.podiumSendPollOrShout(twilioClient, "HOLA CHICO!", mainTwilioNumber, fromNumber)
		subscribeUser(fromNumber, 'tutorial')
		print("WOOO")
	elif(subscribeName):
		print("SUBSCRIBED")
	elif(stop):
		print("NOOOO")
	else:
		print("Please send a valid command.")

	print(message)
	return render_template("hello.html")

def subscribeUser(fromNumber, podiumAccountName):
	pass
	#addUserToDatabase(fromNumber, podiumAccountName)

def unsubscribeUser(fromNumber, podiumAccountName):
	pass
	#removeUserFromDatabase(fromNumber, podiumAccountName)

@main.route('/test-podium', methods=['GET'])
def testPodium():
	return render_template("test-podium.html")
