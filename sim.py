import json
import correlate
import generate
import laundering
import sys

def addDestination(packets, destination):
    return list(map(lambda p : {'time':p, 'destination': destination}, packets))

def fileTest():
    f = open('sim.json')
    j = json.load(f)

    senders = []
    destinations = []
    packets_out = []
    for s in j['senders']:
        packets = generate.parse(s['generation'], j['time'])
        packets = addDestination(packets, s['destination'])
        senders.append({'sender': s['name'], 'packets': packets.copy()})
        if s['launder']:
            packets = laundering.parse(j['laundering'], j['time'],
                                       j['destinations'], packets)

        packets_out += packets

    packets_out.sort(key=lambda x : x['time'])

    for d in j['destinations']:
        dpackets = list(map(lambda x : x['time'], list(filter(lambda x : x['destination'] == d, packets_out))))
        destinations.append({'destination': d, 'packets': dpackets})

    correlate.parse(j['correlation'], j['time'], destinations, senders)

    f.close()
