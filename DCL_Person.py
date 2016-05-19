import random
import DCL_Personality as Personality

class Person(object):
    def __init__(self, model, location = None, friends_affinity = 5, enemies_affinity = -5,
                 personality = None):
        self.affinity_map = {}
        self.friends = []
        self.enemies = []
        self.friends_affinity = friends_affinity
        self.enemies_affinity = enemies_affinity
        self.previous_post_seen = None
        self.personality = personality
        self.model = model

        if location is None:
            self.location = (random.randint(-180, 180), random.randint(-80, 80))

    def take_turn(self):
        # decide to create a post or not
        self.decay_relationships()
        pass

    def create_post(self):
        if self.personality is None:
            # No personality, do nothing
            pass
        else:
            post = self.personality.create_post()
            if post is not None:
                self.dispatch_post(post)

    def process_post(self, message):
        if message != self.previous_post_seen and message.creator not in self.enemies:
            self.previous_post_seen = message
            if self.personality is None:
                pass
            else:
                affinity_delta = self.personality.process_post(message)
                if message.poster in self.affinity_map:
                    self.affinity_map[message.poster] += affinity_delta
                else:
                    self.affinity_map[message.poster] = affinity_delta

                poster_affinity = self.affinity_map[message.poster]
                if poster_affinity >= self.friends_affinity:
                    if message.poster not in self.friends:
                        self.friends.add(messsage.poster)
                elif poster_affinity <= self.enemies_affinity:
                    if message.poster not in self.enemies:
                        self.enemies.add(messsage.poster)
        else:
            # ignore message
            pass

    def dispatch_post(self, post):
        for friend in self.friends:
            friend.process_post(post)

    def decay_relationships(self):
        """
        Reduces the amount of like/dislike for people who are not friends or unfriended,
        in that way over time, people "forget about" people that they don't really know well
        :return: nothing
        """
        affect_magnitude = 0.95 # these settings need to be moved somewhere more centalized
        removal_thresh = 0.05

        known_people = self.affinity_map.keys()
        people_to_affect = [x for x in known_people if known_people not in self.friends
                            and known_people not in self.enemies]

        for person in people_to_affect:
            self.affinity_map[person] *= affect_magnitude
            if abs(self.affinity_map[person]) < removal_thresh:
                del self.affinity_map[person]