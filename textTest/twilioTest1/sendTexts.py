# Download the twilio-python library from http://twilio.com/docs/libraries
from twilio.rest import TwilioRestClient
 
# Find these values at https://twilio.com/user/account
account_sid = ""
auth_token = ""
client = TwilioRestClient(account_sid, auth_token)
 
message = client.messages.create(to="+17345520988", from_="+14243320631",
                                     body="Hello there! Text me back please :)")

message = client.messages.create(to="+12018355444", from_="+14243320631",
                                     body="Hello there! Text me back please :)")

message = client.messages.create(to="+16148321908", from_="+14243320631",
                                     body="Hello there! Text me back please :)")

message = client.messages.create(to="+15864847275", from_="+14243320631",
                                     body="Hello there! Text me back please :)")