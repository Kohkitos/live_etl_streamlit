def donut_option(pos, neg, neu):
    """_summary_

    Args:
        pos (int): amount of positive messages.
        neg (int): amount of negative messages.
        neu (int): amount of neutral messages.

    Returns:
        _type_: _description_
    """

    if pos == 0:
        data = [
                {"value": len(pos), "name": "NEG", "itemStyle": {"color": '#ff6961'}},
                {"value": len(neg), "name": "NEU", "itemStyle": {"color": '#fdfd96'}}
                ],
    elif neg == 0:
        data = [
                {"value": len(pos), "name": "NEG", "itemStyle": {"color": '#ff6961'}},
                {"value": len(neu), "name": "POS", "itemStyle": {"color": '#77dd77'}}
                ],
    elif neu == 0:
        data = [
                {"value": len(pos), "name": "NEG", "itemStyle": {"color": '#ff6961'}},
                {"value": len(neg), "name": "NEU", "itemStyle": {"color": '#fdfd96'}}
                ],
    else:
        data = [
                {"value": len(pos), "name": "NEG", "itemStyle": {"color": '#ff6961'}},
                {"value": len(neg), "name": "NEU", "itemStyle": {"color": '#fdfd96'}},
                {"value": len(neu), "name": "POS", "itemStyle": {"color": '#77dd77'}}
                ],

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