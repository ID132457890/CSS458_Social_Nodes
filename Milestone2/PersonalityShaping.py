import Personality
import random

# basic way to set all agents to a specific type
#------------------
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

#------------------



# introduce some randomness within the range of categories
#------------------
def dynamic_extrovert_all(model):
    for agent in model.agents:
        dynamic_extrovert_agent(agent)

def dynamic_introvert_all(model):
    for agent in model.agents:
        dynamic_introvert_agent(agent)

def dynamic_extrovert_agent(agent):
    agent.personality.repost_probability = (random.random() * .5) + 0.5
    agent.personality.post_probability = (random.random() * .5) + 0.5
    agent.personality.fame = 100 if random.random() > .97 else agent.personality.fame
    agent.personality.probability_read_reposts = (random.random() * .5) + 0.3

def dynamic_introvert_agent(agent):
    agent.personality.repost_probability = random.random() * .5
    agent.personality.post_probability = random.random() * .3
    agent.personality.fame = 100 if random.random() > .99 else agent.personality.fame
    agent.personality.probability_read_reposts = random.random() * .3

#----------------
# Force personality facets
def clear_facets(agent):
    agent.personality.facets = None

def add_facet(agent, facet):
    facet_chain = agent.personality.facets
    agent.personality.facets = facet(next_facet=facet_chain)





#------------------
# Agent shaping for specific scenarios
#------------------
#
#
# This will set a certain percentage intovert, and a certain percentage extrovert
# Percent extrovert must be set to model.extrovert_percentage before run_simulation is called
#------------------
def set_intovert_extrovert_traits(model):
    if not model.extrovert_percentage:
        raise Exception ("Extrovert percentage must be set as model.extrovert_percentage to use this personality shaper.")
    extroverts = model.extrovert_percentage
    for x in range(len(model.agents)):
        agent = model.agents[x]
        if x < extroverts * len(model.agents) / 100:
            dynamic_extrovert_agent(agent)
        else:
            dynamic_introvert_agent(agent)

# This will allow you to set a certain percentage to a certain type and allow you to specify specific optional
# traits you want to be given to those ranges as well, for example, if you create this variable before running
# run_simulation, you'll get the expected mix:
"""
model.personality_shaping = {
    'ranges' : 'proportional',       # proportional (given as a percentage) or absolute agent numbers
                                     # if proportional is used, all must add to exactly 100%
                                     # if absolute is used, total count must equal size of model.agents
    'definitions': [(20, [PersonalityShaping.DynamicExtrovertAgent, PersonalityShaping.clear_facets,
                         (PersonalityShaping.add_facet, Personality.HatesPeopleWithFame),
                         (PersonalityShaping.add_facet, Personality.LikesDistantPeople]),
                    (80, [PersonalityShaping.DynamicExtrovertAgent, PersonalityShaping.clear_facets,
                         (PersonalityShaping.add_facet, Personality.HatesPeopleWithFame),
                         (PersonalityShaping.add_facet, Personality.LikesClosePeople)])]
}
Alternately, for the same effect using absolute numbering, this can be done (assuming 200 agents):
model.personality_shaping = {
    'ranges' : 'absolute',
    'definitions': [(40, [PersonalityShaping.DynamicExtrovertAgent, PersonalityShaping.clear_facets,
                         (PersonalityShaping.add_facet, Personality.HatesPeopleWithFame),
                         (PersonalityShaping.add_facet, Personality.LikesDistantPeople)]]),
                    (160, [PersonalityShaping.DynamicExtrovertAgent, PersonalityShaping.clear_facets,
                         (PersonalityShaping.add_facet, Personality.HatesPeopleWithFame),
                         (PersonalityShaping.add_facet, Personality.LikesClosePeople)])]
}

The ranges will be read in order, so the first definition will be applied to the lowest-indexed agents, and
the last defined group will be applied to the highest-indexed agents.
"""
def personality_shaping_flexible(model):
    if not model.personality_shaping:
        raise Exception("Shaping configuration must be bound to model.personality_shaping before running model.")
    shape = model.personality_shaping
    pro_idx = None
    if shape['ranges'] == 'proportional':
        pro_idx = True
    elif shape['ranges'] == 'absolute':
        pro_idx = False
    else:
        raise Exception("No indexing method specified in model.personality_shaping")

    shape_definitions = shape['definitions']
    current_index = 0
    cumulative_percent = 0
    for definition in shape_definitions:
        indexer, settings = definition
        if pro_idx == True:
            cumulative_percent += indexer
            if cumulative_percent > 100:
                raise Exception("Percent > 100%")
            elif cumulative_percent == 100:
                target_index = len(model.agents)-1
            else:
                target_index = current_index + (len(model.agents) * indexer / 100)
        else:
            target_index = current_index + indexer - 1
            if target_index >= len(model.agents):
                raise Exception("Agent count in definition exceeds number of agents in model")

        while (current_index <= target_index):
            for setting in settings:
                if type(setting) is tuple:
                    setting[0](model.agents[current_index], setting[1])
                else:
                    setting(model.agents[current_index])
            current_index += 1

    if current_index != len(model.agents):
        raise Exception("Agent specifications not given for all agents")


