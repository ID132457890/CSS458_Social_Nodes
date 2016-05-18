class Relationship(object):
    #Used to represent a person that is a friend or 
    #an ignored person
    
    personID = 1234567890
    strength = 1.0 #Used to check the strength of a friendship or ignore level
    
class Friend(Relationship):
    
    def __init__(self, personID):
        self.personID = personID
        
class IgnoredPerson(Relationship):
    
    def __init__(self, personID):
        self.personID = personID