import json
import correlate
import generate
import laundering
import output
import sys

def addDestination(packets, destination):
    return list(map(lambda p : {'time':p, 'destination': destination}, packets))

def extractTopSender(result):
    return sorted(result['senders'], key=lambda x : x['value'])[0]['sender']

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
        print(x)
        nres.append(fileTest(j, get_output=True))

    for result in nres:
        tot = list(map(lambda x : str(isCorrelated(j['senders'], x)), result))
        print(list(map(lambda x : isCorrelated(j['senders'], x), result)))
        #print(result)
        #print('=================')
        #print(extractTopSender(result[0]))
        #sender = extractTopSender(result[0])
        #print('=================')
        #print(extractSenderDestination(j['senders'], sender))
        #print('=================')
        #print(j['senders'])
        #if j['senders'][sorted(result['senders'], key=lambda x: x['value'])[0]['sender']] == result['destination']:
        #    print('succ')
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
        senders.append({'sender': s['name'], 'packets': packets.copy()})
        if s['launder']:
            packets = laundering.parse(j['laundering'], j['time'],
                                       j['destinations'], packets)

        packets_out += packets

    packets_out.sort(key=lambda x : x['time'])

    for d in j['destinations']:
        dpackets = list(map(lambda x : x['time'], list(filter(lambda x : x['destination'] == d, packets_out))))
        destinations.append({'destination': d, 'packets': dpackets})

    results = correlate.parse(j['correlation'], j['time'], destinations, senders)

    #output.parse(j['output'], results)

    if get_output:
        return results

nTest(20)
