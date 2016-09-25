from flask import Flask
from flask.ext import restful
from flask.ext.restful import (reqparse, abort, fields, marshal_with, marshal, Api)
from flask_restful_swagger import swagger
import requests
import json

app = Flask(__name__)

###################################
api = swagger.docs(Api(app), apiVersion='0.1')
###################################

# Currently localhost, add in configuration file
docker_host = "127.0.0.1"

CONTAINERS = []

def update_containers():
    r = requests.get('http://' + docker_host + ':2375/containers/json')
    print(json.loads(r.content))
    CONTAINERS = r.content

class Webserver(restful.Resource):
    "Describing a webserver node"
    @swagger.operation(
            notes='Get a webserver node by id'
    )
    def get(self, node_id):
        if not(len(CONTAINERS) > node_id > 0) or CONTAINERS[node_id] is None:
            abort(404, message="Node {} doesn't exist".format(node_id))
        return CONTAINERS[node_id]

    def delete(self, node_id):
        if not(len(CONTAINERS) > node_id > 0):
            abort(404, message="Node {} doesn't exist".format(node_id))
        CONTAINERS[node_id] = None
        return "", 204

class WebserverList(restful.Resource):
    "Describing the list of webserver nodes"
    @swagger.operation(
            notes='Get the list of webserver nodes'
    )
    def get(self):
        update_containers()
        return CONTAINERS

api.add_resource(Webserver, '/webserver/<int:node_id>')
api.add_resource(WebserverList, '/webservers')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
