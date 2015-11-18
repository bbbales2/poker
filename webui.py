import flask
import os
import sys
import socket
import random
import flask.ext.session
import json
import main

def make_decision(player, roundNumber, bets, cards):
    raises = 0

    bets = bets.split('/')[-1]

    if len(bets) > 0:
        for b in bets:
            if b == 'r':
                raises += 1

        raises -= 1
    
    goesfirst = (player == 1 and roundNumber == 0) or (player == 0 and roundNumber > 0)

    print raises, bets

    if (len(bets) == 0 and goesfirst):
        choices = ['c', 'r', 'f']
    elif (not goesfirst and len(bets) == 1 and bets[0] == 'c'):
        choices = ['c', 'r']
    elif raises >= 3:
        choices = ['c', 'f']
    else:
        choices = ['c', 'r', 'f']

    return random.choice(choices)

appDir = os.path.abspath(os.path.dirname(__file__))

app = flask.Flask('poker', template_folder = appDir + '/templates/')

session = flask.ext.session.Session()

states = []
actions = []

def get_state():
    return { 'round' : flask.session['round'],
             'bets' : flask.session['bets'],
             'cards' : flask.session['cards'],
             'hcards' : flask.session['hcards'],
             'ccards' : flask.session['ccards'],
             'winner' : flask.session['winner'],
             'percent' : flask.session['percent'],
             'player' : flask.session['player'],
             'wallet' : flask.session['wallet'],
             'pool' : flask.session['pool'] }

def computer_play():
    pass

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

def make_play(player, action):
    bets = flask.session['bets'].split('/')[-1]

    raises = 0

    if len(bets) > 0:
        for b in bets:
            if b == 'r':
                raises += 1

        raises -= 1
    
    goesfirst = (player == 1 and flask.session['round'] == 0) or (player == 0 and flask.session['round'] > 0)

    #print raises, bets

    if (len(bets) == 0 and goesfirst):
        choices = ['c', 'r', 'f']
    elif (not goesfirst and len(bets) == 1 and bets[0] == 'c'):
        choices = ['c', 'r']
    elif raises >= 3:
        choices = ['c', 'f']
    else:
        choices = ['c', 'r', 'f']

    if flask.session['winner'] == -1 and action in choices:
        #print "{0} does {1}".format(player, action)
        flask.session['bets'] += action

        playerString = 'player' if (flask.session['player'] == player) else 'computer'

        if action == 'r':
            if flask.session['round'] == 0 and len(bets) == 0:
                #print 'f'
                flask.session['wallet'][playerString] -= 6
                flask.session['pool'][playerString] += 6
            elif len(bets) == 0 or bets == 'c':
                #print 'a'
                flask.session['wallet'][playerString] -= 4
                flask.session['pool'][playerString] += 4
            else:
                #print 'b'
                flask.session['wallet'][playerString] -= 8
                flask.session['pool'][playerString] += 8
        elif action == 'c':
            if flask.session['round'] == 0 and len(bets) == 0:
                #print 'i'
                flask.session['wallet'][playerString] -= 2
                flask.session['pool'][playerString] += 2
            elif len(bets) == 0:
                #print 'g'
                pass
            else:
                #print 'd'
                flask.session['wallet'][playerString] -= 4
                flask.session['pool'][playerString] += 4
        elif action == 'f':
            #print 'e'
            flask.session['winner'] = 1 - player

            winningPlayerString = 'computer' if playerString == 'player' else 'player'

            flask.session['wallet'][winningPlayerString] += sum(flask.session['pool'].values())
            flask.session['pool'] = { 'player' : 0,
                                      'computer' : 0 }

            return 'next'

    #print 'here we are', bets, flask.session['bets'].split('/')[-1], action, flask.session['round'], choices, flask.session['winner']

    if len(flask.session['bets'].split('/')[-1]) > 1 and action == 'c':
        if flask.session['round'] == 0 and flask.session['winner'] == -1:
            flask.session['cards'].append(flask.session['deck'].pop())
            flask.session['cards'].append(flask.session['deck'].pop())
            flask.session['cards'].append(flask.session['deck'].pop())
        elif flask.session['round'] == 1 and flask.session['winner'] == -1:
            flask.session['cards'].append(flask.session['deck'].pop())
        elif flask.session['round'] == 2 and flask.session['winner'] == -1:
            flask.session['cards'].append(flask.session['deck'].pop())
        elif flask.session['round'] >= 3:
            retVal = main.win([ai2num(card) for card in flask.session['hcards']],
                              [ai2num(card) for card in flask.session['ccards']],
                              [ai2num(card) for card in flask.session['cards']])

            if retVal == 0:
                retVal = 1 - flask.session['player']
            elif retVal == 1:
                retVal = flask.session['player']

            if flask.session['winner'] != 234134:
                if retVal != 2:
                    #print retVal
                    if flask.session['player'] == retVal:
                        winnerString = 'player'
                    else:
                        winnerString = 'computer'
                
                    #print flask.session['player'], 'won', winnerString

                    flask.session['wallet'][winnerString] += sum(flask.session['pool'].values())
                    flask.session['pool'] = { 'player' : 0,
                                              'computer' : 0 }
                else:
                    for player, value in flask.session['pool'].items():
                        flask.session['wallet'][player] += value
                        flask.session['pool'] = { 'player' : 0, 'computer' : 0 }

            flask.session['winner'] = flask.session['player'] if (flask.session['player'] == retVal) else 1 - flask.session['player']

        if flask.session['winner'] == -1:
            flask.session['round'] += 1
            flask.session['bets'] += '/'

        flask.session['percent'] = main.estimate([ai2num(c) for c in flask.session['hcards']], [ai2num(c) for c in flask.session['deck'] + flask.session['ccards']], [ai2num(c) for c in flask.session['cards']])

        return 'next'

    return None

@app.route('/play')
def play():
    action = flask.request.args.get('action', None)
    
    playerNumber = flask.session['player']
    computerNumber = 1 - flask.session['player']

    ret = make_play(playerNumber, action)

    if not ret or (computerNumber == 0 and ret):
        computerAction = make_decision(computerNumber, flask.session['round'], flask.session['bets'], flask.session['ccards'] + flask.session['cards'])

        make_play(computerNumber, computerAction)
    
    return flask.json.jsonify(state = get_state())

@app.route('/')
def index():
    reset = flask.request.args.get('reset', None)
    which = flask.request.args.get('which', None)
    resetWallet = flask.request.args.get('resetWallet', None)

    if which:
        which = int(which)

    if (resetWallet is not None or
        reset is not None and
        'pool' in flask.session):
        for player, value in flask.session['pool'].items():
            flask.session['wallet'][player] += value
            flask.session['pool'] = { 'player' : 0, 'computer' : 0 }

    if (resetWallet is not None or
        'wallet' not in flask.session or
        'pool' not in flask.session):
        flask.session['wallet'] = { 'player' : 0, 'computer' : 0 }
        flask.session['pool'] = { 'player' : 0, 'computer' : 0 }

    if (reset is not None or
        'round' not in flask.session or
        'bets' not in flask.session or
        'cards' not in flask.session or
        'hcards' not in flask.session or
        'ccards' not in flask.session):
        flask.session['round'] = 0
        flask.session['bets'] = ''
        flask.session['cards'] = []
        flask.session['winner'] = -1

        deck = []
        for r in ranks:
            for s in suits:
                deck.append(r + s)

        random.shuffle(deck)

        p0 = []
        p1 = []

        p0.append(deck.pop())
        p1.append(deck.pop())
        p0.append(deck.pop())
        p1.append(deck.pop())

        flask.session['hcards'] = p0
        flask.session['ccards'] = p1

        flask.session['player'] = which

        if which == 0:
            flask.session['wallet']['computer'] -= 2
            flask.session['wallet']['player'] -= 4
            flask.session['pool']['computer'] += 2
            flask.session['pool']['player'] += 4

            computerAction = make_decision(1, flask.session['round'], flask.session['bets'], flask.session['ccards'] + flask.session['cards'])

            make_play(1, computerAction)
        else:
            flask.session['wallet']['computer'] -= 4
            flask.session['wallet']['player'] -= 2
            flask.session['pool']['computer'] += 4
            flask.session['pool']['player'] += 2

        flask.session['deck'] = deck

        #flask.session['percent'] = main.estimate([ai2num(c) for c in p0], [ai2num(c) for c in deck + p1], [])
    flask.session['percent'] = main.estimate([ai2num(c) for c in flask.session['hcards']], [ai2num(c) for c in flask.session['deck'] + flask.session['ccards']], [ai2num(c) for c in flask.session['cards']])        
    return flask.render_template('index.html', data = json.dumps(get_state()))

if __name__ == '__main__':
    app.config['SESSION_TYPE'] = 'filesystem'

    session.init_app(app)
    app.run(debug = True)

