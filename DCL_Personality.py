import random
import DCL_Post as Post
import Model

def random_personality_generator(personality, model):
    num_of_topics = model.topics

    likemap = {}
    # both of these need to sum to <= 1
    prob_to_like = .1
    prob_to_dislike = .1

    amount_to_like_dislike = (1,5)

    for x in range(num_of_topics):
        like = random.random()
        amount = random.randint(amount_to_like_dislike[0], amount_to_like_dislike[1])
        if like < prob_to_like:
            likemap[x] = amount
        elif like < prob_to_dislike + prob_to_like:
            amount *= -1
            likemap[x] = amount
        else:
            pass

    return likemap

def random_facets(personality, model):
    options = (eval('PersonalityFacet.__subclasses__()'))
    selected = []
    num_to_select = len(options) / 2
    while len(selected) < num_to_select:
        for option in options:
            if random.random() < .5 and len(selected) < num_to_select:
                selected.append(option)

    model.logger.log(1, "%r has gained personality facets %r" % (personality.person, selected))
    selected[len(selected)-1] = selected[len(selected)-1]()
    for x in range(len(selected)-2, -1, -1):
        selected[x] = selected[x](selected[x+1])
    return selected[0]

class Personality(object):
    def __init__(self, person, model, generator = random_personality_generator,
                 facet_generator = random_facets):
        self.person = person
        self.interests = generator(self, model)
        self.facets = facet_generator(self, model)
        self.model = model

    def process_post(self, message):
        like_total = 0

        for topic in message.topics:
            if topic in self.interests:
                like_total += self.interests[topic]

        like_total = self.facets.process_post(message, like_total, self.person)
        self.model.logger.log(0, "%r had reaction of %d to %r" % (self.person, like_total, message))
        self.repost_decide(message)
        return like_total

    def create_post(self):
        if random.random() < .2:
            keys = list(self.interests.keys())
            post_topic = []
            # randomly 1 to 4 topics
            for x in range(random.randint(0, 4)):
                post_topic.append(self.interests[keys[random.randint(0, len(keys)-1)]])
            return Post.Post(self.person, post_topic)


    def repost_decide(self, message):
        # just repost 20% for now
        if random.random() < .2:
            self.person.dispatch_post(message)





class PersonalityFacet(object):
    """
    Decorator design pattern to allow arbitrary number of personality "facets" that can manipulate the
    end result of how much a post is liked or disliked
    """
    def __init__(self, next_facet = None):
        self.next_facet = next_facet

    def process_post(self, message, current_score, person):
        if self.next_facet is None:
            return current_score
        return self.return_result(message, current_score, person)

    def return_result(self, message, current_score, person):
        if self.next_facet is None:
            return current_score
        return self.next_facet.return_result(message, current_score, person)


class LikesEveryOddTopicNumber(PersonalityFacet):
    def process_post(self, message, current_score, person):
        for topic in message.topics:
            if topic % 2 == 1:
                current_score += 5
        return self.return_result(message, current_score, person)

class LikesEveryEvenTopicNumber(PersonalityFacet):
    def process_post(self, message, current_score, person):
        for topic in message.topics:
            if topic % 2 == 0:
                current_score += 5
        return self.return_result(message, current_score, person)

class LikesClosePeople(PersonalityFacet):
    def process_post(self, message, current_score, person):
        distance = Model.find_distance(person, message.sender)
        if distance < 2000 and current_score > 0:
            current_score *= 3 if current_score > 0 else 0.5
        return self.return_result(message, current_score, person)

class LikesDistantPeople(PersonalityFacet):
    def process_post(self, message, current_score, person):
        distance = Model.find_distance(person, message.sender)
        if distance > 2000 and current_score > 0:
            current_score *= 3 if current_score > 0 else 0.5
        return self.return_result(message, current_score, person)

class HatesPeopleInOppositeHemisphere(PersonalityFacet):
    def process_post(self, message, current_score, person):
        if person.location[0] * message.sender.location[0] < 0:
            current_score += - 10
        if person.location[1] * message.sender.location[1] < 0:
            current_score += - 10
        return self.return_result(message, current_score, person)

class LovesPeopleInOppositeHemisphere(PersonalityFacet):
    def process_post(self, message, current_score, person):
        if person.location[0] * message.sender.location[0] < 0:
            current_score += 20
        if person.location[1] * message.sender.location[1] < 0:
            current_score += 20
        return self.return_result(message, current_score, person)