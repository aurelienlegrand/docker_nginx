class Node:
    """Defines a Node (webserver or load balancer"""

    def __init__(self, node_id, image, ip_addr):
        self.node_id = node_id
        self.image = image
        self.ip_addr = ip_addr

    def to_json(self):
        return("'node_id': '" + self.node_id + "', 'image': '" + self.image + "', ip_addr: '" + self.ip_addr + "'")
