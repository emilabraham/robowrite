#! /usr/bin/env python

import argparse
from util import DefaultDict, Counter

parser = argparse.ArgumentParser(description="An AI for writing prose \"similar\" to an input document.")
parser.add_argument('data', type=argparse.FileType('r'), help="The file to read training data from")
args = parser.parse_args()

training_map = DefaultDict(Counter)

last_word = None
for line in args.data:
    for word in line.split():
        if last_word is not None:
            training_map[last_word][word] += 1
        last_word = word

print training_map['Sherlock']
