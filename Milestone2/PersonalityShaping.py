import Personality
import random

def static_introvert_personalities_who_like_distant_people(model):
    for agent in model.agents:
        agent.personality.repost_probability = 0.1
        agent.personality.post_probability = 0.1
        agent.personality.fame = 0
        agent.personality.probability_read_reposts = 0.5
        #agent.interests = {1: 5, 2: -5}
        agent.personality.facets = Personality.LovesPeopleInOppositeHemisphere()

def static_extrovert_personalities_who_like_distant_people(model):
    for agent in model.agents:
        agent.personality.repost_probability = 0.9
        agent.personality.post_probability = 0.9
        agent.personality.fame = 70
        agent.personality.probability_read_reposts = 0.8
        #agent.interests = {1: 5, 2: -5}
        agent.personality.facets = Personality.LovesPeopleInOppositeHemisphere()

def set_intovert_extrovert_traits(model):
    if not model.extrovert_percentage:
        raise Exception ("Extrovert percentage must be set as model.extrovert_percentage to use this personality shaper.")
    extroverts = model.extrovert_percentage
    for x in range(len(model.agents)):
        agent = model.agents[x]
        if x < extroverts * len(model.agents) / 100:
            agent.personality.repost_probability = (random.random() * .5) + 0.5
            agent.personality.post_probability = (random.random() * .5) + 0.5
            agent.personality.fame = 100 if random.random() < .80 else agent.personality.fame
            agent.personality.probability_read_reposts = (random.random() * .5) + 0.3
        else:
            agent.personality.repost_probability = random.random() * .5
            agent.personality.post_probability = random.random() * .3
            agent.personality.fame = 100 if random.random() < .95 else agent.personality.fame
            agent.personality.probability_read_reposts = random.random() * .3