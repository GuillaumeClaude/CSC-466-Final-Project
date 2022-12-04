import random

# =======================================
# PACKET LAUNDERING FUNCS
# =======================================

def delay(frq, std, packets, stop):
    return list(filter(lambda x : x < stop, map(lambda h : h + random.gauss(0.2, 0.1), packets)))
