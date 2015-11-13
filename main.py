import random

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
    for i in range(6,0,-1):
        if (tface[i] == tface[i-1]):
            pair = i
            break
    return pair

def istwopair(pair, tface):
    twopair = -1
    if (pair != -1):
        for i in range(pair, 0,-1):
            if (tface[i] == tface[i-1]):
                twopair = i
                break
    return twopair

def value(hand, table):

    tface = [0]*7
    tsuit = [0]*7

    for i in range(0, 2):
        tface[i] = face(hand[i])
        tsuit[i] = suit(hand[i])

    for j in range(2, 7):
        tface[i] = face(table[i-2])
        tsuit[i] = suit(table[i-2])

    #TODO what kind of sorting are we talking about?
    #sorted in ascending order
    tface.sort(reverse = False)
    tsuit.sort(reverse = False)

    high = tface[6] #high card

    #PAIR: returns the highest index of the highest pair in the hand
    # i.e. pair([0,1,2,3,3,4,5])
    # returns -1 if no pairs are present
    pair = ispair(tface)
        
    #TWOPAIR: -1, sum of pairs
    twopair = istwopair(pair, tface)    

    #THREEOFAKIND: -1, value of the card
    threeofakind = -1
    if (pair != -1):
        for i in range(pair, 2):
            if (tface[i] == tface[i-1] and tface[i-1] == tface[i-2]):
                threeofakind = i
                break

    #STRAIGHT: -1, largest card
    straight = -1
    straightsuit = -1
    s = 0

    tface2 = [0]*8
    tsuit2 = [0]*8
    tface2[0] = tface[0]
    for i in range (1, 7):
        if tface[i] != tface[i-1]:
            tface2[s] = tface[i]
            tsuit2[s] = tsuit[i]
            s += 1

    if (s >= 5):
        for i in range(s-1, 3):
            if (tface2[i] -1 == tface2[i-1] and
                tface2[i] -2 == tface2[i-2] and
                 tface2[i] -3 == tface2[i-3] and
                  tface2[i] -4 == tface2[i-4]):
                  straight = tface2[i]
                  straightsuit = tsuit2[i]
            if (straight == -1 and tface[6] == 12):
                  if(tface2[3] == 3 and
                     tface2[2] == 2 and
                      tface2[1] == 1 and
                       tface2[0] == 0):
                      straight = 3
                      straightsuit = tsuit2[3]

    #FLUSH: -1, highest card
    flush = -1
    flushsuit = -1
    cs = [0]*4
    ms = [0]*4
    
    for i in range(0, 6):
        cs[tsuit[i]] += 1
        ms[tsuit[i]] = max(ms[tsuit[i]], tface[i])

    if (cs[0] >= 5):
        flush = ms[0]
        flushsuit = 0
    if (cs[1] >= 5):
        flush = ms[1]
        flushsuit = 1
    if (cs[2] >= 5):
        flush = ms[2]
        flushsuit = 2
    if (cs[3] >= 5):
        flush = ms[3]
        flushsuit = 3

    #FULLHOUSE: -1, highest triple
    fullhouse = -1
    if (threeofakind != -1 and twopair != -1):
        fullhouse = tface[threeofakind]

    #FOUROFAKIND: -1, card value
    fourofakind = -1
    if (threeofakind != -1):
        for i in range(threeofakind, 3):
            if (tface[i] == tface[i-1] and
                tface[i] == tface[i-2] and
                tface[i] == tface[i-3]):
                fourofakind = i

    #STRAIGHTFLUSH: -1, highest card
    straightflush = -1
    if (straight != -1 and flush != -1 and flushsuit == straightsuit):
        straightflush = straight

    #TODO: stemmer denne logikken?
    #HIGHCARDS
    pair = tface[pair]
    twopair = tface[twopair]
    threeofakind = tface[threeofakind]
    fourofakind = tface[fourofakind]

    if (straightflush != -1):
        return 13*8 + straightflush

    if (fourofakind != -1):
        return 13*7 + straightflush

    if (fullhouse != -1):
        return 13*6 + straightflush

    if (flush != -1):
        return 13*5 + straightflush

    if (straight != -1):
        return 13*4 + straightflush

    if (threeofakind != -1):
        return 13*3 + straightflush

    if (twopair != -1):
        return 13*2 + straightflush

    if (pair != -1):
        return 13*1 + straightflush

    return tface[6]

def win(hand0, hand1, table):
    value0 = value(hand0, table)
    value1 = value(hand1, table)

    if (value0 == value1):
        if (face(hand0[0]) == face(hand0[1]) and face(hand1[0]) == face(hand1[1])):
            return (face(hand0[0]) > face(hand1[0]))
        elif (face(hand0[0]) == face(hand0[1])):
            return true;
        elif (face(hand1[0]) == face(hand1[1])):
            return false
        else:
            return max(face(hand0[0]), face(hand0[1])) > max(face(hand0[0]), face(hand0[1]))
    else:
        return value0 > value1

def main():
    total = 0

    hand0 = [0]*2
    hand1 = [0]*2
    table = [0]*5

    hand0[0] = int(random.random()*52 //1)
    hand0[1] = int(random.random()*52 //1)

    print('We have: ', hand0[0], hand0[1])

    nhands = 0
    nwins = 0


    #The big LOOP

    i = 5
    j = 43

    print(i, j)

    hand1[0] = i
    hand1[1] = j
    print('He has:', i, j)
    print(hand1[0])
    print(hand1[1])

    for k in range(j+1, 50):
        for l in range(k+1, 50):
            for m in range(l+1, 50):
                for n in range(m+1, 50):
                    for o in range(n+1, 50):
                        table[0] = k
                        table[1] = l
                        table[2] = m
                        table[3] = n
                        table[4] = o

                        if (win(hand0, hand1, table)):
                            nwins += 1

                        nhands += 1
    print("percent win (max 1.0) ", nwins/nhans)
    print(total)
                        
    

















    
