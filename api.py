from flask import (Flask, make_response)
from flask_restful import (Resource, abort, Api)
from flask_restful_swagger import swagger
import requests
import json
from node import (Node, NodeJSONEncoder)

app = Flask(__name__)

###################################
api = swagger.docs(Api(app), apiVersion='0.1')
###################################

# Currently localhost, add in configuration file
docker_host = "127.0.0.1"

containers_list = []
containers = {}

def update_containers():
    r = requests.get('http://' + docker_host + ':2375/containers/json')
    print(json.loads(r.content))
    data = json.loads(r.content)
    print("=================")
    for node in data:
        container = Node(node["Id"], node["Image"], node["NetworkSettings"]["Networks"]["bridge"]["IPAddress"])
        containers_list.append(container.to_json())
        containers[container.node_id] = container

def node_json_output(data, code, headers=None):
    dumped = json.dumps(data, cls=NodeJSONEncoder)
    resp = make_response(dumped, code)
    resp.headers.extend(headers or {})
    return resp

class Webserver(Resource):
    "Describing a webserver node"
    @swagger.operation(
            notes='Get a webserver node by id'
    )
    def get(self, node_id):
        update_containers()
        if not node_id in containers:
            abort(404, message="Node {} doesn't exist".format(node_id))
        return containers[node_id]

    def delete(self, node_id):
        if not(len(containers_list) > node_id > 0):
            abort(404, message="Node {} doesn't exist".format(node_id))
        containers_list[node_id] = None
        return "", 204

class WebserverList(Resource):
    "Describing the list of webserver nodes"
    @swagger.operation(
            notes='Get the list of webserver nodes'
    )
    def get(self):
        update_containers()
        return containers.values()

api.add_resource(Webserver, '/webserver/<string:node_id>')
api.add_resource(WebserverList, '/webservers')
api.representations.update({
    'application/json': node_json_output
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
