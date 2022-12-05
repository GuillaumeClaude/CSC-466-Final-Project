import random
import generate

# =======================================
# LAUNDERING PARSE
# =======================================

def parse(string, time, destinations, packets):
    spl = string.split()

    # Delay
    if spl[0].startswith('d'):
        if len(spl) == 3:
            return delay(float(spl[1]), float(spl[2]),
                         packets, time)
        else:
            return delay(float(spl[1]), float(spl[1])/2.0,
                         packets, time)


    # Batch
    elif spl[0].startswith('b'):
        return nBatch(int(spl[1]), packets)

    # Dummies
    elif spl[0].startswith('a'):
        if len(spl) == 3:
            return addDummies(float(spl[1]), float(spl[2]),
                              destinations, packets,
                              time)
        else:
            return addDummies(float(spl[1]), float(spl[1])/2.0,
                              destinations, packets,
                              time)

    else:
        raise Exception('unknown launderer')

# =======================================
# PACKET LAUNDERING FUNCS
# =======================================

def modifyTime(packet, time):
    packet['time'] = time
    return packet

def delay(frq, std, packets, stop):
    lst = list(filter(lambda x : x['time'] < stop, map(lambda h : modifyTime(h, h['time'] + random.gauss(0.2, 0.1)), packets)))
    print(lst)
    return lst

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


