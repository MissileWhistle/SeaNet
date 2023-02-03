# This is simply the class that defines a graph object

class node:
    def __init__(self, p):
        self.cord = p
        self.weight = None
        self.next = None