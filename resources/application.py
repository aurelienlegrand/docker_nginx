class Application():
    """Describes an application: A name, a number of nodes (webservers), a threshold and a ratio
    When the threshold of connections is reached, the number of nodes requested is multiplied by the ratio"""
    def __init__(self, name, nb_nodes, threshold, ratio):
       self.name = name
       self.nb_nodes = nb_nodes
       self.threshold = threshold
       self.ratio = ratio

