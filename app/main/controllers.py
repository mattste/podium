from flask import render_template, current_app, render_template, request, redirect, jsonify
import re

from . import main
from ..twilioAPI.twilioAPI import TwilioActions
from ..db.database import Database

@main.route('/', methods=['GET'])
def index():
	db = Database()
	shouts = db.get_shouts()
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
	return render_template("apply.html")

@main.route('/podiums', methods=['GET'])
def podiums():

	db = Database()
	shouts = db.get_shouts()
	podiums = [{"podium_title": podium["title"]} for podium in db.get_podiums()]
	return render_template("podiums.html", shouts=shouts, podiums=podiums)


mainTwilioNumber = '+14243320631'

@main.route('/podium/<podium_title>/poll/create', methods=['GET'])
def create_poll_get(podium_title):
	return render_template("poll.html", podium_title=podium_title)

@main.route('/podium/poll/create', methods=['POST'])
def create_poll_post():
	poll_info = request.get_json()
	print(poll_info)
	podium_title = poll_info.get("podium_title")
	if podium_title is None:
		return jsonify({"message": "You did not provide a podium title in your request"})
	
	createPoll(podium_title, poll_info)
	return jsonify({"message": "You've successfully created your poll! Let's see what your subscribers have to say."})

#Receive podium responses for main Podium Number
@main.route('/podiumReceive', methods=['GET', 'POST'])
def podiumReceive():
	#Options for main Podium number
		#Start: Gives "Welcome to Podium Message"
		#'Podium Name': Subscribes to specific podium
		#Stop: Unsubscribes user from all podiums
		#Else: Please send valid command to Podium

	message = request.values.get('Body').lower()
	message = message.strip()
	fromNumber = request.values.get('From')
	toNumber = request.values.get('To')

	#Endpoint to deal with texts to main twilio number
	if(toNumber == mainTwilioNumber):
		parseMainResponse(message, fromNumber, toNumber)
		pass
	else:
		parseResponse(message, fromNumber, toNumber)
		pass
		#Query dB for toNumber to see which podium responded to
		#Create function to parse response from user

	print(message)
	return ('', 200)

def parseMainResponse(message, subscriber_number, podium_number):
	start = re.search(r'start', message)
	stop = re.search(r'stop', message)
	twilioClient = TwilioActions()

	#Get a list of all the podium handles
	podiumAccounts = getPodiumHandles()

	subscribe_to_podium = None
	#Loop thru podium handles and check if user's message matches existing account
	for podium in podiumAccounts:
		#If we get a result, subscribe user to podium (add their number to specific podium account's subscriber list)
		if (podium['title'].lower() == message):
			subscribe_to_podium = podium
			break

	if(start):
		#Send start message
		message = ("Welcome to Podium! Text the name of a Podium to subscribe to it. "
		"Text stop to unsubscribe from all podiums. Text anything else to receive an error! "
		"Respond with the message \"Tutorial\" to see what Podium is all about.")
		TwilioActions.podiumSendPollOrShout(twilioClient, message, mainTwilioNumber, subscriber_number)
		subscribeUser(subscriber_number, podium_number)
	elif(subscribe_to_podium):
		#ValidateSubscription(subscribeName, subscriber_number)
		subscribeUser(subscriber_number, podium['podium_number'])
		TwilioActions.podiumSendPollOrShout(twilioClient, "You have successfully subscribed to {}. High five! Wait...I'm a phone. Beep boop bop bop.".format(subscribe_to_podium["title"]), podium['podium_number'], subscriber_number)
	elif(stop):
		unsubscribeAll(subscriber_number)
		TwilioActions.podiumSendPollOrShout(twilioClient, "You have successfully been unsubscribed from all Podium accounts. Tis a sad moment.", mainTwilioNumber, subscriber_number)
	else:
		TwilioActions.podiumSendPollOrShout(twilioClient, "Please send a valid command.", mainTwilioNumber, subscriber_number)

def getPodiumHandles():
	db = Database()
	return db.get_podiums()

def createPoll(podium_title, poll_info):
	db = Database()
	podium = db.get_podium(podium_title)
	subscribers = podium.get("subscribers", [])
	podium_number = podium["podium_number"]
	db.create_poll(question=poll_info["question"], options=poll_info["options"], podium_number=podium_number)
	
	twilioClient = TwilioActions()
	options = "\n ".join(option for option in poll_info["options"])
	message = "{} has a question! {} Text back one of the following options: \n\n {}".format(podium_title, poll_info["question"], options)
	for subscriber_number in subscribers:
		TwilioActions.podiumSendPollOrShout(twilioClient, message, podium_number, subscriber_number)

def parseResponse(message, fromNumber, toNumber):
	'''remove nonalpha, make lowercase, split on spaces, check first elt of list,
	see if a,b,c,d,e then store if not check for option from poll sent out'''

	message = re.sub('[^0-9a-zA-Z]+', ' ', message)
	term_list = message.split(" ")

	#send term_list[0] to dB as response to poll
	response = {
		"subscriber_number": fromNumber,
		"option": term_list[0]
	}

	db = Database()

	print("ok till now")

	db.respond_to_latest_podium_poll(response, toNumber)

	response_text = "Thank you for responding to the Poll.  Visit https://www.youtube.com/watch?v=otfy8dRqeFI to see results. Have a great day!"
	twilioClient = TwilioActions()
	twilioClient.podiumSendPollOrShout(response_text, toNumber, fromNumber)
	#Check from toNumber which podium account they are talking to
	#Get most recent poll and do appropriate action
	pass

def subscribeUser(subscriber_number, podium_number):
	db = Database()
	db.subscribe_to_podium(subscriber_number=subscriber_number, podium_number=podium_number)

def unsubscribeUser(fromNumber, podiumAccountName):
	pass
	#removeUserFromDatabase(fromNumber, podiumAccountName)

def unsubscribeAll(fromNumber):
	#loop thru all podium accounts
		#call unsubscribeUser(fromNumber, podiumAccountName) for all accounts
	pass

@main.route('/podium/<podium_title>', methods=['GET'])
def podium(podium_title):
	db = Database()
	shouts = db.get_shouts()
	podium = db.get_podium(podium_title=podium_title)
	latest_poll = db.get_latest_podium_poll(podium_title=podium_title)
	podium_info = {
		"title": podium["title"],
		"num_subscribers": len(podium["subscribers"]),
		"description": podium["description"],
		"latest_poll": {
			"results": "None",
			"question": latest_poll["question"],
			"options": latest_poll["options"]
		}
	}
	return render_template("podium.html", shouts=shouts, podium=podium_info)
