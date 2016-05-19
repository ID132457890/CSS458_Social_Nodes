import numpy as N

import Personality as PT
import Visualizer as V
import PersonsManager as PM

from Post import Post

class Position(object):
    x = 0.0
    y = 0.0
    
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y
        
    def toTouple(self):
        return (self.x, self.y)
        
    def distanceFrom(self, position):
        return N.sqrt((position.x - self.x)**2 + (position.y - self.y)**2)

class Person(object):
    ID = 0
    position = Position()
    
    personality = None
    
    connectedPeople = {}
    friendsList = {}
    ignoredList = {}
    
    def __init__(self, position, ID=0, friends=None):
        self.position = position
        self.personality = PT.Personality()
        self.ID = ID
        
    def evaluatePost(self, post):
        likeness = self.personality.evaluatePost(self, post)
        
        if post.senderID in self.connectedPeople:
            self.connectedPeople[post.senderID] += likeness
        else:
            self.connectedPeople[post.senderID] = likeness
        
        sender = PM.PersonsManager.sharedManager.getPersonFromID(post.senderID)
        V.Visualizer.sharedVisualizer.connect(self, sender, self.connectedPeople[post.senderID])
        
    def createPost(self):
        post = Post([1,2], self.ID)
        PM.PersonsManager.sharedManager.broadcastPost(post)