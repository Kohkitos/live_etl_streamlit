# ------ LIBRARIES

## For web and plots
import streamlit as st
import pandas as pd
import numpy as np
from streamlit_echarts import st_echarts
# For graphics options
from options import donut_option

#delete later
from api import *

# --- CONFIG

st.set_page_config(page_title="Investiture ETL", page_icon=":red_circle:", layout='wide', initial_sidebar_state='expanded')

# CSS
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# --- SIDEBAR

# get timestamps
timestamps = get_timestamps(db.message)
day_15 = [x for x in range(timestamps[15]['start'], timestamps[15]['finish'] + 1)]
day_16 = [x for x in range(timestamps[16]['start'], timestamps[16]['finish'] + 1)]
# set default day to both
day = 'both'


with st.container():
    st.sidebar.markdown("## PEDRO SANCHEZ' INVESTITURE LIVE CHAT ANALYSIS\n`Iron Hack's Final Project`")
    
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

	data_15 = message_15(f"{sent}-{start_15}-{end_15}")
	data_16 = message_16(f"{sent}-{start_16}-{end_16}")
	# cards info
	users = data_15['users'] + data_16['users']
	count = data_15['count'] + data_16['count']
	counts_15 = max_min_comments(start_15, end_15)
	counts_16 = max_min_comments(start_16, end_16)
	maxim = max(counts_15['max_comments']['count'], counts_16['max_comments']['count'])
	minim = min(counts_15['min_comments']['count'], counts_16['min_comments']['count'])
	# donut info
	total_pos = len(data_15['POS_messages']) + len(data_16['POS_messages'])
	total_neu = len(data_15['NEU_messages']) + len(data_16['NEU_messages'])
	total_neg = len(data_15['NEG_messages']) + len(data_16['NEG_messages'])
	
	data ={
        'POS_messages': data_15['POS_messages'] + data_16['POS_messages'],
        'NEU_messages': data_15['NEU_messages'] + data_16['NEU_messages'],
        'NEG_messages': data_15['NEG_messages'] + data_16['NEG_messages']
    }
except:
	try:
		total_minutes = end_15 - start_15
		start = start_15
		end = end_15
		data = message_15(f"{sent}-{start_15}-{end_15}")
		users = data['users']
		counts = max_min_comments(start_15, end_15)
	except:
		total_minutes = end_16 - start_16
		start = start_16
		end = end_16
		data = message_16(f"{sent}-{start_16}-{end_16}")
		users = data['users']
		counts = max_min_comments(start_16, end_16)
	# cards info
	users = data['users']
	count = data['count']
	maxim = counts['max_comments']['count']
	minim = counts['min_comments']['count']
	# donut info
	total_pos = len(data['POS_messages'])
	total_neu = len(data['NEU_messages'])
	total_neg = len(data['NEG_messages'])




# --- CARDS

with st.container():
	col1, col2, col3, col4 = st.columns(4)
	
	col1.image('../img/user.png', width=50)
	col1.metric("Users", users)
	
	col2.image('../img/chat.png', width=50)
	col2.metric("Comments", count)
	
	col3.image('../img/bubble-chat.png', width=50)
	col3.metric("Average Comments per Minute", count // total_minutes)
	
	col4.metric("Max Comments per Minute", maxim)
	col4.metric("Min Comments per Minute", minim)

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
		options = donut_option(total_pos, total_neg, total_neu)
		st.markdown('### Sentiment Analysis')
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

available_lines = list(colors.keys())
selected_lines = st.multiselect('Select lines to display:', available_lines, default=available_lines)

if selected_lines == []:
	selected_lines = available_lines

for sent in sents:
	sent_df = df[df['sentiment_analysis'] == sent]
	message_count = sent_df.groupby('timestamp').size().reset_index(name='count')
	messages_per_sentiment[sent] = message_count.set_index('timestamp')['count']
	
final_df = pd.DataFrame(messages_per_sentiment)

filtered_df = final_df[selected_lines]

filtered_colors = [colors[line] for line in selected_lines]
	

with st.container():
	st.markdown('### Messages per Minute')
	st.line_chart(filtered_df, 
                use_container_width=True,
				color=filtered_colors)