import sys, json, requests
from flask import Flask, request
from google_places import get_attractions
import _thread

try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai

app = Flask(__name__)

PAT = 'EAAOoByh2huoBABpK8h9ZALdNo0yeR3SMjJjMfMeSv8EsN8vlIwPNKC9VefE7vQ2pMwkETdLaojp1RZBA04kfcupomXmgZChW7uZAzHQjfhZAFgn8TfgkM9tDcTwiq0rZCtrXY8utHFc2AX5uNAGvy8SI4pr7bmtDVl8PU02NQVc7dZBB5625FHk'

CLIENT_ACCESS_TOKEN = '209db766ffbe4f608f45dcb0ce970bc1'

VERIFY_TOKEN = 'tinuade'

ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

@app.route('/webhook', methods=['GET'])
def handle_verification():
    '''
    Verifies facebook webhook subscription
    Successful when verify_token is same as token sent by facebook app
    '''
    if (request.args.get('hub.verify_token', '') == VERIFY_TOKEN):     
        print("succefully verified")
        return request.args.get('hub.challenge', '')
    else:
        print("Wrong verification token!")
        return "Wrong validation token"


@app.route('/webhook', methods=['POST'])
def handle_message():
    '''
    Handle messages sent by facebook messenger to the applicaiton
    '''
    data = request.get_json()

    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  
                    sender_id = messaging_event["sender"]["id"]        
                    recipient_id = messaging_event["recipient"]["id"]  
                    message_text = messaging_event["message"]["text"]
                    reply = parse_user_message(message_text)
                    send_message_response(sender_id, reply) 

    return "ok"


def send_message(sender_id, message_text):
    '''
    Sending response back to the user using facebook graph API
    '''
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",

        params={"access_token": PAT},

        headers={"Content-Type": "application/json"}, 

        data=json.dumps({
        "recipient": {"id": sender_id},
        "message": {"text": message_text}
    }))


def parse_user_message(user_text):
    '''
    Send the message to API AI which invokes an intent
    and sends the response accordingly
    The bot response is appened with weaher data fetched from
    open weather map client
    '''
    
    request = ai.text_request()
    request.query = user_text

    response = json.loads(request.getresponse().read().decode('utf-8'))
    responseStatus = response['status']['code']
    if (responseStatus == 200):
        print("API AI response", response['result']['fulfillment']['speech'])
        api_response = response['result']
        attractions = None
        if not api_response['actionIncomplete']:
            try:
                location = api_response['parameters']['Location']
                attractions = get_attractions(location)
            except KeyError:
                pass

        response = api_response['fulfillment']['speech']
        if attractions:
            response += '. ' + attractions
        return response

def send_message_response(sender_id, message_text):

    sentenceDelimiter = ". "
    messages = message_text.split(sentenceDelimiter)
    
    for message in messages:
        send_message(sender_id, message)

if __name__ == '__main__':
    app.run()