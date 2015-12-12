import re

class BasicBuilder(object):
    def buildNode(self, word, last_node):
        return word
    
    def getWord(self, node):
        return node


class SentenceBuilder(object):
    def __init__(self):
        self.endPattern = re.compile('.*[.!?][\'"]*')

    def buildNode(self, word, last_node):

        # This word is considered to start a sentence if it is the first word
        # or the last word ended a sentence
        startsSentence = True if last_node is None else last_node[2]
        endsSentence = self.endPattern.match(word) is not None

        return (word, startsSentence, endsSentence)

    def getWord(self, node):
        return node[0]
