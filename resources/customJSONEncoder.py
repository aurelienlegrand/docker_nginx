from flask.json import JSONEncoder
from node import Node
from application import Application

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Node):
            return {
                'node_id' : obj.node_id,
                'image' : obj.image,
                'ip_addr' : obj.ip_addr
            }
	if isinstance(obj, Application):
	    return {
	    	'name' : obj.name,
                'nb_nodes' : obj.nb_nodes
	    }
        return super(JSONEncoder, self).default(obj)

