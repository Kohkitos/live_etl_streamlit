# ------ LIBRARIES

## For web and plots
import streamlit as st
import pandas as pd
import numpy as np
from streamlit_echarts import st_echarts
## For connecting to MongoDB
from pymongo import MongoClient
from passwords import *
# For time
from datetime import datetime, timedelta

# ------- API FUNCTIONS (delete later)
def message_15(param):
	"""
	This is a function that returns a JSON serching for the values specified in the param.

	The param should be structure as follows: {SENTIMEN}-{START TIMESTAMP}-{END TIMESTAMP}.
	{SENTIMENT}: a string with POS, NEG and NEU in any combination (e.g: POSNEG, NEGPOS, POSNEGNEU...)
	{START TIMESTAMP}: from what time you want to look or in minutes (e.g: 5, 9, 0...)
	{END TIMESTAMP}: to what time you want to look or in minutes (e.g: 5, 9, 0...)

	Example of params:
		POSNEGNEU-O-1000 	(this param will return every message).
		POS-20-25			(this param will return positive messages on day 15 from minute 20 to 25)
		NEUNEG-0-30			(this param will return neutral and negative message from both days from the beggining to minute 30)

	Args:
		param (str): a string with the data to request.

	Returns:
		json: a JSON with the data requested as follows:
			{message_count: 		int,
			user_count:				int,
			SENT_messages:			json}
	"""

	# split params into parts and split sent into a list
	params = param.split('-')
	parts = split_3(params[0])

	# initialize result dictionary and users
	users = []
	result = {}
	result['count'] = 0

	date = datetime.now().replace(day=15, hour=0, minute=0, second=0, microsecond=0)
	end_date = date.replace(day = 17)
	for part in parts:
		messages = list(db.message.find({'sentiment_analysis': {'$in': parts},
						'timestamp': { '$gt':  params[1], '$lt': params[2]},
						"date": {"$gte": date, "$lt": end_date}})
		)
		# prepare key names
		name = f'{part}_messages'
		count_name = f'{part}_count'
		# prepare count
		count = len(messages)
		# update users
		for message in messages:
			if message['commentator_id'] in users:
				continue
			users.append(message['commentator_id'])
		# update result
		result[name] = messages
		result[count_name] = count
		result['count'] += count

	# get the user count	
	result['users'] = len(users)
	return result

def message_16(param):
	"""
	This is a function that returns a JSON serching for the values specified in the param.

	The param should be structure as follows: {SENTIMEN}-{START TIMESTAMP}-{END TIMESTAMP}.
	{SENTIMENT}: a string with POS, NEG and NEU in any combination (e.g: POSNEG, NEGPOS, POSNEGNEU...)
	{START TIMESTAMP}: from what time you want to look or in minutes (e.g: 5, 9, 0...)
	{END TIMESTAMP}: to what time you want to look or in minutes (e.g: 5, 9, 0...)

	Example of params:
		POSNEGNEU-O-1000 	(this param will return every message).
		POS-20-25			(this param will return positive messages on day 15 from minute 20 to 25)
		NEUNEG-0-30			(this param will return neutral and negative message from both days from the beggining to minute 30)

	Args:
		param (str): a string with the data to request.

	Returns:
		json: a JSON with the data requested as follows:
			{message_count: 		int,
			user_count:				int,
			SENT_messages:			json}
	"""

	# split params into parts and split sent into a list
	params = param.split('-')
	parts = split_3(params[0])

	# initialize result dictionary and users
	users = []
	result = {}
	result['count'] = 0

	date = datetime.now().replace(day=16, hour=0, minute=0, second=0, microsecond=0)
	end_date = date.replace(day = 17)
	for part in parts:
		messages = list(db.message.find({'sentiment_analysis': {'$in': parts},
						'timestamp': { '$gt':  params[1], '$lt': params[2]},
						"date": {"$gte": date, "$lt": end_date}})
		)
		# prepare key names
		name = f'{part}_messages'
		count_name = f'{part}_count'
		# prepare count
		count = len(messages)
		# update users
		for message in messages:
			if message['commentator_id'] in users:
				continue
			users.append(message['commentator_id'])
		# update result
		result[name] = messages
		result[count_name] = count
		result['count'] += count

	# get the user count	
	result['users'] = len(users)
	return result

def split_3(text):
    parts = [text[i:i + 3] for i in range(0, len(text), 3)]
    return parts

def get_timestamps(colec):
    dates = [datetime(2023, 11, 15, 0, 0, 0), datetime(2023, 11, 16, 0, 0, 0)]
    res = {}

    for date in dates:
        next_day = date + timedelta(days=1)
        docs = colec.find({
            'date': {
                '$gte': date,
                '$lt': next_day
            }
        })

        ordered = sorted(docs, key=lambda x: x['timestamp'] if 'timestamp' in x else 0)
        res[date.day] = {
            'start': ordered[0]['timestamp'] if ordered else None,
            'finish': ordered[-1]['timestamp'] if ordered else None
        }

    return res
# --- CONFIG

st.set_page_config(page_title="Investment ETL", page_icon=":red_circle:", layout='wide', initial_sidebar_state='expanded')

# CSS
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# --- DELETE LATER (this will be done by the API)

db = MongoClient(STR_CONN).final_project

# --- SIDEBAR

# get timestamps
timestamps = get_timestamps(db.message)
day_15 = [x for x in range(timestamps[15]['start'], timestamps[15]['finish'] + 1)]
day_16 = [x for x in range(timestamps[16]['start'], timestamps[16]['finish'] + 1)]
# set default day to both
day = 'both'


with st.container():
    st.sidebar.markdown("## PEDRO SANCHEZ' INVESTMENT LIVE CHAT ANALYSIS\n`Iron Hack's Final Project`")
    
    col1, col2, col3 = st.sidebar.columns(3)
    
    if col1.button('Day 15'):
        day = '15'
    if col2.button('Day 16'):
        day = '16'
    if col3.button('Both'):
        day = 'both'

    st.sidebar.markdown(f'#### The day selected is {day}')

    if day != '16':
        start_15, end_15 = st.sidebar.select_slider(
            "Select timestamp's range from day 15",
            options=day_15,
            value=(timestamps[15]['start'], timestamps[15]['finish']))

    if day != '15':
        start_16, end_16 = st.sidebar.select_slider(
            "Select timestamp's range from day 16",
            options=day_16,
            value=(timestamps[16]['start'], timestamps[16]['finish']))

# ---- PREPARE INFO
sent = "NEGPOSNEU"
sents = split_3(sent)

try:
	total_minutes_15 = end_15 - start_15
	total_minutes_16 = end_16 - start_16
	total_minutes = (total_minutes_16 + total_minutes_15) // 2
	start = min(start_15, start_16)
	end = max(end_15, end_16)

	data_15 = message_15(f"{sent}-{start}-{end}")
	data_16 = message_16(f"{sent}-{start}-{end}")
	# cards info
	users = data_15['users'] + data_16['users']
	count = data_15['count'] + data_16['count']
except:
	try:
		total_minutes = end_15 - start_15
		start = start_15
		end = end_15
		data = message_15(f"{sent}-{start}-{end}")

		users = data_15['users']
	except:
		total_minutes = end_16 - start_16
		start = start_16
		end = end_16
		data = message_16(f"{sent}-{start}-{end}")
	# cards info
	users = data['users']
	count = data['count']


# --- CARDS

with st.container():
	col1, col2, col3, col4 = st.columns(4)
	
	col1.image('../img/user.png', width=50)
	col1.metric("Users", users)
	
	col2.image('../img/chat.png', width=50)
	col2.metric("Comments", users)
	
	col3.image('../img/bubble-chat.png', width=50)
	col3.metric("Average Comments per Minute", count // total_minutes)
	
	col4.metric("Max Comments per Minute", 42)
	col4.metric("Min Comments per Minute", 42)

st.write('---')

# --- DONUT AND TABLE

def apply_style_to_row(row):
    if row['sentiment_analysis'] == 'POS':
        row_style =  ['background-color: #77dd77'] * len(row)
    elif row['sentiment_analysis'] == 'NEG':
        row_style =  ['background-color: #ff6961'] * len(row)
    else:
        row_style = ['background-color: #fdfd96'] * len(row)
	
    message_style = ['color: black'] * len(row)
    
    combined_style = [f"{row_style[i]}; {message_style[i]}" for i in range(len(row))]
    
    return combined_style

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
                        {"value": len(data['NEG_messages']), "name": "NEG", "itemStyle": {"color": '#ff6961'}}, 	# red
                        {"value": len(data['NEU_messages']), "name": "NEU", "itemStyle": {"color": '#fdfd96'}},  	# yellow
                        {"value": len(data['POS_messages']), "name": "POS", "itemStyle": {"color": '#77dd77'}}   	# green
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
		# prepare dataframe with possible sents
		df = pd.DataFrame()
		for sent in sents:
			key = f"{sent}_messages"
			part_df = pd.DataFrame(data[key])
			df = pd.concat([df, part_df], ignore_index=True)
		sort_df = df.sort_values(by='date').reset_index(drop=True)

		st.markdown('### Comments')
		df_2 = sort_df[['message', 'sentiment_analysis']]
		styled_df = df_2.style.apply(apply_style_to_row, axis=1)
		st.write(styled_df)

st.write('---')

# --- LINE CHART
# set-up colours
colors = {
    "NEG": "#ff6961",
    "NEU": "#fdfd96",
    "POS": "#77dd77"
}

messages_per_sentiment = {}

for sent in sents:
	sent_df = df[df['sentiment_analysis'] == sent]
	message_count = sent_df.groupby('timestamp').size().reset_index(name='count')
	messages_per_sentiment[sent] = message_count.set_index('timestamp')['count']
	
final_df = pd.DataFrame(messages_per_sentiment)

plot_colors = []
used_sents = []
for i,row in sort_df.iterrows():
	sent = row['sentiment_analysis']
	if sent not in used_sents:
		used_sents.append(sent)
		plot_colors.append(colors[sent])
	
	if len(used_sents) == len(sents):
		break
	

with st.container():
	st.markdown('### Messages per Minute')
	st.line_chart(final_df, 
                use_container_width=True,
				color=plot_colors)