import random
import DCL_Post as Post

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

        like_total = self.facets.process_post(message, like_total)
        self.model.logger.log(0, "%r had reaction of %d to %r" % (self.person, like_total, message))
        self.repost_decide(message)
        return like_total

    def create_post(self):
        # just one topic for now
        keys = list(self.interests.keys())
        post_topic = [self.interests[keys[random.randint(0, len(keys)-1)]],]
        return Post.Post(self.person, post_topic)
        # to be implemented once post object exists

    def repost_decide(self, message):
        # just repost everything liked in this implementation
        self.person.dispatch_post(message)





class PersonalityFacet(object):
    """
    Decorator design pattern to allow arbitrary number of personality "facets" that can manipulate the
    end result of how much a post is liked or disliked
    """
    def __init__(self, next_facet = None):
        self.next_facet = next_facet

    def process_post(self, message, current_score):
        if self.next_facet is None:
            return current_score
        return (self.next_facet.process_post(message))

    def return_result(self, message, current_score):
        if self.next_facet is None:
            return current_score
        return (self.next_facet.process_post(message))


class LikesEveryOddTopicNumber(PersonalityFacet):
    def process_post(self, message, current_score):
        for topic in message.topics:
            if topic % 2 == 1:
                current_score += 1
        return self.return_result(message, current_score)

class LikesEveryEvenTopicNumber(PersonalityFacet):
    def process_post(self, message, current_score):
        for topic in message.topics:
            if topic % 2 == 0:
                current_score += 1
        return self.return_result(message, current_score)