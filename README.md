## Virtualenv Commands
Create the virtual environment in the parent folder:
`virtualenv -p python3 podium-venv`

Activate the virtual environment:
`source podium-venv/bin/activate`

Deactivate:
`deactivate`

## Setup
Install [RethinkDB](http://rethinkdb.com/). Instructions for all platforms [here](http://rethinkdb.com/docs/install/). On OSX:
`brew update && brew install rethinkdb`

Install the requirements:
`pip install -r requirements.txt`

Install [Compass](http://compass-style.org/install/) which is used for static assets. 

## Modifying the Stylesheets
Navigate to '/app/static'
Run `compass watch` if you modify the SCSS files. It will compile them to native css upon saving.

## Database Info
Start RethinkDB by running the following in your shell:
`rethinkdb`
RethinkDB has a cool web interface at localhost:8080 that allows you to do queries, manage your tables and see query latency.

To populate with test data, use the following command (in the main terminal):

python -m unittest app.tests.test_database.DatabaseTestCase.test_populate_with_mock

## Live Graphing Backend

Install node on your system

Install all requirements:
  Go into app_node folder and type in `npm install package.json`
  
Run:
  `node sockets.js`

## Run App

Use the following command:

  `python manage.py runserver`

## Twilio

In order for Twilio to work effectively, you need to have a valid Account SID and Auth Token stored in the cfg file(s) in the envs folder.  

Additionally, you need to have setup a Twilio account online and paid for valid phone numbers to assign to your Podium 'Leader' accounts (in addition to the main Podium account).

For each phone number, you need to assign web endpoints for the incoming messages to be sent to (this is done via the online Twilio admin interface in the Phone number options setting).  In order to do this, you need to either host the web app or use ngrok to temporarily put the website online so you can obtain a valid url.

####Credit
Base project structure based off of Miguel Grinberg's [flasky](https://github.com/miguelgrinberg/flasky)
