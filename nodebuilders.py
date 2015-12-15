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
        self.endPattern = re.compile('.*[.!?][\'"]*$')

    def buildNode(self, word, last_node):

        # This word is considered to start a sentence if it is the first word
        # or the last word ended a sentence
        startsSentence = True if last_node is None else last_node[2]
        endsSentence = self.endPattern.match(word) is not None

        return (word, startsSentence, endsSentence)

    def getWord(self, node):
        return node[0]


class ParagraphBuilder(object):
    def __init__(self):
        # A word is considered to end a sentence if it ends in one of . ? !
        # optionally followed by some number of single or double quotes
        self.endPattern = re.compile('.*[.!?][\'"]*$')

    def buildNode(self, word, last_node, lines_before, is_title):

        # This word is considered to start a sentence if it is the first word
        # or the last word ended a sentence
        startsSentence = True if last_node is None else last_node[2]
        endsSentence = self.endPattern.match(word) is not None

        return (word, startsSentence, endsSentence, lines_before, is_title)

    def getWord(self, node):
        return node[0]



class QuoteBuilder(object):
    def __init__(self):
        # A word is considered to end a sentence if it ends in one of . ? !
        # optionally followed by some number of single or double quotes
        self.endPattern = re.compile('.*[.!?][\'"]*$')

        self.startQuotePattern = re.compile('[\'"]+')
        self.endQuotePattern = re.compile('[\'"]+$')

    def buildNode(self, word, last_node, lines_before, is_title):

        # This word is considered to start a sentence if it is the first word
        # or the last word ended a sentence
        startsSentence = True if last_node is None else last_node[2]
        endsSentence = self.endPattern.match(word) is not None

        startQuote = self.startQuotePattern.match(word)
        endQuote = self.endQuotePattern.search(word)

        if startQuote is not None:
            startQuote = startQuote.group()
        if endQuote is not None:
            endQuote = endQuote.group()

        return (word, startsSentence, endsSentence, lines_before, is_title, startQuote, endQuote)

    def getWord(self, node):
        return node[0]
