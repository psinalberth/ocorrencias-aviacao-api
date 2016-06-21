from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = True

#Include config from config.py
app.config.from_object('config')
app.secret_key = 'some_secret'

#Create an instance of SQLAclhemy
db = SQLAlchemy(app)
ma = Marshmallow(app)

@app.after_request
def after_request(response):
	response.headers.add('Access-Control-Allow-Origin', '*')
	response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
	response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')	
	return response


