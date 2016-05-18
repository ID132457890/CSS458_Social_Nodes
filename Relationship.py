class Relationship(object):
    senderID = 1234567890
    strength = 1.0
    
class Friend(Relationship):
    
    def __init__(self, senderID):
        self.senderID = senderID
        
class IgnoredPerson(Relationship):
    
    def __init__(self, senderID):
        self.senderID = senderID