import random

class Person(object):
    def __init__(self, location = None, friends_affinity = 5, enemies_affinity = -5,
                 personality = None):
        self.affinity_map = {}
        self.friends = []
        self.enemies = []
        self.friends_affinity = friends_affinity
        self.enemies_affinity = enemies_affinity
        self.previous_post_seen = None
        self.personality = personality

        if location is None:
            self.location = (random.randint(-180, 180), random.randint(-80, 80))

    def take_turn(self):
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

        else:
            # ignore message
            pass

    def dispatch_post(self, post):
        for friend in self.friends:
            friend.process_post(post)