###%%
import socket
import contextlib#.contextmanager
import random
import sys
import subprocess
import time

IP = '127.0.0.1'
bufferSize = 1024

ranks = '23456789TJQKA'
suits = 'shdc'

odeck = []
for r in ranks:
    for s in suits:
        odeck.append(r + s)

deck = list(odeck)
random.shuffle(deck)

r = 0

players = [{ 'port' : int(sys.argv[1]), 'hand' : [] },
           { 'port' : int(sys.argv[1]) + 1, 'hand' : [] }]

for i, player in enumerate(players):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((IP, player['port']))
    s.listen(1)

    #Run the two example players
    #if i == 0:
    subprocess.Popen("./example_player.limit.2p.sh 127.0.0.1 {0}".format(player['port']).split())
    #else:
    #    subprocess.Popen("python ../webui.py {0}".format(player['port']).split())

    conn, addr = s.accept()

    player['socket'] = s
    player['c'] = conn
    data = player['c'].recv(bufferSize)
    print "received version data:", data

def buildState(i):
    player = players[i]
    string = 'MATCHSTATE:{position}:{handNumber}:{bets}:{cards}|{holes}\n'.format(position = i, handNumber = 0, bets = betsToString(), cards = ''.join(player['hand']), holes = holesToString())
    print 'sending to {0}: {1}'.format(i, string.strip())
    return string

bets = []

def betsToString():
    out = '/'.join(bets)
    return out

holes = []

def holesToString():
    out = '/'.join([''.join(hole) for hole in holes])

    if len(out) > 0:
        out = '/' + out

    return out

def prepareRound(r):
    if r == 0:
        players[0]['hand'].append(deck.pop())
        players[1]['hand'].append(deck.pop())
        players[0]['hand'].append(deck.pop())
        players[1]['hand'].append(deck.pop())
    elif r == 1:
        holes.append([])

        holes[0].append(deck.pop())
        holes[0].append(deck.pop())
        holes[0].append(deck.pop())
    elif r == 2:
        holes.append([])
        
        holes[-1].append(deck.pop())
    elif r == 3:
        holes.append([])
        
        holes[-1].append(deck.pop())
    bets.append('')

    for i, player in enumerate(players):
        player['c'].send(buildState(i))  # echo

def handleBets(cplayer):
    raises = 0

    ret = 'c'

    while 1:
        action = players[cplayer]['c'].recv(bufferSize).split(':')[-1]
        print action

        bets[-1] += action[0]

        if action[0] == 'f':
            if len(bets[0]) == 1:
                raise Exception("First bet in a round cannot fold")

            #print 'player {0} wins'.format(1 - cplayer)
            return ('f', cplayer)
        elif action[0] == 'r':
            if raises > 3:
                raise Exception("Too many raises!")

            raises += 1
        elif action[0] == 'c':
            if len(bets[-1]) != 1:
                #print "next round"
                return ('c', cplayer)

        # Send message to other player
        cplayer = 1 - cplayer
        players[cplayer]['c'].send(buildState(cplayer))

    raise Exception("Should never get here")

# Deal players their two cards
# In two players, button == small blind
# Non button player goes first!

for r in range(4):
    prepareRound(r)
    result = handleBets(0 if r > 0 else 1)

    if result[0] == 'f':
        print "player {0} won!".format(1 - result[1])
        break

for player in players:
    player['socket'].close()
