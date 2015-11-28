import random
import numpy

#TODO: test the win() logic heavily

# 0  | 1  | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  | 10 | 11 | 12 |
# 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
# 26 | 27 | 28 | 29 | 30 | 31 | 32 | 33 | 34 | 35 | 36 | 37 | 38 |
# 39 | 40 | 41 | 42 | 43 | 44 | 45 | 46 | 47 | 48 | 49 | 50 | 51 |

# 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  | 10 | J  | Q  | K  | A  |

#0-12 spades, 0 suit
#13-25 hearts, 1 suit
#26-38 diamonds, 2
#39-51 clubs, 3


def suit(card):
    return card//13

def face(card):
    return card%13

def printc(card):
    s = suit(card)
    f = face(card)
    if (f <= 8): word = f+2
    elif (f == 9): word = 'Jack'
    elif (f == 10): word = 'Queen'
    elif (f == 11): word = 'King'
    else: word = 'Ace'

    if (s==0):      print(word, ' of spades')
    elif (s==1):    print(word, 'of hearts')
    elif (s==2):    print(word, 'of diamonds')
    else:           print(word, 'of clubs')

def ispair(tface):
    pair = -1
    for i in range(len(tface)-1,0,-1):
        if (tface[i] == tface[i-1]):
            pair = i-1
            break
    return pair

def istwopair(pair, tface):
    twopair = -1
    if (pair != -1):
        for i in range(pair-1, 0,-1):
            if (tface[i] == tface[i-1] and tface[pair] != tface[i]):
                twopair = i-1
                break
    return twopair

def isthreeofakind(pair, tface):
    threeofakind = -1
    if (pair != -1):
        for i in range(len(tface)-1, 1, -1):
            if (tface[i] == tface[i-1] and tface[i-1] == tface[i-2]):
                threeofakind = i-2
                break
    return threeofakind

def isstraight(tface, tsuit):
    straight = -1
    straightsuit = -1
    s = 0

    tface2 = [0]*7
    tsuit2 = [0]*7
    tface2[0] = tface[0]
    for i in range (0, len(tface)-1, 1):
        if tface[i] != tface[i+1]:
            tface2[s] = tface[i]
            tsuit2[s] = tsuit[i]
            s += 1
    tface2[s] = tface[len(tface)-1]
    tsuit2[s] = tsuit[len(tsuit)-1]

    if (s >= 5):
        for i in range(s, 3, -1):
            if (tface2[i] -1 == tface2[i-1] and
                tface2[i-1] -1 == tface2[i-2] and
                     tface2[i-2] -1 == tface2[i-3] and
                  tface2[i-3] -1 == tface2[i-4]):
                if (straight < tface[2]):
                    straight = tface2[i]
                    straightsuit = tsuit2[i]
            if (straight == -1 and tface[6] == 12):
                  if(tface2[3] == 3 and
                     tface2[2] == 2 and
                      tface2[1] == 1 and
                       tface2[0] == 0):
                      straight = 3
                      straightsuit = tsuit2[3]
    return straight, straightsuit

import collections

def isflush(tface, tsuit):                   
    flush = -1
    flushsuit = -1
    
    counter = collections.Counter(tsuit)

    for s in counter:
        if counter[s] >= 5:
            flushsuit = s

            toReturn = []
            for j in range(len(tface) - 1, -1, -1):
                if (tsuit[j] == flushsuit):
                    toReturn.append(tface[j])
                
                if len(toReturn) == 5:
                    return toReturn, flushsuit
                    
            raise Exception('Invalid Flush')

    return flush, flushsuit

def isfullhouse(twopair, threeofakind, tface):
    fullhouse = -1
    if (threeofakind != -1 and twopair != -1):
        fullhouse = tface[threeofakind]
    return fullhouse

def isfourofakind(threeofakind, tface):
    fourofakind = -1
    if (threeofakind != -1):
        for i in range(len(tface)-1, 2, -1):
            if (tface[i] == tface[i-1]):
                if (tface[i-1] == tface[i-2]):
                    if (tface[i-2] == tface[i-3]):
                        fourofakind = i-3
                        break
    return fourofakind

def isstraightflush(straight, straightsuit, flush, flushsuit):
    straightflush = -1
    if (straight != -1 and flush != -1 and flushsuit == straightsuit):
        straightflush = straight
    return straightflush

def value(hand, table):

    tface = [0]*(len(hand)+len(table))
    tsuit = [0]*(len(hand)+len(table))

    for i in range(0, len(hand)):
        tface[i] = face(hand[i])
        tsuit[i] = suit(hand[i])

    for j in range(len(hand), len(hand)+len(table),1):
        tface[j] = face(table[j-2])
        tsuit[j] = suit(table[j-2])

    #TODO what kind of sorting are we talking about?
    #sorted in ascending order
    tface, tsuit = zip(*sorted(zip(tface, tsuit), key = lambda x : x[0]))
    #print("tface after sorting", tface)

    highcard = tface[len(tface)-1] #high card
    #print("Highcard(value) - ", highcard)

    #PAIR: returns the lowest index of the highest pair in the hand
    # i.e. ispair([0,1,2,3,3,4,5])
    # >>>
    # 3
    # returns -1 if no pairs are present
    pair = ispair(tface)
    #print("Pair(index)- ", pair)
        
    #TWO PAIRS: returns the lowest index of the lowest pair in the hand
    # i.e. istwopair(pair, [0,2,2,3,3,4,5])
    # >>>
    # 1
    # returns -1 if no pairs are present
    twopair = istwopair(pair, tface)
    #print("Two pairs(lowest index) - ", twopair)

    #THREE OF A KIND: returns the lowest index of the highest triple in the hand
    # i.e. isthreeofakind(pair, [0,0,0,3,5,5,5])
    # >>>
    # 4
    # returns -1 if no triple is present
    threeofakind = isthreeofakind(pair, tface)
    #print("Three of a kind(lowest index) - ", threeofakind)

    #STRAIGHT: returns the highest card value of the straight in the hand and
    # the suit of that card
    # i.e. isstraight([4,5,6,6,7,8,11], [0,0,0,0,0,0,0])
    # >>>
    # (8, 0)
    # returns (-1,-1) if no straight is present
    straight, straightsuit = isstraight(tface, tsuit)
    #print("Straight(highest value) - ", straight)
    #print("Straightsuit - ", straightsuit)

    #FLUSH: returns the highest card value of the flush in the hand and
    # the suit of that card
    # i.e. isflush([4,5,6,6,7,8,11], [0,0,0,0,0,0,0])
    # >>>
    # (11, 0)
    # returns (-1,-1) if no flush is present                
    flush, flushsuit = isflush(tface, tsuit)
    #print("Flush(highest value) - ", flush)
    #print("Flushsuit - ", flushsuit)
    
    #FULL HOUSE: returns the highest card value of the triple in the hand
    # i.e. isfullhouse(0, 3, [1,1,8,11,11,11,51])
    # >>>
    # 11
    # returns -1 if no full house is present
    fullhouse = isfullhouse(twopair, threeofakind, tface)
    #print("Fullhouse(value of triple) - ", fullhouse)

    #FOUR OF A KIND: returns the lowest index of of the quadruple in the hand
    # i.e. isfourofakind(3, [1,1,11,11,11,11,51])
    # >>>
    # 5
    # returns -1 if no four of a kind is present
    fourofakind = isfourofakind(threeofakind, tface)
    #print("Four of a kind(lowest index) - ", fourofakind)

    #STRAIGHT FLUSH: returns the highest card value of the straight in the hand
    # i.e. isstraightflush(12,0,12,0)
    # >>>
    # 12
    # returns -1 if no straight flush is present
    straightflush = isstraightflush(straight, straightsuit, flush, flushsuit)
    #print("Straight flush(highest card) - ", straightflush)
    
    #HIGHCARDS
    if (straightflush != -1):
        #print "straight flush"
        return 8, [straightflush], []

    if (fourofakind != -1):
        #print "four of a kind"
        fourofakind = tface[fourofakind]

        cards = set(tface)
        cards.remove(fourofakind)
        cards = sorted(list(cards))

        return 7, [fourofakind], cards[-1:]

    if (fullhouse != -1):
        #print "full house"
        return 6, [max(tface[pair], tface[twopair]), fullhouse], []

    if (flush != -1):
        #print "flush"
        return 5, flush, []

    if (straight != -1):
        #print "straight"
        return 4, [straight], []
    
    if (threeofakind != -1):
        #print "three of a kind"
        threeofakind = tface[threeofakind]

        cards = set(tface)
        cards.remove(threeofakind)
        cards = sorted(list(cards))

        return 3, [threeofakind], cards[-2:]

    if (twopair != -1):
        #print "two pair"
        twopair = tface[twopair]

        cards = set(tface)
        cards.remove(twopair)
        cards.remove(tface[pair])
        cards = sorted(list(cards))

        return 2, [twopair, tface[pair]], cards[-1:]

    if (pair != -1):
        #print "pair"
        pair = tface[pair]

        cards = set(tface)
        cards.remove(pair)
        cards = sorted(list(cards))

        return 1, [pair], cards[-3:]

    #print "high card"

    return 0, [], tuple(tface[2:7])

def win(hand0, hand1, table):
    #print "player 0"
    type0, value0, highcards0 = value(hand0, table)

    value0 = numpy.array(sorted(value0, reverse = True))
    highcards0 = numpy.array(sorted(highcards0, reverse = True))
    #print type0, value0, highcards0
    #print "player 1"
    type1, value1, highcards1 = value(hand1, table)

    value1 = numpy.array(sorted(value1, reverse = True))
    highcards1 = numpy.array(sorted(highcards1, reverse = True))
    #print type1, value1, highcards1
    #print "----"

    if type0 != type1:
        return type0 > type1

    comp = (value0 == value1)

    #print comp

    for i, eq in enumerate(comp):
        if not eq:
            #print i
            return value0[i] > value1[i]

    comp = (highcards0 == highcards1)

    #print "checking high card"

    for i, eq in enumerate(comp):
        if not eq:
            #print i
            return highcards0[i] > highcards1[i]        

    #print "it's a tie"

    return 2

def estimate(hand0, hole, N = 100):
    deck0 = list(set(range(0, 52)) - set(hand0) - set(hole))

    outcomes = []

    for i in range(N):
        cards = random.sample(deck0, 7)
        #random.shuffle(deck0)
        thole = list(hole)

        hand1 = cards[0:2]#random.sample(deck0, 2)

        thole += cards[2 : 2 + 5 - len(hole)]#deck0[2 : 2 + 5 - len(hole)]

        #printc(hand0[0])
        #printc(hand0[1])
        #printc(hand1[0])
        #printc(hand1[1])
        #printc(thole[0])
        #printc(thole[1])
        #printc(thole[2])
        #printc(thole[3])
        #printc(thole[4])
        outcomes.append(win(hand0, hand1, thole))

    outcomes = numpy.array(outcomes)

    outcomes[outcomes == 2] = 0.5

    return numpy.mean(outcomes) if len(outcomes) > 0 else 0

def estimate2(hand0, hole, N = 30):
    outcomes = []

    for i in range(N):
        thole = list(hole)

        deck = set(range(0, 52)) - set(hand0) - set(hole)

        cards = random.sample(deck, 7)

        hand1 = cards[0:2]#random.sample(deck0, 2)

        w1s = []
        w2s = []

        if len(hole) == 0:
            state = 0
        elif len(hole) == 3:
            state = 1
        elif len(hole) == 4:
            state = 2
        elif len(hole) == 5:
            state = 3
        
        for i in range(state, 3):
            thole = hole + cards[2 : 2 + (i + 2) - len(hole)]#deck0[2 : 2 + 5 - len(hole)]

            w1s.append(estimate(hand0, thole, 30))
            w2s.append(estimate(hand1, thole, 30))

        p1folded = False
        p2folded = False
        for w1, w2 in zip(w1s, w2s):
            if w1 < 0.5:
                p1folded = True
            
            if w2 < 0.5:
                p2folded = True

            if p1folded and not p2folded:
                outcomes.append(0.0)
            elif not p1folded and p2folded:
                outcomes.append(1.0)
            elif p1folded and p2folded:
                outcomes.append(0.5)

        if not p1folded and not p2folded:
            #print hand0, hand1, hole
            thole = hole + cards[2 : 2 + 5 - len(hole)]#deck0[2 : 2 + 5 - len(hole)]

            output = win(hand0, hand1, thole)

            if output == 2:
                outcomes.append(0.5)
            elif output == 1:
                outcomes.append(1.0)
            elif output == 0:
                outcomes.append(0.0)

    return numpy.mean(outcomes)

def testWinningOdds():
    hand0 = [0]*2
    hand1 = [0]*2
    table = [0]*5
    
    hand0[0] = int(random.random()*52 //1)
    hand0[1] = int(random.random()*52 //1)

    print('We have: ')
    printc(hand0[0])
    printc(hand0[1])

    hand1[0] = int(random.random()*52//1)
    hand1[1] = int(random.random()*52//1)
    print('He has: ')
    printc(hand1[0])
    printc(hand1[1])

    
    table[0] = int(random.random()*52//1)
    table[1] = int(random.random()*52//1)
    table[2] = int(random.random()*52//1)
    table[3] = int(random.random()*52//1)
    table[4] = int(random.random()*52//1)
    print('Table: ')
    printc(table[0])
    printc(table[1])
    printc(table[2])
    printc(table[3])
    printc(table[4])
    
    print(win(hand0, hand1, table))
