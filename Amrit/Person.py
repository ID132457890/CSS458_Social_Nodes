import numpy as N

import Personality as PT
import Visualizer as V
import PersonsManager as PM
import Post as PO
import Variables as VR

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
    online = False
    
    personality = None
    
    connectedPeople = {}
    friendsList = {}
    ignoredList = {}
    
    allPosts = []
    receivedPosts = []
    
    def __init__(self, position, ID=0, friends=None):
        self.position = position
        
        randomScales = N.random.randint(VR.MIN_TOPIC_VALUE, VR.MAX_TOPIC_VALUE, size=VR.NUM_OF_TOPICS)
        
        topics = {}
        for index in range(VR.NUM_OF_TOPICS):
            topics[index + 1] = randomScales[index]
            
        self.personality = PT.Introvert(topics=topics)
        self.ID = ID
        
    def getFriends(self):
        friends = []
        
        for personID in self.connectedPeople.keys():
            if self.connectedPeople[personID] >= VR.FRIEND_LIMIT:
                friends.append(personID)
                
        return friends
        
    def getEdges(self):
        edges = []
        
        for personID in self.connectedPeople:
            person = PM.PersonsManager.sharedManager.getPersonFromID(personID)
            
            edge = {(self, person): self.connectedPeople[personID]}
            edges.append(edge)
            
        return edges
        
    def evaluatePost(self, post):
        if (post.senderID != self.ID) and (post in self.allPosts) == False:
            sender = PM.PersonsManager.sharedManager.getPersonFromID(post.senderID)
            self.allPosts.append(post)
            
            if ((post.senderID in self.connectedPeople) == False) or ((post.senderID in self.connectedPeople) and \
                self.connectedPeople[post.senderID] > VR.ENEMY_LIMIT):
                self.receivedPosts.append(post)
        
                likeness = self.personality.evaluatePost(self, post)
        
                if post.senderID in self.connectedPeople:
                    self.connectedPeople[post.senderID] += likeness
                else:
                    self.connectedPeople[post.senderID] = likeness
            
                PM.PersonsManager.sharedManager.startOnline(person=self)
        
                V.Visualizer.sharedVisualizer.connect(self, sender, self.connectedPeople[post.senderID])
        
    def sharePosts(self):
        for post in list(self.receivedPosts):
            if self.personality.shouldSharePost():
                PM.PersonsManager.sharedManager.sharePost(post, self.getFriends())
                self.receivedPosts.remove(post)
        
    def createPost(self):
        if self.personality.shouldCreatePost():
            chosenTopics = []
            
            for key in self.personality.topics:
                if self.personality.topics[key] > 0:
                    chosenTopics.append(key)
            
            post = PO.Post(chosenTopics, self.ID)
            PM.PersonsManager.sharedManager.broadcastPost(post)
            
            self.allPosts.append(post)