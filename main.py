import random

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

def isflush(tface, tsuit):                   
    flush = -1
    flushsuit = -1
    
    suitlist = tsuit
    suitlist.sort(reverse = False)

    for i in range(len(suitlist)-1, 4, -1):
        if (suitlist[i] == suitlist[i-1]):
            if (suitlist[i-1] == suitlist[i-2]):
                if (suitlist[i-2] == suitlist[i-3]):
                    if (suitlist[i-3] == suitlist[i-4]):
                        if (suitlist[i-4] == suitlist[i-5]):
                            flushsuit = suitlist[i]
                            for j in range(len(tface)-1, 3,-1):
                                if (tsuit[j] == flushsuit):
                                    flush = tface[j]
                                    break
                            break
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
    tface.sort(reverse = False)
    tsuit.sort(reverse = False)
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
        return 13*8 + straightflush

    if (fourofakind != -1):
        fourofakind = tface[fourofakind]
        return 13*7 + fourofakind

    if (fullhouse != -1):
        return 13*6 + fullhouse

    if (flush != -1):
        return 13*5 + flush

    if (straight != -1):
        return 13*4 + straight
    
    if (threeofakind != -1):
        threeofakind = tface[threeofakind]
        return 13*3 + threeofakind

    if (twopair != -1):
        twopair = tface[pair]
        return 13*2 + twopair

    if (pair != -1):
        pair = tface[pair]
        return 13*1 + pair

    return tface[6]

def win(hand0, hand1, table):
    value0 = value(hand0, table)
    #print(value0)
    value1 = value(hand1, table)
    #print(value1)

    if (value0 == value1):
        if (face(hand0[0]) == face(hand0[1]) and face(hand1[0]) == face(hand1[1])):
            return (face(hand0[0]) > face(hand1[0]))
        elif (face(hand0[0]) == face(hand0[1])):
            return True;
        elif (face(hand1[0]) == face(hand1[1])):
            return False
        else:
            return max(face(hand0[0]), face(hand0[1])) > max(face(hand0[0]), face(hand0[1]))
    else:
        return value0 > value1

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

def main():
    total = 0

    hand0 = [0]*2
    hand1 = [0]*2
    table = [0]*5

    hand0[0] = int(random.random()*52 //1)
    hand0[1] = int(random.random()*52 //1)

    print('We have: ')
    printc(hand0[0])
    printc(hand0[1])

    nhands = 0
    nwins = 0


    #The big LOOP

    hand1[0] = int(random.random()*52//1)
    hand1[1] = int(random.random()*52//1)
    print('He has: ')
    printc(hand1[0])
    printc(hand1[1])

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
    print("percent win (max 1.0) ", nwins/nhands)
                        
    

















    