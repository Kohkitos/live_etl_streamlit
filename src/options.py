from api import *

def donut_option(pos, neg, neu):
    """Sets up the options for the donut diagram according to the sentiment anlysis required.

    Args:
        pos (int): amount of positive messages.
        neg (int): amount of negative messages.
        neu (int): amount of neutral messages.

    Returns:
        _type_: _description_
    """

    if pos == 0:
        data = [
                {"value": neg, "name": "NEG", "itemStyle": {"color": '#ff6961'}},
                {"value": neu, "name": "NEU", "itemStyle": {"color": '#fdfd96'}}
                ]
    elif neg == 0:
        data = [
                {"value": neu, "name": "NEU", "itemStyle": {"color": '#fdfd96'}},
                {"value": pos, "name": "POS", "itemStyle": {"color": '#77dd77'}}
                ]
    elif neu == 0:
        data = [
                {"value": neg, "name": "NEG", "itemStyle": {"color": '#ff6961'}},
                {"value": pos, "name": "POS", "itemStyle": {"color": '#77dd77'}}
                ]
    else:
        data = [
                {"value": neg, "name": "NEG", "itemStyle": {"color": '#ff6961'}},
                {"value": neu, "name": "NEU", "itemStyle": {"color": '#fdfd96'}},
                {"value": pos, "name": "POS", "itemStyle": {"color": '#77dd77'}}
                ]

    options = {
            "tooltip": {"trigger": "item"},
            "series": [
                {
                    "name": "Sentiment",
                    "type": "pie",
                    "radius": ["25%", "65%"],
                    "data": data,
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
    
    return options

class web_data():

    def __init__(self, sent, start_15 = -1, start_16 = -1, end_15 = -1, end_16 = -1):  
        """Object initiation.

        Args:
            sent (string): a string with the sentiments to check.
            start_15 (int): Start timestamp of day 15. Defaults to -1.
            start_16 (int): Start timestamp of day 16. Defaults to -1.
            end_15 (int): End timestamp of day 15. Defaults to -1.
            end_16 (int, optional): End timestamp of day 16. Defaults to -1.
        """

        # Check if we want both days or one
        if start_16 <= 0:
            self.days = 0
            start, end = start_15, end_15

        elif start_15 <= 0:
            self.days = 0
            start, end = start_16, end_16

        else:
            self.days = 1

        # if both days are imputed
        if self.days:
            total_minutes_15 = end_15 - start_15
            total_minutes_16 = end_16 - start_16
            # data for later
            self.total_minutes = total_minutes_15 + total_minutes_16
            self.data_15 = message_15(f"{sent}-{start_15}-{end_15}")
            self.data_16 = message_16(f"{sent}-{start_16}-{end_16}")
            # cards info
            self.users = self.data_15['users'] + self.data_16['users']
            self.count = self.data_15['count'] + self.data_16['count']
            counts_15 = max_min_comments(start_15, end_15)
            counts_16 = max_min_comments(start_16, end_16)
            self.maxim = max(counts_15['max_comments']['count'], counts_16['max_comments']['count'])
            self.minim = min(counts_15['min_comments']['count'], counts_16['min_comments']['count'])
            # donut info and data for table and line plot
            ## Initiate a dictionary with -1 meaning there are none
            self.message_count = {'POS': -1, 'NEU': -1, 'NEG': -1}
            self.data = {'POS_messages': -1, 'NEU_messages': -1, 'NEG_messages': -1}
            # for pos
            if len(self.data_15['POS_messages']) >= 0 or len(self.data_16['POS_messages']) >= 0:
                self.message_count['POS'] = len(self.data_15['POS_messages']) + len(self.data_16['POS_messages'])
                self.data['POS_MESSAGES'] = self.data_15['POS_messages'] + self.data_16['POS_messages']
            # for neu
            if len(self.data_15['NEU_messages']) >= 0 or len(self.data_16['NEU_messages']) >= 0:
                self.message_count['NEU'] = len(self.data_15['NEU_messages']) + len(self.data_16['NEU_messages'])
                self.data['NEU_messages'] = self.data_15['NEU_messages'] + self.data_16['NEU_messages']
            # for neg
            if len(self.data_15['NEG_messages']) >= 0 or len(self.data_16['NEG_messages']) >= 0:
                self.message_count['NEG'] = len(self.data_15['NEG_messages']) + len(self.data_16['NEG_messages'])
                self.data['NEG_messages'] = self.data_15['NEG_messages'] + self.data_16['NEG_messages']
        else:
            # moviditas