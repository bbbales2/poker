#%%
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

print val(0.75, False, 'cr', 3, 0, 2, 4)
# 0

#print 0, val(0.5, True, 'rrf', 3)
# 8