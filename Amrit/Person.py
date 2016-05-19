import numpy as np

class Position(object):
    x = 0.0
    y = 0.0
    
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

class Person(object):
    identifier = 0
    position = Position()
    
    connectedPeople = {}
    friendsList = {}
    ignoredList = {}
    
    def __init__(self, position, friends=None):
        self.position = position
        
    def likePost():
        pass
        
    def createPost():
        return "do something"
        
    def sendPost():
        return "ds"