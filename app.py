"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

import re
import string
import math
import sys
import random
import requests
from flask import Flask, request
from pymessenger import Bot

from PHQ9 import questions
from quotes import quotes

app = Flask(__name__)

ACCESS_TOKEN = "EAAEZBStZBVouoBAAGPECqOC5CZBCu7XzeNbc1draiRZArFjmuCeRG9TDPRZAYEyEvaYNagsEZAs46b7Y65qHXeTeo3rC9ZB3sPunaC03yeTbq5qMi3VsqgpZAmraIzL7CzKYCCCH4KHjMkTvCRZCnGm42Uxs1fiKKVjWqcVZCTFKfICgZDZD"
VERIFY_TOEKN = "hello"
bot = Bot(ACCESS_TOKEN)
arr = []

# we will get info about sender
@app.route('/', methods=['GET', 'POST'])
def verify():
    # webhook verification
    # these hubs are parameters of what is sent between FB and your code (with a value)
    # hub.mode always has value of subscribe, hub.challenge has int value, hub.verify has the verify token

    # if there is a get request where hub.mode == subscribe and also a hub.challenge get request (this int must be passed back to FB) (basically contact with FB)
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        # if FB does not send the verify_token, then mismatch in tokens
        if request.args.get("hub.verify_token") != VERIFY_TOEKN:
            return "Verification token mismatch", 403
        # since it is verify token, send back the hub.challenge
        return request.args["hub.challenge"], 200

    # if not GET then POST request
    # if post request (get a message so want to post to server), need to send message back to user
    else:
        # get json file from webhook that contains the data of message 
        data = request.get_json()
        #log(data)

        # format:
        # {'object': 'page', 
        #  'entry': [{'id': '100169205227335',
        #            'time': 1603411168137, 
        #            'messaging': [{'sender': {'id': '3304070599646311'}, 
        #                          'recipient': {'id': '100169205227335'}, 
        #                           'timestamp': 1603408810943, 
        #                           'message': {'mid': 'm_O1Kb5Hp0gTGPhbBlShVWo5goa2M_uXV7Qp7cInl0jtF5sREViZospMLVwOWJjIrDHzOSd2PNK5upa5AuLg7gqg', 
        #                                       'text': 'will'}}]}]}
        
        if data['object'] == 'page':
            # loop over list 'entry'
            for entry in data['entry']:
                # loop over list 'messaging' which is in list 'entry'
                for messaging_event in entry['messaging']:

                    # IDs
                    sender_id = messaging_event['sender']['id']
                    recipient_id = messaging_event['recipient']['id']

                    # if can get 'message' key when looping over list 'messaging' (if a message exists), return value of key
                    # and only send a response message if POST request sender is the user (multiple POST requests sent every time a message appears in messenger)
                    if messaging_event.get('message') and sender_id != '100169205227335':
                        # if there is a 'text' key or 'attachment' key
                        if messaging_event['message'].get('text'):
                            r = requests.get('https://graph.facebook.com/{}?fields=first_name,last_name,profile_pic&access_token={}'.format(sender_id, ACCESS_TOKEN)).json()
                            name = r['first_name']
                            # name = "test"

                            response_msg = get_message(messaging_event['message']['text'], name, arr)
                            bot.send_text_message(sender_id, response_msg)
                        else:
                            messaging_text = 'no text'
                    elif messaging_event.get('postback'):
                        received_postback(messaging_event)

        

        # complete a post request
        return "Message Processed", 200

# print message recieved back from FB in console
def log(message):
    print(message)
    # flush out buffer after each print so info prints all at once EACH TIME
    sys.stdout.flush()
    return "ok"

# return random sentence from imported list "joke"
def get_message(message, name, arr):
    # look for stuff in bracket (optional)
    if re.search("h(i|ello)?", message, re.IGNORECASE):
        arr.clear()
        return("Good Day, Master {}!\n\nI am here to assess your mental health as well as provide you with some words of wisdom at the end to enlighten your day. We will run through the the PHQ-9 Questionnaire (a series of 9 questions) to better understand your current situation (:\n\nIf you are ready to begin, respond with the phrase \"start\". Feel free to exit out of this survey by typing the word \"exit\" anytime during the survey\n\nOr if you would just like to receive a random quote, that's ok too! Just message me \"quote\"!".format(name))
    elif message == "start" and len(arr) == 0:
        arr.clear()
        return(questions[0])
    elif message == "quote" and len(arr) == 0:
        arr.clear()
        return("\"{}\"".format(random.choice(random.choice(quotes))))
    # if entry is a number
    elif message.isdigit() and len(arr) < 9:
        message = int(message)
        # check if num is between allowable nums
        if message in range(0,4):
            # see which question to ask next depending on size of array that stores input values
            for i in range(10):
                if len(arr) == i:
                    arr.append(message)
                    print(len(arr))
                    return(questions[i+1])
        else:
            return("Please enter a number between 0 and 3 inclusive")
        # after getting all the info needed
    elif message.isdigit() and len(arr) == 9:
        arr.append(int(message))
        if arr[9] in range(0,6):
            # sum the elements up until the 9th element (exclude mood)
            total = sum(arr[:9])
            # select random quote from provided mood
            quote = random.choice(quotes[arr[9]])
            return_message = "test"
            if total in range(0,5):
                return_message = ("{} Points\n\nScores <= 4 suggest minimal depression which may not require treatment. Functionally, the patient does not report limitations due to their symptoms\n\n\"{}\"".format(total, quote))
            elif total in range(5,10):
                return_message = ("{} Points\n\nScores 5-9 suggest mild depression which may require only watchful waiting and repeated PHQ-9 at followup. Functionally, the patient is “somewhat” having difficulty with life tasks due to their symptoms\n\n\"{}\"".format(total, quote))
            elif total in range(10, 15):
                return_message = ("{} Points\n\nScores 10-14 suggest moderate depression severity; patients should have a treatment plan ranging form counseling, followup, and/or pharmacotherapy. Functionally, the patient is “somewhat” having difficulty with life tasks due to their symptoms\n\n\"{}\"".format(total, quote))
            elif total in range(15, 20):
                return_message = ("{} Points\n\nScores 15-19 suggest moderately severe depression; patients typically should have immediate initiation of pharmacotherapy and/or psychotherapy. Functionally, the patient is “somewhat” having difficulty with life tasks due to their symptoms\n\n\"{}\"".format(total, quote))
            elif total >= 20:
                return_message = ("{} Points\n\nScores 20 and greater suggest severe depression; patients typically should have immediate initiation of pharmacotherapy and expedited referral to mental health specialist. Functionally, the patient is “somewhat” having difficulty with life tasks due to their symptoms\n\n\"{}\"".format(total, quote))
            if arr[8] != 0:
                return_message += "\n\nLooks like life is really tough for you right now. Please seek medical help immediately - life is too valuable and people love you too much for you to just throw it all away...\n\nCanada Suicide Prevention Service: 833-456-4566. SMS: Text START to 741741"
            arr.clear()
            return(return_message)
        else:
            return("Please enter a number between 0 and 5 inclusive")
    # exit prompt
    elif message == "exit":
        arr.clear()
        return("Good-bye! And just a reminder, you're gorgeous (:")
    else:
        arr.clear()
        return("Invalid Entry. Please start over by entering \"start\"")

    # arr.append(int(message))
    # return sum(arr) 

if __name__ == '__main__':
    app.run()
