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

nodebuilder = nodebuilders.ParagraphBuilder()
if args.imp:
    training_map = cPickle.load(args.data)
else:
    training_map = util.DefaultDict(util.Counter)

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
            node = nodebuilder.buildNode(word, last_node, blank_lines, is_title)
            blank_lines = 0;
            if last_node is not None:
                training_map[last_node][node] += 1
            last_node = node
args.data.close()

if args.export:
    cPickle.dump(training_map, args.output, -1)
else:
    start_nodes = [k for k in training_map if k[1]]

    word_count = 0
    line_width = 0
    current_node = random.choice(start_nodes)

    while True:
        word = nodebuilder.getWord(current_node)

        if current_node[3] > 0:
            args.output.write('\n' + '\n'*current_node[3])
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

        if word_count > args.word_count and current_node[2]:
            break

        current_node = training_map[current_node].sample()

        if current_node is None:
            print "Oh noes!"
            break
args.output.close()
