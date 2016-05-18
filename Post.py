from enum import Enum

class PostType(Enum):
    Nothing = 0
    Technology = 1
    Physics = 2
    Politics = 3
    Economics = 4
    #...
    
class PostTopics(object):
    primaryTopic = PostType.Nothing
    secondaryTopic = PostType.Nothing
    thirdTopic = PostType.Nothing

class Post(object):
    topics = PostTopics()
    senderID = 1234567890
    
    like = True
    
    def __init__ (self, topics, senderID):
        self.topics = topics
        self.senderID = senderID
        
    