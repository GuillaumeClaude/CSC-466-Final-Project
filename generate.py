import random

# =======================================
# PACKET PARSE
# =======================================

def parse(string, time):
    spl = string.split(',')

    # Constant
    if spl[0].startswith('c'):
        return timeConstant(float(spl[1]), time)

    # Normal
    elif spl[0].startswith('n'):
        if len(spl) == 3:
            return timeNormal(float(spl[1]), float(spl[2]),
                              time)
        else:
            return timeNormal(float(spl[1]), float(spl[1])/2.0,
                              time)

    # OnOff
    elif spl[0].startswith('o'):
        if len(spl) == 5:
            return timeOnOff(float(spl[1]), float(spl[2]),
                             float(spl[3]), float(spl[4]),
                             time)
        else:
            return timeOnOff(float(spl[1]), float(spl[1])/2.0,
                             float(spl[2]), float(spl[2])/2.0,
                             time)

    # Burst
    elif spl[0].startswith('b'):
        if len(spl) == 7:
            return timeOnOff(float(spl[1]), float(spl[2]),
                             float(spl[3]), float(spl[4]),
                             float(spl[5]), float(spl[6]),
                             time)
        else:
            return timeOnOff(float(spl[1]), float(spl[1])/2.0,
                             float(spl[2]), float(spl[2])/2.0,
                             float(spl[3]), float(spl[3])/2.0,
                             time)

    else:
        raise Exception('unknown generator')


# =======================================
# PACKET GENERATION FUNCS
# =======================================

# Constant packet generation
def timeConstant(frq,stop):
    packets = []
    time = 0.0

    while True:
        time += frq

        if time >= stop:
            return packets

        packets.append(time)

# Packet generation time based on a normal distribution
def timeNormal(frq,std,stop):
    packets = []
    time = 0.0

    while True:
        time += abs(random.gauss(mu=frq, sigma=std))
        if time >= stop:
            return packets

        packets.append(time)

# Packet generation time based on on-off distribution
def timeOnOff(interval_frq,interval_std,packet_frq,packet_std,stop):
    packets = []
    time = 0.0

    while True:
        # ON
        interval_stop = time + abs(random.gauss(mu=interval_frq,sigma=interval_std))
        while True:
            ntime = abs(random.gauss(mu=packet_frq, sigma=packet_std))
            if (ntime + time) >= interval_stop or (ntime + time) > stop:
                break
            time += ntime
            packets.append(time)

        # OFF
        if time >= stop:
            return packets
        time += abs(random.gauss(mu=interval_frq,sigma=interval_std))

# For simulating bursty traffic
def timeBurst(off_frq,off_std,on_frq,on_std,packet_frq,packet_std,stop):
    packets = []
    time = 0.0

    while True:
        # ON
        interval_stop = time + abs(random.gauss(mu=on_frq,sigma=on_std))
        while True:
            ntime = abs(random.gauss(mu=packet_frq, sigma=packet_std))
            if (ntime + time) > interval_stop or (ntime + time) > stop:
                break
            time += ntime
            packets.append(time)

        # OFF
        if time > stop:
            return packets
        time += abs(random.gauss(mu=off_frq,sigma=off_std))

