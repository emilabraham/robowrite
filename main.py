#! /usr/bin/env python

import argparse
import nodebuilders
import random
import util

parser = argparse.ArgumentParser(description="An AI for writing prose \"similar\" to an input document.")
parser.add_argument('data', type=argparse.FileType('r'), help="The file to read training data from")
parser.add_argument('output',type=argparse.FileType('w'), help="The file to write the novel to")
args = parser.parse_args()

training_map = util.DefaultDict(util.Counter)
nodebuilder = nodebuilders.SentenceBuilder()

last_node = None
for line in args.data:
    for word in line.split():
        node = nodebuilder.buildNode(word, last_node)
        if last_node is not None:
            training_map[last_node][node] += 1
        last_node = node

for tran in training_map.values():
    tran.normalize()

start_nodes = [k for k in training_map if k[1]]

word_count = 0
current_node = random.choice(start_nodes)
with args.output as out:
    while True:
        out.write(nodebuilder.getWord(current_node))
        word_count += 1

        if word_count > 1000 and current_node[2]:
            break
        out.write(' ')
        current_node = training_map[current_node].sample()

        if current_node is None:
            print "Oh noes!"
            exit()
