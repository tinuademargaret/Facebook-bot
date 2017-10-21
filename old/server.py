import apiai
CLIENT_ACCESS_TOKEN = '209db766ffbe4f608f45dcb0ce970bc1 '
PAGE_ACCESS_TOKEN = 'EAAOoByh2huoBABpK8h9ZALdNo0yeR3SMjJjMfMeSv8EsN8vlIwPNKC9VefE7vQ2pMwkETdLaojp1RZBA04kfcupomXmgZChW7uZAzHQjfhZAFgn8TfgkM9tDcTwiq0rZCtrXY8utHFc2AX5uNAGvy8SI4pr7bmtDVl8PU02NQVc7dZBB5625FHk'
VERIFY_TOKEN = 'tinuade'

ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
#GET request
@app.route('/', methods=['GET'])
def handle_verification():
    if (request.args.get('hub.verify_token', '') == VERIFY_TOKEN):
        print("Verified")
        return request.args.get('hub.challenge', '')
    else:
        print("Wrong token")
        return "Error, wrong validation token"
#POST request
@app.route('/', methods=['POST'])
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
                    send_message_response(sender_id, parse_natural_text(message_text))


    return "ok"def send_message(sender_id, message_text):
    '''
    Sending response back to the user using facebook graph API
    '''
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",

        params={"access_token": PAGE_ACCESS_TOKEN},

        headers={"Content-Type": "application/json"},

        data=json.dumps({
        "recipient": {"id": sender_id},
        "message": {"text": message_text}
    }))