from flask import Flask, request
from flask_restful import Resource, Api, reqparse, abort

app = Flask(__name__)
api = Api(app)

requests = []

parser = reqparse.RequestParser()
parser.add_argument('title', required=True, type=str)
parser.add_argument('location', required=True, type=str)
parser.add_argument('request_type', required=True)
parser.add_argument('description')


def find_request(request_id):
    """ Find a specific request resource based off the id """
    return [_request for _request in requests if _request['request_id'] == request_id]


class RequestList(Resource):
    def get(self):
        return {"requests": requests}, 200

    def post(self):
        args = parser.parse_args()
        request = {
            "request_id": requests[-1]["request_id"] + 1 if requests else 1,
            "title": args['title'],
            "location": args['location'],
            "request_type": args['request_type'],
            "description": args['description']
        }
        requests.append(request)
        return {"request": request}, 201


class Request(Resource):
    def get(self, request_id):
        """ Get a single request resource based off its id """
        request = find_request(request_id)
        if len(request) == 0:
            return {"message": f"request {request_id} doesn't exit."}, 404
        return {'request': request[0]}, 200

    def put(self, request_id):
        """ Update a single request resource based off its id """
        _request = find_request(request_id)
        if len(_request) == 0:
            return {"message": f"request {request_id} doesn't exit."}, 404
        _request[0]['title'] = request.json.get(
            'title', _request[0]['title'])
        _request[0]['location'] = request.json.get(
            'location', _request[0]['location'])
        _request[0]['request_type'] = request.json.get(
            'request_type', _request[0]['request_type'])
        _request[0]['description'] = request.json.get(
            'description', _request[0]['description'])

        return {"requests": requests}


api.add_resource(RequestList, '/api/v1/users/requests/')
api.add_resource(Request, '/api/v1/users/request/<int:request_id>/')
