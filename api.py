from flask import Flask, request
from flask_restful import Resource, Api
from flask_restful import reqparse

app = Flask(__name__)
api = Api(app)

VERIFY_TOKEN = 'i_love_python'


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


# app.get('/webhook', function(req, res) {
#   if (req.query['hub.mode'] === 'subscribe' &&
#       req.query['hub.verify_token'] === <VERIFY_TOKEN>) {
#     console.log("Validating webhook");
#     res.status(200).send(req.query['hub.challenge']);
#   } else {
#     console.error("Failed validation. Make sure the validation tokens match.");
#     res.sendStatus(403);          
#   }  
# });


class BotAPI(Resource):
    def get(self):
        args = request.args
        if args['hub.mode'] == 'subscribe' and args['hub.verify_token'] == VERIFY_TOKEN:
            print('Validating webhook...')
            return int(args['hub.challenge'])
        else:
            print('Failed validation')
            return {error: '403'}

    def post(self):
        pass

api.add_resource(HelloWorld, '/')
api.add_resource(BotAPI, '/webhook')
if __name__ == '__main__':
    app.run(debug=True)