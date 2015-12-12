#! /usr/bin/env python

import argparse
import nodebuilders
from util import DefaultDict, Counter

parser = argparse.ArgumentParser(description="An AI for writing prose \"similar\" to an input document.")
parser.add_argument('data', type=argparse.FileType('r'), help="The file to read training data from")
args = parser.parse_args()

training_map = DefaultDict(Counter)
nodebuilder = nodebuilders.SentenceBuilder()

last_node = None
for line in args.data:
    for word in line.split():
        node = nodebuilder.buildNode(word, last_node)
        if last_node is not None:
            training_map[last_node][node] += 1
        last_node = node

for k in training_map.keys():
    if k[2]:
        print k
