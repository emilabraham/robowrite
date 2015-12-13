import re

class BasicBuilder(object):
    def buildNode(self, word, last_node):
        return word
    
    def getWord(self, node):
        return node


class SentenceBuilder(object):
    def __init__(self):
        # A word is considered to end a sentence if it ends in one of . ? !
        # optionally followed by some number of single or double quotes
        self.endPattern = re.compile('.*[.!?][\'"]*')

        #Matches word starting with single or double quotes
        self.startsQuote = re.compile('[\'"].*[^.!?]')

        #Matches for punctuation and then any type of quote at end of word
        self.endsQuote = re.compile('[-.!?,][\'"]$')

    def buildNode(self, word, last_node):

        # This word is considered to start a sentence if it is the first word
        # or the last word ended a sentence
        startsSentence = True if last_node is None else last_node[2]
        endsSentence = self.endPattern.match(word) is not None
        startsQuote = self.startsQuote.match(word) is not None

        #Search anywhere in word for the endsQuote pattern
        endsQuote = self.endsQuote.search(word) is not None

        return (word, startsSentence, endsSentence, startsQuote, endsQuote)

    def getWord(self, node):
        return node[0]
