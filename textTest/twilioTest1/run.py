from flask import Flask, request, redirect
import twilio.twiml

# Download the twilio-python library from http://twilio.com/docs/libraries
from twilio.rest import TwilioRestClient
 
# Find these values at https://twilio.com/user/account
account_sid = ""
auth_token = ""
client = TwilioRestClient(account_sid, auth_token)
 
app = Flask(__name__)
 
@app.route("/sendTexts", methods=['GET', 'POST'])
def sendTexts():
	message = client.messages.create(to="+17345520988", from_="+14243320631",
	                                     body="Hello there! Text me back please :)")

	message = client.messages.create(to="+12018355444", from_="+14243320631",
	                                     body="Hello there! Text me back please :)")

	message = client.messages.create(to="+16148321908", from_="+14243320631",
	                                     body="Hello there! Text me back please :)")

	message = client.messages.create(to="+15864847275", from_="+14243320631",
	                                     body="Hello there! Text me back please :)")

	return "YO"

@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    """Respond to incoming calls with a simple text message."""
 
    message = request.values.get('Body');
    print message

    resp = twilio.twiml.Response()
    if(message == "start" or message == "Start"):
		resp.message("Hello and Welcome to Podium! This is a tutorial for our new platform. Please respond to this message with '$test' to subscribe and recieve a test poll! If you would like to unsubscribe at any time, text \"Stop\" to this number.")
    elif(message == "$test"):
    	resp.message("What is your favorite flavor of ice cream (Please respond with A, B, C, or D)?\nA. Chocolate\nB. Vanilla\nC. Strawberry\nD. Other")
    else:
    	if(message == 'a' or message == 'A' or message == 'b' or message == 'B' or message == 'c' or message == 'C' or message == 'd' or message == 'D'):
    		resp.message("Thank you very much for your response! Have a great day :)")
    	else:
    		resp.message("Answer invalid.  Please respond with A, B, C, or D.")

    return str(resp)
 
if __name__ == "__main__":
    app.run(debug=True)