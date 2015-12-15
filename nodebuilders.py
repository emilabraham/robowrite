import re
import util

class BasicBuilder(object):
    def __init__(self, metadata=None):
        self.metadata = None
    def buildNode(self, word, last_node):
        return word
    
    def getWord(self, node):
        return node

    def getMetadata(self, node, key):
        return None


class SentenceBuilder(object):
    def __init__(self, metadata=None):
        # A word is considered to end a sentence if it ends in one of . ? !
        # optionally followed by some number of single or double quotes
        self.endPattern = re.compile('.*[.!?][\'"]*$')

        self.metadata = metadata or util.DefaultDict(dict)

    def buildNode(self, word, last_node):
        node = word

        self.metadata[node] = {
            # This word is considered to start a sentence if it is the first word
            # or the last word ended a sentence
            'startsSentence': True if last_node is None else self.getMetadata(last_node, 'endsSentence'),
            'endsSentence': self.endPattern.match(word) is not None}

        return node

    def getWord(self, node):
        return node

    def getMetadata(self, node, key):
        return self.metadata[node][key]


class ParagraphBuilder(object):
    def __init__(self, metadata=None):
        # A word is considered to end a sentence if it ends in one of . ? !
        # optionally followed by some number of single or double quotes
        self.endPattern = re.compile('.*[.!?][\'"]*$')

        self.metadata = metadata or util.DefaultDict(dict)

    def buildNode(self, word, last_node, lines_before, is_title):
        node = word

        self.metadata[node] = {
            # This word is considered to start a sentence if it is the first word
            # or the last word ended a sentence
            'startsSentence': True if last_node is None else self.getMetaData(last_node, 'endsSentence'),
            'endsSentence': self.endPattern.match(word) is not None,

            'linesBefore': lines_before,
            'isTitle': is_title}

        return node

    def getWord(self, node):
        return node

    def getMetadata(self, node, key):
        return self.metadata[node][key]


class QuoteBuilder(object):
    def __init__(self, metadata=None):
        # A word is considered to end a sentence if it ends in one of . ? !
        # optionally followed by some number of single or double quotes
        self.endPattern = re.compile('.*[.!?][\'"]*$')

        self.startQuotePattern = re.compile('[\'"]+')
        self.endQuotePattern = re.compile('[\'"]+$')

        self.metadata = metadata or util.DefaultDict(dict)

    def buildNode(self, word, last_node, lines_before, is_title):

        node = word

        # This word is considered to start a sentence if it is the first word
        # or the last word ended a sentence
        startsSentence = True if last_node is None else self.getMetadata(last_node, 'endsSentence')
        endsSentence = self.endPattern.match(word) is not None

        startQuote = self.startQuotePattern.match(word)
        endQuote = self.endQuotePattern.search(word)

        if startQuote is not None:
            startQuote = startQuote.group()
        if endQuote is not None:
            endQuote = endQuote.group()

        self.metadata[node] = {
            'startsSentence': startsSentence,
            'endsSentence': endsSentence,
            'linesBefore': lines_before,
            'isTitle': is_title,
            'quotesStarted': startQuote,
            'quotesEnded': endQuote}

        return word

    def getWord(self, node):
        return node

    def getMetadata(self, node, key):
        return self.metadata[node][key]
