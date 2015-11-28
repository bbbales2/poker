#!/usr/bin/env python
# Evaluate chance of winning at each betting round. Raise when possible

import socket
import random
import sys
import subprocess
import time
import main
import re

#import pyximport
#pyximport.install()
import main

if len(sys.argv) < 3:
    print "Usage: player ip port"
    exit(0)

ip = sys.argv[1]
port = int(sys.argv[2])
bufferSize = 1024

ranks = '23456789TJQKA'
suits = 'shdc'

def ai2num(string):
    for i, s in enumerate(suits):
        if string[1] == s:
            suit = i
            break

    for i, r in enumerate(ranks):
        if string[0] == r:
            rank = i
            break

    return suit * 13 + rank

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((ip, port))

sock.send('VERSION:2.0.0\n')

print 'WE ARE THIS'

while 1:
    data = sock.recv(bufferSize).strip()
    for line in data.split('\r\n'):
        #print '-----'
        #print "recv : ", line

        tmp, position, handNumber, bets, cards = line.split(':')
        
        #print "tmp", tmp
        #print "position", position
        #print "hand number", handNumber
        #print "bets", bets
        #print "cards", cards
        
        position = int(position)
        handNumber = int(handNumber)
        
        bets = bets.split('/')
        
        roundNumber = len(bets)
        
        ourCards, otherCards = cards.split('|')
        ourCards = re.findall('..', ourCards)
        otherCards = otherCards.split('/')
        otherDudesCards = otherCards[0]
        otherDudesCards = re.findall('..', otherDudesCards)
        holeCards = ''.join(otherCards[1:])
        holeCards = re.findall('..', holeCards)

        if position == 1:
            tmp = ourCards
            ourCards = otherDudesCards
            otherDudesCards = tmp

        #print 'ourCards', ourCards
        #print 'otherDudesCards', otherDudesCards

        finished = False
        if (len(ourCards) == len(otherDudesCards)) or (len(bets[-1]) > 0 and bets[-1][-1] == 'f'):
            finished = True
        
        play = False
        
        #print 'bets[-1]', bets[-1]
        #print 'roundNumber', roundNumber
        #print 'position', position
        #print len(bets[-1])

        raises = 0
        for c in bets[-1]:
            if c == 'r':
                raises += 1
        
        if roundNumber == 1:
            if position == 1 and len(bets[-1]) % 2 == 0:
                play = True
            elif position == 0 and len(bets[-1]) % 2 == 1:
                play = True
        elif roundNumber > 1:
            if position == 1 and len(bets[-1]) % 2 == 1:
                play = True
            elif position == 0 and len(bets[-1]) % 2 == 0:
                play = True

        #print "play", play

        if play and not finished:
            ranks = '23456789TJQKA'
            suits = 'shdc'

            deck = set()
            for r in ranks:
                for s in suits:
                    deck.add(r + s)

            for card in ourCards + holeCards:
                deck.remove(card)

            #print ourCards
            #print holeCards

            percent = main.estimate([ai2num(c) for c in ourCards],
                                    [ai2num(c) for c in holeCards],
                                    1000)

            #print "EQUITY: ", percent

            response = 'r'

            if raises >= 3 and roundNumber == 1:
                response = 'c'
            elif raises >= 4 and roundNumber > 1:
                response = 'c'

            if percent < 0.5:
                if len(bets[-1]) == 0 or (len(bets[-1]) == 1 and bets[-1][0] == 'c'):
                    response = 'c'
                else:
                    response = 'f'

            string = '{0}:{1}\r\n'.format(line, response)
            #print "send : ", "c"
            sock.send(string)

sock.close()
