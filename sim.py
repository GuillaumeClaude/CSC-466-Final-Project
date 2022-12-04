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

# =======================================
# TESTING
# =======================================

def test():
    i = 0

    for x in range(5):
        p_S = generate.timeNormal(3.0, 5.0, 5000)
        p_sd = laundering.delay(100.0, 50.0, p_S, 5000)
        p_a = generate.timeNormal(3.0, 5.0, 5000)
        p_b = generate.timeBurst(40.0, 10.0, 4.1, 0.1, 0.1, 0.1, 5000)

        print('pearson a a_d', correlate.pearson(p_S, p_sd))
        print('pearson a b', correlate.pearson(p_S, p_a))

        rb = correlate.calcRB(1000)
        hsa = correlate.hash(p_S, 1000, 5000, rb)
        hsb = correlate.hash(p_sd,1000, 5000, rb)
        hsc = correlate.hash(p_a, 1000, 5000, rb)
        hsd = correlate.hash(p_b, 1000, 5000, rb)

        a=correlate.hammingDistance(hsa, hsb)
        b=correlate.hammingDistance(hsa, hsc)
        c=correlate.hammingDistance(hsa, hsd)

        print('a,b', correlate.hammingDistance(hsa, hsb))
        print('a,c', correlate.hammingDistance(hsa, hsc))
        print('a,d', correlate.hammingDistance(hsa, hsd))

        if a < b and a < c:
            i+=1

    print(i)

fileTest()
