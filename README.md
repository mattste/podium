## Setup
Install [RethinkDB](http://rethinkdb.com/). Instructions for all platforms [here](http://rethinkdb.com/docs/install/). On OSX:
`brew update && brew install rethinkdb`

Install the requirements:
`pip install -r requirements.txt`

Install [Compass](http://compass-style.org/install/) which is used for static assets. 

## Virtualenv Commands
Create the virtual environment in the parent folder:
`virtualenv -p python3 podium-venv`

Activate the virtual environment:
`source podium-venv/bin/activate`

Deactivate:
`deactivate`

## Modifying the Stylesheets
Navigate to '/app/static'
Run `compass watch` if you modify the SCSS files. It will compile them to native css upon saving.

## Database Info
Start RethinkDB by running the following in your shell:
`rethinkdb`
RethinkDB has a cool web interface at localhost:8080 that allows you to do queries, manage your tables and see query latency.

####Credit
Base project structure based off of Miguel Grinberg's [flasky](https://github.com/miguelgrinberg/flasky)
