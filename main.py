#! /usr/bin/env python

import argparse
import cPickle
import nodebuilders
import random
import re
import util

parser = argparse.ArgumentParser(description="An AI for writing prose \"similar\" to an input document.")
parser.add_argument('data', type=argparse.FileType('r'), help="The file to read training data from")
parser.add_argument('output',type=argparse.FileType('w'), help="The file to write the novel to")

parser.add_argument('-x', '--export', action='store_true', help="Export training data to the output file instead of writing anything.")
parser.add_argument('-i', '--import', action='store_true', dest='imp', help="Import pre-calculated training data from the input file, instead of parsing prose")

parser.add_argument('-c', '--word-count', type=int, default=2000, metavar="WC",
        help="The minimum number of words to write. Will quit writing after finishing a sentence.")
parser.add_argument('-w', '--wrap-width', type=int, default=150, metavar="WW",
        help="The number of characters to wrap the text to. Single words longer than this may still go past this amount.")
args = parser.parse_args()

builderType = nodebuilders.QuoteBuilder
if args.imp:
    loaded = cPickle.load(args.data)
    training_map = loaded['training_map']
    nb = builderType(loaded['metadata'])
else:
    training_map = util.DefaultDict(util.Counter)
    nb = builderType()

    not_title = re.compile('.*[a-z].*')

    last_node = None
    blank_lines = 0
    for line in args.data:
        words = line.split()

        is_title = False
        if not words:
            blank_lines += 1
        elif not not_title.match(line):
            is_title = True

        for word in words:
            node = nb.buildNode(word, last_node, blank_lines, is_title)
            blank_lines = 0;
            if last_node is not None:
                training_map[last_node][node] += 1
            last_node = node
args.data.close()

if args.export:
    cPickle.dump({
        'training_map': training_map,
        'metadata': nb.metadata}, args.output, -1)
else:
    start_nodes = [k for k in training_map if nb.getMetadata(k, 'startsSentence')]

    word_count = 0
    line_width = 0
    in_quote = False
    current_node = random.choice(start_nodes)

    trimQuotes = re.compile('[^\'"]+[\'"]*$')

    while True:
        word = nb.getWord(current_node)

        if in_quote and nb.getMetadata(current_node, 'quotesStarted'):
            trimmed = trimQuotes.search(word)
            word = trimmed.group() if trimmed else word

        if nb.getMetadata(current_node, 'linesBefore') > 0:
            args.output.write('\n' + '\n'*nb.getMetadata(current_node, 'linesBefore'))
            line_width = 0
        elif line_width > 0 and line_width+len(word)+1 < args.wrap_width:
            args.output.write(' ')
            line_width += 1
        elif line_width > 0:
            args.output.write('\n')
            line_width = 0

        args.output.write(word)
        word_count += 1
        line_width += len(word)

        if word_count > args.word_count and nb.getMetadata(current_node, 'endsSentence'):
            break

        if nb.getMetadata(current_node, 'quotesStarted'):
            in_quote = True

        if nb.getMetadata(current_node, 'quotesEnded'):
            in_quote = False


        if in_quote:
            possible_nodes = [n for n in training_map[current_node] if not nb.getMetadata(n, 'quotesStarted')]

            if not possible_nodes:
                current_node = training_map[current_node].sample()
            else:
                current_node = random.choice(possible_nodes)
        else:
            current_node = training_map[current_node].sample()

        if current_node is None:
            print "Failed to find a node. Picking randomly..."
            current_node = random.choice(start_nodes)

args.output.close()
