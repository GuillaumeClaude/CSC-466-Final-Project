from math import sqrt, sin
import random

def parse(string, time, destinations, senders):
    spl = string.split()

    results = []

    # Hashing
    if spl[0].startswith('h'):
        rb = calcRB(int(spl[1]))
        for d in destinations:
            nds = []
            #print(d['destination'], 'sender correlations')
            dhash = hash(d['packets'], int(spl[1]), time, rb)
            for s in senders:
                shash = hash(list(map(lambda l:l['time'],
                                   s['packets'])),
                                int(spl[1]), time, rb)
                hd = hammingDistance(dhash, shash)
                #print('sender', s['sender'], hd)
                print(s)
                nds.append({'sender':s['sender'], 'value':hd})
            results.append({'destination':d['destination'], 'senders': nds})
        return results

    else:
        raise Exception('unknown generator')


# =======================================
# PEARSON COR FUNCS
# =======================================

def mean(packets):
    return sum(packets)/len(packets)

def pearson(packetsA, packetsB):
    packetsAB = zip(packetsA, packetsB)
    meanA = mean(packetsA)
    meanB = mean(packetsB)

    num = sum(map(lambda s : (s[0]-meanA)*(s[1]-meanB), packetsAB))
    den = sqrt(sum(map(lambda x : (x-meanA)**2, packetsA))*sum(map(lambda y: (y-meanB)**2, packetsB)))

    return abs(num/den)

# =======================================
# HAMMING COR FUNCS
# =======================================

def timeWindows(packets, N, time):
    tw = time/N
    windows = [0]*N

    for packet in packets:
        print(packet)
        print(packet//tw)
        print(int(packet//tw))
        print(len(windows))
        windows[int(packet//tw)] = 1 + windows[int(packet//tw)]
    return windows

def calcRB(N):
    return list(map(lambda h : random.uniform(-1,1), [0]*N))

def hash(packets, N, time, randomBases):
    tw = time/N
    T = timeWindows(packets, N, time)
    H = [0]*N
    b_j = 0
    for (i, t_i) in enumerate(T):
        t_d = tw*i
        b_i = t_i - b_j
        if i == 0:
            H = list(map(lambda h_i : R(i+1,t_d, randomBases, h_i[0]), enumerate(H)))
        else:
            H = list(map(lambda h_i : h_i[1] + b_i*R(i+1,t_d,randomBases, h_i[0]), enumerate(H)))
        b_j = t_i

    return list(map(lambda x : 1 if x > 0 else 0, H))

def R(i, x, r, j):
   ans = sin(i+x)/5+sin((i+x)*r[j])*r[j]
   return ans

def hammingDistance(h_a, h_b):
    summation = 0
    for (a, b) in zip(h_a, h_b):
        if a != b:
            summation += 1
    return summation

