import flask
import os
import sys
import socket
import random
import flask.ext.session
import json

def make_decision(player, roundNumber, bets, cards):
    raises = 0

    bets = bets.split('/')[-1]

    if len(bets) > 0:
        if bets[0] == 'r':
            for b in bets[1:]:
                if b == 'r':
                    raises += 1
        else:
            for b in bets[2:]:
                if b == 'r':
                    raises += 1
    
    goesfirst = (player == 1 and roundNumber == 0) or (player == 0 and roundNumber > 0)

    print raises, bets

    if (len(bets) == 0 and goesfirst) or (not goesfirst and len(bets) == 1 and bets[0] == 'c'):
        choices = ['c', 'r']
    elif raises == 3:
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
             'hcards' : flask.session['hcards'] }

def computer_play():
    pass

def make_play(player, action):
    if flask.session['winner'] > -1:
        return

    flask.session['bets'] += action

    if action == 'f':
        flask.session['winner'] = 1 - player
        return 'next'

    raises = 0

    bets = flask.session['bets'].split('/')[-1]

    if len(bets) > 1 and action == 'c':
        if flask.session['round'] == 0:
            flask.session['cards'].append(flask.session['deck'].pop())
            flask.session['cards'].append(flask.session['deck'].pop())
            flask.session['cards'].append(flask.session['deck'].pop())
        elif flask.session['round'] == 1:
            flask.session['cards'].append(flask.session['deck'].pop())
        elif flask.session['round'] == 2:
            flask.session['cards'].append(flask.session['deck'].pop())
        elif flask.sesion['round'] == 3:
            flask.session['winner'] = random.randint(0, 1)

        flask.session['round'] += 1
        flask.session['bets'] += '/'

        return 'next'

    return None

@app.route('/play')
def play():
    action = flask.request.args.get('action', None)

    ret = make_play(0, action)

    if not ret:
        computerAction = make_decision(1, flask.session['round'], flask.session['bets'], flask.session['ccards'] + flask.session['cards'])

        make_play(1, computerAction)
    
    return flask.json.jsonify(state = get_state())

@app.route('/')
def index():
    reset = flask.request.args.get('reset', None)

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

        ranks = '23456789TJQKA'
        suits = 'shdc'

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

        computerAction = make_decision(1, flask.session['round'], flask.session['bets'], flask.session['ccards'] + flask.session['cards'])

        make_play(1, computerAction)

        flask.session['deck'] = deck
        
    return flask.render_template('index.html', data = json.dumps(get_state()))

if __name__ == '__main__':
    app.config['SESSION_TYPE'] = 'filesystem'

    session.init_app(app)
    app.run(debug = True)

