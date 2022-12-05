import correlate
import copy
import generate
import json
import laundering
import numpy as np
import output
import sys
import random

def addDestination(packets, destination):
    return list(map(lambda p : {'time':p, 'destination': destination}, packets))

def extractTopSender(result):
    senders = result['senders'].copy()
    random.shuffle(senders) # Shuffle to prevent ORDER BIAS
    return sorted(senders, key=lambda x : x['value'])[0]['sender']

def extractSenderDestination(senders, sender):
    for s in senders:
        if s['name'] == sender:
            return s['destination']

def isCorrelated(senders, flow):
    if extractSenderDestination(senders, extractTopSender(flow)) == flow['destination']:
        return 1
    else:
        return 0

def nTest(n):
    f = open('sim.json')
    j = json.load(f)
    nres = []
    for x in range(0,n):
        nres.append(fileTest(j, get_output=True))

    tot = []
    for result in nres:
        tot.append(list(map(lambda x : isCorrelated(j['senders'], x), result)))

    tot = list(map(str, np.array(tot).mean(axis=0)))
    print(tot)

    nf = open('sim.csv', 'a')
    nf.write(','.join(tot)+',\n')
    nf.close()

    f.close()

def fileTest(j, get_output=False):

    senders = []
    destinations = []
    packets_out = []
    for s in j['senders']:
        packets = generate.parse(s['generation'], j['time'])
        packets = addDestination(packets, s['destination'])
        npackets = copy.deepcopy(packets)
        senders.append({'sender': s['name'], 'packets': npackets})
        if s['launder']:
            packets = laundering.parse(j['laundering'], j['time'],
                                       j['destinations'], packets)

        packets_out += packets

    packets_out.sort(key=lambda x : x['time'])

    for d in j['destinations']:
        dpackets = list(map(lambda x : x['time'], list(filter(lambda x : x['destination'] == d, packets_out))))
        destinations.append({'destination': d, 'packets': dpackets})

    results = correlate.parse(j['correlation'], j['time'], destinations, senders)

    if get_output:
        return results

nTest(50)
