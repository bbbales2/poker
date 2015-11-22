#!/usr/bin/env python
# Evaluate chance of winning at each betting round.
# 
# For 50-60%, prefer check to raise
# For 40-50% and past flop, don't fold

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

def val(e, preflop, bets, maxRaises, pool, sb = 2, bb = 4):
    raises = 0

    for b in bets:
        if b == 'r':
            raises += 1

    sgn = 1
    if not preflop:
        sgn = -1

    vals = {}

    if raises < maxRaises:
        #print 'raise side of tree'
        vals['r'] = val(e, preflop, bets + 'r', maxRaises, pool, sb, bb)[1]
        
    if len(bets) == 0:
        #print 'check side of tree'
        vals['c'] = val(e, preflop, bets + 'c', maxRaises, pool, sb, bb)[1]
    else:
        #print 'hihihihi', e, raises, bb, -(e - 0.5) * (2 * bb + raises * 2 * bb) 
        vals['c'] = -(e - 0.5) * ((2 * bb + raises * 2 * bb) + pool)

    if preflop and len(bets) == 0:
        vals['f'] = sb
    else:
        #print raises, (-1)**raises
        vals['f'] = (raises * bb + pool / 2.0) * (-1)**(raises + (1 if (len(bets) > 0 and bets[0] == 'c') else 0) + (1 if not preflop else 0))
        
    if len(bets) == 1 and bets[0] == 'c':
        del vals['f']

    if len(bets) % 2 == (1 if preflop else 0):
        #print 'max of ', vals
        test = sorted(vals.items(), key = lambda x : x[1])[-1]
        return test
    else:
        #print 'min of ', vals
        return sorted(vals.items(), key = lambda x : x[1])[0]

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
                                    [ai2num(c) for c in deck],
                                    [ai2num(c) for c in holeCards],
                                    100)

            #print "EQUITY: ", percent

            if position == 0:
                percent = 1 - percent

            response = val(percent, roundNumber == 1, bets[-1], 3 if roundNumber == 1 else 4, 0, 10, 20)[0]

            #response = 'r'

            #if raises >= 3 and roundNumber == 1:
            #    response = 'c'
            #elif raises >= 4 and roundNumber > 1:
            #    response = 'c'

            #if percent < 0.6:
            #    response = 'c'

            #if ((percent < 0.5 and roundNumber <= 2) or
            #    (percent < 0.4 and roundNumber > 2)):
            #    if len(bets[-1]) == 0 or bets[-1][0] == 'c':
            #        response = 'c'
            #    else:
            #        response = 'f'

            string = '{0}:{1}\r\n'.format(line, response)
            #print "send : ", "c"
            sock.send(string)

sock.close()
