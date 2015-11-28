#!/usr/bin/env python
# Evaluate chance of winning at each betting round.
# 
# For 50-60%, prefer check to raise
# For 40-50% and past flop, don't fold

import numpy
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

distributions = {
    0 : {
    },
    1 : {
    }
}

#%%
distributions = {
    0 : {
    },
    1 : {
    }
}

def getPool(bets, bb):
    pool = 0

    for rd, betRound in enumerate(bets[:-1]):
        if len(betRound) == 0:
            continue

        if rd == 0 and betRound[0] == 'c':
            pool += bb

        for bet in betRound:
            if bet == 'r':
                pool += 2 * bb
                
    return pool
                        
def val(e, bets, maxRaises, pool, randomplayer, sb, bb):
    pool = getPool(bets, bb)

    raises = 0

    for b in bets[-1]:
        if b == 'r':
            raises += 1

    preflop = len(bets) == 1

    sgn = 1
    if not preflop:
        sgn = -1

    vals = {}

    if raises < maxRaises:
        #print 'raise side of tree'
        bets2 = list(bets)
        bets2[-1] += 'r'
        vals['r'] = val(e, bets2, maxRaises, pool, randomplayer, sb, bb)[1]
    #else:
    #    if len(bets) < 5:
    #        bets2 = list(bets)
    #        bets2.append('r')
    #        vals['r'] = val(e, bets2, maxRaises, pool, randomplayer, sb, bb)[1]

    if len(bets[-1]) == 0:
        #print 'check side of tree'
        bets2 = list(bets)
        bets2[-1] += 'c'
        vals['c'] = val(e, bets2, maxRaises, pool, randomplayer, sb, bb)[1]
    else:
        if len(bets) < 4:
            #raise Exception("addfssdf")
            bets2 = list(bets)
            bets2[-1] += 'c'
            bets2.append('')
            vals['c'] = val(e, bets2, maxRaises, pool, randomplayer, sb, bb)[1]
        else:
            #print 'hihihihi', e, raises, bb, -(e - 0.5) * (2 * bb + raises * 2 * bb)
            vals['c'] = -(e - 0.5) * ((2 * bb + raises * 2 * bb) + pool)

    if preflop and len(bets[0]) == 0:
        vals['f'] = sb
    else:
        #print raises, (-1)**raises
        vals['f'] = (raises * bb + pool / 2.0) * (-1)**(raises + (1 if (len(bets[-1]) > 0 and bets[-1][0] == 'c') else 0) + (1 if not preflop else 0))

    if (len(bets[-1]) == 1 and bets[-1][0] == 'c') or (len(bets) > 1 and len(bets[-1]) == 0):
        del vals['f']

    #print vals, bets, bets[-1], preflop


    if len(bets[-1]) % 2 == (1 if preflop else 0):
        #print 'max of ', vals
        key = (len(bets), bets[-1])

        if key not in distributions[randomplayer]:
            dist = { 'r' : 1.0, 'c' : 1.0, 'f' : 1.0 }
        else:
            dist = distributions[randomplayer][key]

        mixed = 0.0
        den = 0.0
        for c, v in vals.items():
            den += dist[c]

        for c, v in vals.items():
            mixed += (dist[c] / den) * v

        a = 1.0 / (1.0 + numpy.exp(-0.1 * (sum(dist.values()) - 50.0)))

        pure = sorted(vals.items(), key = lambda x : x[1])[-1]

        out = (pure[0], mixed * a + pure[1] * (1.0 - a))
    else:
        #print 'min of ', vals
        key = (len(bets), bets[-1])

        if key not in distributions[randomplayer]:
            dist = { 'r' : 1.0, 'c' : 1.0, 'f' : 1.0 }
        else:
            dist = distributions[randomplayer][key]

        mixed = 0.0
        den = 0.0
        for c, v in vals.items():
            den += dist[c]

        for c, v in vals.items():
            mixed += (dist[c] / den) * v

        a = 1.0 / (1.0 + numpy.exp(-0.1 * (sum(dist.values()) - 50.0)))

        pure = sorted(vals.items(), key = lambda x : x[1])[0]

        out = (pure[0], mixed * a + pure[1] * (1.0 - a))

    return out

otherBets = ''

def getBets(bets, position):
    output = ''

    for r in range(len(bets)):
        if r == 0:
            output += bets[r][(1 - position)::2]
        else:
            output += bets[r][position::2]
                    
    return output

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

        print '----------------'
        print "received ", line

        #print bets

        def lastBet(bets):
            tmpBets = list(bets)

            if len(tmpBets) == 1 and len(tmpBets[-1]) == 0:
                return -1

            if len(tmpBets[-1]) == 0 and len(tmpBets) > 1:
                del tmpBets[-1]

            #print tmpBets
            if len(tmpBets) == 1:
                if len(tmpBets[0]) % 2 == 1:
                    return 1
                else:
                    return 0
            else:
                if len(tmpBets[-1]) % 2 == 1:
                    return 0
                else:
                    return 1

        #print position, otherBets

        print bets, len(bets), len(bets[-1])
        print lastBet(bets), position
        #print 'lastplay ', lastBet(bets), position

        if lastBet(bets) == 1 - position:
            if len(bets) > 0 and len(bets[-1]) > 0:
                key = (len(bets), bets[-1][:-1])
            else:
                key = (len(bets) - 1, bets[-2][:-1])

            otherBets = getBets(bets, 1 - position)

            if key not in distributions[1 - position]:
                distributions[1 - position][key] = { 'r' : 1.0, 'c' : 1.0, 'f' : 1.0 }

            distributions[1 - position][key][otherBets[-1]] += 1

            print 'update'#, distributions

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
                                     100)

            print "EQUITY: ", percent

            if position == 0:
                percent = 1 - percent

            pool = 0

            for rd, betRound in enumerate(bets[:-1]):
                if len(betRound) == 0:
                    continue

                if rd == 0 and betRound[0] == 'c':
                    pool += 4

                for bet in betRound:
                    if bet == 'r':
                        pool += 8

            print 'Pool: ', pool

            response = val(percent, bets, 3 if roundNumber == 1 else 4, pool, 1 - position, 10, 20)[0]

            #if percent0 < 0.4:
            #    response = 'f'

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
            print "send : ", response, string
            sock.send(string)

sock.close()
