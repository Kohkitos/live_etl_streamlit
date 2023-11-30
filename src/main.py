# ---- LIBRARIES

## For web and plots
import streamlit as st
import pandas as pd
import plost
## For connecting to MongoDB
from pymongo import MongoClient
from passwords import *
# For time
from datetime import datetime



# ---- API FUNCTIONS

def message(param):
	"""This is a function that returns a JSON serching for the values specified in the param.

	The param should be structure as follows: {SENTIMEN}-{DAY}-{START TIMESTAMP}-{END TIMESTAMP}.
	{SENTIMENT}: a string with POS, NEG and NEU in any combination (e.g: POSNEG, NEGPOS, POSNEGNEU...)
	{DAY}: the day to look for, currently either 15 or 16; 0 will look for both days.
	{START TIMESTAMP}: from what time you want to look or in minutes (e.g: 5, 9, 0...)
	{END TIMESTAMP}: to what time you want to look or in minutes (e.g: 5, 9, 0...)

	Example of params:
		POSNEGNEU-O-O-1000 	(this param will return every message).
		POS-15-20-25		(this param will return positive messages on day 15 from minute 20 to 25)
		NEUNEG-0-0-30		(this param will return neutral and negative message from both days from the beggining to minute 30)

	Args:
		param (str): a string with the data to request.

	Returns:
		json: a JSON with the data requested as follows:
			{message_count: 	int,
			user_count:			int,
			messages:			json}
	"""

	# split params into parts and split sent into a list
	params = param.split('-')
	parts = split_3(params[0])

	# if both days are requested
	if params[1] == '0':
		messages = list(db.message.find({'sentiment_analysis': {'$in': parts},
						 'timestamp': { '$gte':  int(params[2]), '$lte': int(params[3])}
						 })
			       )
		
	# if only one day is requested
	else:
		date = datetime.now().replace(day=int(params[1]), hour=0, minute=0, second=0, microsecond=0)
		end_date = date.replace(day = int(param[1] + 1))

		messages = list(db.message.find({'sentiment_analysis': {'$in': parts},
						'timestamp': { '$gt':  params[2], '$lt': params[3]},
						"date": {"$gte": date, "$lt": end_date}})
	       )

	# get the user count	
	users = []
	for message in messages:
		if message['commentator_id'] in users:
			continue
		users.append(message['commentator_id'])

	result ={
		'count': len(messages),
		'users': len(users),
		'messages': messages
		}
	return result

def split_3(text):
    parts = [text[i:i + 3] for i in range(0, len(text), 3)]
    return parts