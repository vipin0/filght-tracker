"""This module provide all the main functionalities for the 
slack bot like routing and handlling the events.
"""

import os
from slack import WebClient
from flask import Flask,request, Response
from dotenv import load_dotenv
from slackeventsapi import SlackEventAdapter
from utils.flights import parse_query, parse_tracking_query


load_dotenv()


app = Flask(__name__)
slack_event_apapter = SlackEventAdapter(
                        os.environ.get('SLACK_SIGNING_SECRET'),'/slack/events',app)

client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))

BOT_ID = client.api_call('auth.test',)['user_id']

@app.route("/")
def index():
    return "Hey There! I'm FlightBot."

@app.route('/help',methods=['POST'])
def help():
    """route function for the help endpoint.
    """
    data = request.form
    # print(data)
    channel_id = data.get('channel_id')
    # print(channel_id)
    
    help_text = """
        Use the following */commands*.
        /search_fight *origin_code* *destination_code* *[YYYY-MM-DD]* *[no_passengers]* *[class]* 
            You must provide origin airport code and destination airport code.
            default search date to today\'s date.
            default no_passengers is 1
            default class is \'E\' or you can use \'B\'.\n
        /list_arrivals *airport_code* *[begintime]* *[endtime]*
            endtime and begintime must be in format like 2021-12-12\n
        /list_departures *airport_code* *[begintime]* *[endtime]*
            endtime and begintime must be in format like 2021-12-12\n
        /help to see this help menu.
        """
    client.chat_postMessage(channel=channel_id,text=help_text)
    return Response(), 200


@app.route('/search_flight',methods=['POST'])
def get_flights():
    """route function for the get_flights endpoint.
    """
    data = request.form
    # print(data)
    channel_id = data.get('channel_id')
    user_id = data.get('user_id')
    query = data.get('text').split(" ")
    if len(query)>=2:
        client.chat_postEphemeral(channel=channel_id,user=user_id,text="Your request is being processed!")
        flights = parse_query(query)
        client.chat_postMessage(channel=channel_id,text=flights)
    else:
        client.chat_postMessage(channel=channel_id,text="Please provide correct Origin and Destination Airport code.")

    return Response(), 200

@app.route('/list_arrivals',methods=['POST'])
def list_arrivals():
    """route function for the list_arrivals endpoint.
    """
    data = request.form
    # print(data)
    channel_id = data.get('channel_id')
    user_id = data.get('user_id')
    query = data.get('text').split(",")
    # print("function:,",data.get('text'))
    if len(query)>=1:
        client.chat_postEphemeral(channel=channel_id,user=user_id,text="Your request is being processed!")
        flights = parse_tracking_query("arrival",query)
        client.chat_postMessage(channel=channel_id,text=flights)
    else:
        client.chat_postMessage(channel=channel_id,text="Please provide correct Airport name or code.")

    return Response(), 200
    

@app.route('/list_departures',methods=['POST'])
def list_departures():
    """route function for the list_departures endpoint.
    """
    data = request.form
    # print(data)
    channel_id = data.get('channel_id')
    user_id = data.get('user_id')
    query = data.get('text').split(" ")
    if len(query)>=1:
        client.chat_postEphemeral(channel=channel_id,user=user_id,text="Your request is being processed!")
        flights = parse_tracking_query("departure",query)
        client.chat_postMessage(channel=channel_id,text=flights)
    else:
        client.chat_postMessage(channel=channel_id,text="Please provide correct Airport name or code.")

    return Response(), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get('PORT',3000)),debug=True)