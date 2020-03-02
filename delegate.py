class delegate(object):
    def __init__(self, name, delegation):
        self.name = name
        self.delegation = delegation
    def findFlag(self, delegation):
        return(determineFlag(self.delgation))