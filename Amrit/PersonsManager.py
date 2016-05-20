import numpy as N
import Visualizer as V
import Person as PE
import Variables as VR

class PersonsManager(object):
    sharedManager = None
    
    increasingID = 0
    
    people = []
    posts = []
    
    @staticmethod
    def createManager():
        PersonsManager.sharedManager = PersonsManager()
    
    def addPerson(self, position):
        person = PE.Person(PE.Position(position.x, position.y), ID=self.increasingID)
        
        self.people.append(person)
        self.increasingID += 1
        
        V.Visualizer.sharedVisualizer.addNode(person)
        
    def getPersonFromID(self, personID):
        for person in self.people:
            if person.ID == personID:
                return person
                
        return None
        
    def startOnline(self, person=None):
        if person == None:
            randomIndexes = N.random.randint(len(self.people))
        
            for i in range(len(self.people)):
                if i in randomIndexes:
                    self.people[i].online = True
        else:
            for aPerson in self.people:
                if person.position.distanceFrom(aPerson.position) <= VR.NEIGHBOUR_DISTANCE:
                    aPerson.online = True
        
    def startSending(self):
        for person in self.people:
            if person.online == True:
                person.createPost()
        
    def broadcastPost(self, post):
        for person in self.people:
            if person.ID != post.senderID:
                person.evaluatePost(post)
            
        self.posts.append(post)
        
    def sharePost(self, post, people):
        for person in self.people:
            if person.ID in people:
                person.evaluatePost(post)