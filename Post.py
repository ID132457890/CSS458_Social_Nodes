class Post(object):
    """
    Post object, currently contains no behavior
    """

    def __init__(self, sender, topics):
        """
        :param sender: Reference to agent who sent the message
        :param topics: List of integers representing message topics
        """
        self.sender = sender
        self.topics = topics