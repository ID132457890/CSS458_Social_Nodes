import random

class Personality(object):
    def __init__(self, person, model, generator = random_personality_generator):
        self.interests = {}
        self.disinterests = {}
        self.person = person
        (self.interests, self.disinterests) = generator(self, model)

    def process_post(self, message):
        pass
        # to be implemented once post object exists

    def create_post(self):
        pass
        # to be implemented once post object exists

def random_personality_generator(personality, model):
    num_of_topics = model.topics

    # both of these need to sum to <= 1
    prob_to_like = .1
    prob_to_dislike = .1

    amount_to_like_dislike = (1,5)

    for x in range(num_of_topics):
        like = random.random()
        if like < prob_to_like:
            personality.interests[x] = random.randint(amount_to_like_dislike[0], amount_to_like_dislike[1])
        elif like < prob_to_dislike + prob_to_like:
            personality.disinterests[x] = random.randint(amount_to_like_dislike[0], amount_to_like_dislike[1])
        else:
            pass

class PersonalityFacet(object):
    """
    Decorator design pattern to allow arbitrary number of personality "facets" that can manipulate the
    end result of how much a post is liked or disliked
    """
    def __init__(self, next_facet):
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
        # if message has an odd topic number in it... current_score += 1
        self.return_result(message, current_score)