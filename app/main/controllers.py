from flask import render_template, current_app, render_template, request, redirect
import re
from . import main
from ..twilioAPI.twilioAPI import TwilioActions

@main.route('/', methods=['GET'])
def index():
	#shouts is array of:
		# shout = {
		# 	link: <link to associated podium>,
		# 	handle: <handle for associated podium>
		# 	message: <shout message>
		# }

	current_db = current_app.config['RETHINKDB_DB']
	return render_template("index.html", shouts=shouts)

@main.route('/apply', methods=['GET'])
def apply():
	#shouts is array of:
		# shout = {
		# 	link: <link to associated podium>,
		# 	handle: <handle for associated podium>
		# 	message: <shout message>
		# }

	current_db = current_app.config['RETHINKDB_DB']
	return render_template("hello.html")

@main.route('/podiums', methods=['GET'])
def podiums():
	#shouts is array of:
		# shout = {
		# 	link: <link to associated podium>,
		# 	handle: <handle for associated podium>
		# 	message: <shout message>
		# }
	#podiums is array of:
		# podium = {
		# 	link: <link to associated podium>,
		# 	handle: <handle for associated podium>
		# }

	current_db = current_app.config['RETHINKDB_DB']
	return render_template("podiums.html", shouts=shouts, podiums=podiums)

mainTwilioNumber = '+14243320631'

#Receive podium responses for main Podium Number
@main.route('/podiumReceive', methods=['GET', 'POST'])
def podiumReceive():
	#Options for main Podium number
		#Start: Gives "Welcome to Podium Message"
		#'Podium Name': Subscribes to specific podium
		#Stop: Unsubscribes user from all podiums
		#Else: Please send valid command to Podium

	message = request.values.get('Body').lower();
	fromNumber = request.values.get('From')
	toNumber = request.values.get('To')

	#Endpoint to deal with texts to main twilio number
	if(toNumber == mainTwilioNumber):
		parseMainResponse(message, fromNumber)
		pass
	else:
		pass
		#Query dB for toNumber to see which podium responded to
		#Create function to parse response from user

	print(message)
	return render_template("hello.html")

def parseMainResponse(message, fromNumber):
	start = re.search(r'start', message)
	stop = re.search(r'stop', message)
	twilioClient = TwilioActions()

	#Get a list of all the podium handles
	#podiumAccounts = getPodiumHandles()

	#Loop thru podium handles and check if user's message matches existing account
		#If we get a result, subscribe user to podium (add their number to specific podium account's subscriber list)
	subscribeName = 'name of account subscribing to'

	if(start):
		#Send start message
		TwilioActions.podiumSendPollOrShout(twilioClient, "Welcome message", mainTwilioNumber, fromNumber)
		subscribeUser(fromNumber, 'tutorial')
		print("WOOO")
	elif(subscribeName):
		pass
		#ValidateSubscription(subscribeName, fromNumber)
		#Subscribe(subscribeName, fromNumber)
		#TwilioActions.podiumSendPollOrShout(twilioClient, "You have successfully subscribed", mainTwilioNumber, fromNumber)
	elif(stop):
		unsubscribeAll(fromNumber)
		TwilioActions.podiumSendPollOrShout(twilioClient, "You have successfully been unsubscribed from all Podium accounts.", mainTwilioNumber, fromNumber)
	else:
		TwilioActions.podiumSendPollOrShout(twilioClient, "Please send a valid command.", mainTwilioNumber, fromNumber)

def parseResponse(message, fromNumber, toNumber):
	#Check from toNumber which podium account they are talking to
	#Get most recent poll and do appropriate action
	pass

def subscribeUser(fromNumber, podiumAccountName):
	pass
	#addUserToDatabase(fromNumber, podiumAccountName)

def unsubscribeUser(fromNumber, podiumAccountName):
	pass
	#removeUserFromDatabase(fromNumber, podiumAccountName)

def unsubscribeAll(fromNumber):
	#loop thru all podium accounts
		#call unsubscribeUser(fromNumber, podiumAccountName) for all accounts
	pass

@main.route('/test-podium', methods=['GET'])
def testPodium():
	return render_template("test-podium.html")
