from flask import Flask
from flask_restful import (Resource, abort, Api)
from flask_restful_swagger import swagger
import requests
import json
from node import Node

app = Flask(__name__)

###################################
api = swagger.docs(Api(app), apiVersion='0.1')
###################################

# Currently localhost, add in configuration file
docker_host = "127.0.0.1"

containers = []

def update_containers():
    r = requests.get('http://' + docker_host + ':2375/containers/json')
    print(json.loads(r.content))
    data = json.loads(r.content)
    print("=================")
    for node in data:
        container = Node(node["Id"], node["Image"], node["NetworkSettings"]["Networks"]["bridge"]["IPAddress"])
        containers.append(container.to_json())

class Webserver(Resource):
    "Describing a webserver node"
    @swagger.operation(
            notes='Get a webserver node by id'
    )
    def get(self, node_id):
        update_containers()
        if not(len(containers) > node_id > 0) or containers[node_id] is None:
            abort(404, message="Node {} doesn't exist".format(node_id))
        return containers[node_id]

    def delete(self, node_id):
        if not(len(containers) > node_id > 0):
            abort(404, message="Node {} doesn't exist".format(node_id))
        containers[node_id] = None
        return "", 204

class WebserverList(Resource):
    "Describing the list of webserver nodes"
    @swagger.operation(
            notes='Get the list of webserver nodes'
    )
    def get(self):
        update_containers()
        return containers

api.add_resource(Webserver, '/webserver/<int:node_id>')
api.add_resource(WebserverList, '/webservers')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
