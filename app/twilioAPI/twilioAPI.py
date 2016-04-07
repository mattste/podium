from flask import Flask, current_app, render_template, request, redirect
import rethinkdb as r

from . import twilioAPI
import twilio.twiml
from twilio.rest import TwilioRestClient

class TwilioActions(object):

	def __init__(self):
		self.client = TwilioRestClient(current_app.config['TWILIO_ACCOUNT_SID'], current_app.config['TWILIO_AUTH_TOKEN'])

	def podiumSendPollOrShout(self, message, fromNumber, toNumber):
		message = self.client.messages.create(to=toNumber, from_=fromNumber,
	                                     body=message)
		print(message)

#client = TwilioRestClient(current_app.config['TWILIO_ACCOUNT_SID'], current_app.config['TWILIO_AUTH_TOKEN'])
#mainTwilioNumber = "+14243320631"

#Welcome to podium message that is sent to user
#startMessage = "Hello and Welcome to Podium! Text the name of a Podium account to subscribe or text 'stop' to unsubscribe from all Podiums."

#Success message when user successfully subscribes to podium (sent from main podium number)
#subscribeSuccess = "Congratulations! You have successfully subscribed to a Podium account!"

#Message confirming unsubscription from all podiums
#stopPodiumMessage = "You have successfully unsubscribed from all Podium accounts."


