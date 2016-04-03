from flask import Flask, current_app, render_template, request, redirect
import rethinkdb as r
import twilio.twiml
from twilio.rest import TwilioRestClient

from . import twilio
from . import main

client = TwilioRestClient(current_app.config['TWILIO_ACCOUNT_SID'], current_app.config['TWILIO_AUTH_TOKEN'])
mainTwilioNumber = "+14243320631"

#Welcome to podium message that is sent to user
startMessage = "Hello and Welcome to Podium! Text the name of a Podium account to subscribe or text 'stop' to unsubscribe from all Podiums."

#Success message when user successfully subscribes to podium (sent from main podium number)
subscribeSuccess = "Congratulations! You have successfully subscribed to a Podium account!"

#Message confirming unsubscription from all podiums
stopPodiumMessage = "You have successfully unsubscribed from all Podium accounts."

@twilio.route('/podiumReceive', methods=['GET', 'POST'])
def podiumReceive():
	#Options for main Podium number
		#Start: Gives "Welcome to Podium Message"
		#Help: Displays "Help" message
		#'Podium Name': Subscribes to specific podium
		#Stop: Unsubscribes user from all podiums
		#Else: Please send valid command to Podium

	message = request.values.get('Body');
	print(message)

def podiumSendPollOrShout(message, fromNumber, toNumber):
	message = client.messages.create(to=toNumber, from_=fromNumber,
                                     body=message)
	print message

#Receiving routes for individual Podium accounts (manually setup these routes for individual numbers on admin side of twilio website)
@twilio.route('/podiumReceive123456789', methods=['GET', 'POST'])
def podiumReceive():
	fromNumber = "+1123456789"
	#Options for individual Podium numbers
		#'Answer to poll': Sends user's response to a poll
		#Stop: Unsubscribes user from all podiums

	message = request.values.get('Body');


