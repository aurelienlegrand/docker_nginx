from flask.json import JSONEncoder

class Node:
    """Defines a Node (webserver or load balancer"""

    def __init__(self, node_id, image, ip_addr):
        self.node_id = node_id
        self.image = image
        self.ip_addr = ip_addr

    def to_json(self):
        return("'node_id': '" + self.node_id + "', 'image': '" + self.image + "', ip_addr: '" + self.ip_addr + "'")


class NodeJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Node):
            return {
                'node_id'     : obj.node_id,
                'image'     : obj.image,
                'ip_addr'     : obj.ip_addr
            }
        print("TEST")
        return super(JSONEncoder, self).default(obj)

