import Person as PE
import Post as PO
import PersonsManager as PM

MIN_SCALE = -5
MAX_SCALE = 5

class Personality(object):
    distancePreference = 0.25
    topicPreference = 0.25
    friendPreference = 0.25
    influencePreference = 0.25
    
    postPreference = 0.20
    
    maxDistance = 5
    topics = {1:3, 2:4}
    
    def __init__(self):
        pass
        
    def evaluatePost(self, person, post):
        sender = PM.PersonsManager.sharedManager.getPersonFromID(post.senderID)
        
        distanceLikeness = MIN_SCALE * self.distancePreference
        if person.position.distanceFrom(sender.position) <= self.maxDistance:
            distanceLikeness = MAX_SCALE * self.distancePreference
            
        topicLikeness = 0
        for key in post.topics:
            if key in self.topics:
                topicLikeness += self.topics[key]
                
        topicLikeness *= self.topicPreference
        
        return distanceLikeness + topicLikeness