from flask import (Flask, make_response, request)
from flask_restful import (Resource, abort, Api)
from flask_restful_swagger import swagger
import requests
import json
from resources.node import (Node, NodeJSONEncoder)

app = Flask(__name__)

###################################
api = swagger.docs(Api(app), apiVersion='0.1')
###################################

# Currently localhost, add in configuration file
docker_host = "127.0.0.1"

containers = {}

def update_containers():
    r = requests.get('http://' + docker_host + ':2375/containers/json')
    print(json.loads(r.content))
    data = json.loads(r.content)
    for node in data:
        container = Node(node["Id"], node["Image"], node["NetworkSettings"]["Networks"]["bridge"]["IPAddress"])
        containers[container.node_id] = container

def new_node(image):
    payload = {'Image': image}
    r_create = requests.post('http://' + docker_host + ':2375/containers/create', json=payload)

    data = json.loads(r_create.content)
    if "Id" in data:
        node_id = data["Id"][:12]
        r_start = requests.post('http://' + docker_host + ':2375/containers/' + node_id + '/start')

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

    @swagger.operation(
            notes='Create a new webserver node'
    )
    def put(self):
        image = request.form['image']
        new_node(image)
        return {'created': 'ok'}

    def delete(self, node_id):
        if not node_id in containers:
            abort(404, message="Node {} doesn't exist".format(node_id))
        del containers[node_id]
        return "", 204

class WebserverList(Resource):
    "Describing the list of webserver nodes"
    @swagger.operation(
            notes='Get the list of webserver nodes'
    )
    def get(self):
        update_containers()
        return containers.values()

api.add_resource(Webserver, '/webserver/create', '/webserver/<string:node_id>')
api.add_resource(WebserverList, '/webservers')
api.representations.update({
    'application/json': node_json_output
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
