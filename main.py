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
training_map_quote_length = util.DefaultDict(util.Counter)
nodebuilder = nodebuilders.SentenceBuilder()

last_node = None
for line in args.data:
    for word in line.split():
        node = nodebuilder.buildNode(word, last_node)
        if last_node is not None:
            training_map[last_node][node] += 1
        last_node = node

start_quote_nodes = [k for k in training_map if k[3]]

#start quote stack
startStack = []

start_nodes = [k for k in training_map if k[1]]
#start_quote_nodes = [k for k in training_map if k[3]]
end_quote_nodes = [k for k in training_map if k[4]]

word_count = 0
current_node = random.choice(start_nodes)

with args.output as out:
    while True:
        current_node = training_map[current_node].sample()
        word = nodebuilder.getWord(current_node)
        resample_count = 0

        #If we sample a startQuote and we have 2 quotes to close, resample
        while current_node[3] and len(startStack) > 1:
            current_node = training_map[current_node].sample()
            #update word
            word = nodebuilder.getWord(current_node)
            resample_count += 1
            if resample_count > 10:
                print "Too much resampling. I'm stuck. Help."
                break

        #If we sample an endQuote and there are no quotes to close, resample
        while current_node[4] and len(startStack) is 0:
            current_node = training_map[current_node].sample()
            #update word
            word = nodebuilder.getWord(current_node)
            resample_count += 1
            if resample_count > 10:
                print "Too much resampling. I'm stuck. Help."
                break

        #If the current_node starts a quote, append the quotes onto stack
        if current_node[3] and len(startStack) is 0:
            if word[0] is ('"', "'"):
                startStack.append(word[0])
            if word[1] in  ('"', "'"):
                startStack.append(word[1])
        #If current_node starts a quote and stack is only 1 long, append if it
        #makes sense
        elif current_node[3] and len(startStack) is 1:
            #If you are not duplicating the stack and only single quote word
            if word[0] is not startStack[0] and word[1] not in ('"', "'"):
                startStack.append(word[0])

        #If we sample an endQuote and we have quotes to close
        if current_node[4] and len(startStack) > 0:
            #Only 1 quote to close
            if len(startStack) is 1:
                #If it only closes the open quote on stack, clear the stack
                if word[-1:] is startStack[0] and word[-2:-1] not in ('"', "'"):
                    startStack.pop()
                #Resample otherwise
                else:
                    current_node = training_map[current_node].sample()
                    word = nodebuilder.getWord(current_node)

            #2 quotes to close
            else:
                #If it closes both quotes, clear the stack
                if word[-2:] is "'\"":
                    startStack.pop()
                    startStack.pop()
                #Remove last element if single, inner quote. Only double-quote
                #should remain
                elif word[-1:] is "'":
                    startStack.pop()
                #Resample otherwise
                else:
                    current_node = training_map[current_node].sample()
                    word = nodebuilder.getWord(current_node)

        out.write(nodebuilder.getWord(current_node))
        word_count += 1

        if word_count > 1000 and current_node[2]:
            break
        out.write(' ')
        
        

        if current_node is None:
            print "Oh noes!"
            exit()
