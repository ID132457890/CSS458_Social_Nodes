class Post(object):
    topics = [1, 2]
    senderID = 1234567890
    
    def __init__ (self, topics, senderID):
        self.topics = list(topics)
        self.senderID = senderID
        
    