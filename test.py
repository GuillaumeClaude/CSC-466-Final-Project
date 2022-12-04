import correlate
import generate
import laundering
import sim

# Various tests

def ntest():
    packetsa = sim.addDestination(generate.timeNormal(2, 2, 100), 'A')
    packetsb = sim.addDestination(generate.timeConstant(2, 100), 'B')

    print('A')
    print(packetsa)
    print('B')
    print(laundering.nBatch(10, packetsa))

    # print('A+B')
    # combined = packetsa + packetsb
    # print(sorted(combined, key=lambda p : p['time']))

    # print('with dummies')
    # print(laundering.addDummies(2.0, 1.0, ['A', 'B'], combined, 100))

ntest()
