import random
import generate

# =======================================
# PACKET LAUNDERING FUNCS
# =======================================

def modifyTime(packet, time):
    packet['time'] = time
    return packet

def delay(frq, std, packets, stop):
    return list(filter(lambda x : x['time'] < stop, map(lambda h : modifyTime(h, h['time'] + random.gauss(0.2, 0.1)), packets)))

def nBatch(n, packets):
    npackets = []
    pn=0
    cn=0
    for p in packets:
        cn+=1
        if cn % n == 0:
            npackets += list(map(lambda pk : modifyTime(pk, p['time']), packets[pn:cn]))
            pn = cn

    npackets += list(map(lambda pk : modifyTime(pk, packets[-1]['time']), packets[pn:]))
    return npackets

def addRandomDestinations(packets, destinations):
    return list(map(lambda p : {'time':p, 'destination': random.choice(destinations)}, packets))

def addDummies(frq, std, destinations, packets, stop):
    npackets = addRandomDestinations(generate.timeNormal(frq, std, stop), destinations)
    return sorted((npackets + packets), key=lambda p : p['time'])


