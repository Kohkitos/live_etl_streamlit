# ------ LIBRARIES

## For web and plots
import streamlit as st
import pandas as pd
import plost
from streamlit_echarts import st_echarts
## For connecting to MongoDB
from pymongo import MongoClient
from passwords import *
# For time
from datetime import datetime

# ------- API FUNCTIONS
def message(param):
	"""
	This is a function that returns a JSON serching for the values specified in the param.

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

# --- CONFIG

st.set_page_config(page_title="Investment ETL", page_icon=":red_circle:", layout='wide', initial_sidebar_state='expanded')

# CSS
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# --- DELETE LATER (this will be done by the API)

db = MongoClient(STR_CONN).final_project

# --- SIDEBAR
with st.container():
    st.sidebar.markdown("## PEDRO SANCHEZ' INVESTMENT LIVE CHAT ANALYSIS\n`Iron Hack's Final Project`")

# ----- THIS SHOULD BE DONE BY THE SIDEBAR INFO
data = message("POSNEGNEU-0-0-0")

# --- CARDS
with st.container():
	col1, col2, col3, col4 = st.columns(4)
	
	col1.image('../img/user.png', width=50)
	col1.metric("Users", data['users'])
	
	col2.image('../img/chat.png', width=50)
	col2.metric("Comments", data['count'])
	
	col3.image('../img/bubble-chat.png', width=50)
	col3.metric("Average Comments per Minute", data['count'])
	
	col4.metric("Max Comments per Minute", 42)
	col4.metric("Min Comments per Minute", 42)

st.write('---')

# --- DONUT AND TABLE
with st.container():
	donut, table = st.columns([1, 2])
	with donut:
		st.markdown('### Sentiment Anal')
		options = {
            "tooltip": {"trigger": "item"},
            "series": [
                {
                    "name": "Sentiment",
                    "type": "pie",
                    "radius": ["25%", "65%"],
                    "data": [
                        {"value": 1048, "name": "lore", "itemStyle": {"color": '#ff6961'}}, # red
                        {"value": 735, "name": "pito", "itemStyle": {"color": '#fdfd96'}},  # yellow
                        {"value": 580, "name": "macu", "itemStyle": {"color": '#77dd77'}}   # green
                    ],
					"label": {
						"color": "white"
                    },
                    "emphasis": {
                        "itemStyle": {
                            "shadowBlur": 10,
                            "shadowOffsetX": 0,
                            "shadowColor": "rgba(0, 0, 0, 0.5)",
                        }
                    },
                }
            ],
        }
		st_echarts(options=options, height="300px")
	
	with table:
		df = pd.DataFrame(data['messages']).set_index('message')['sentiment_analysis']
		st.markdown('### Comments')
		st.dataframe(df)

st.write('---')

# --- LINE CHART