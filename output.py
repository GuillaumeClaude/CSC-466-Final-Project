def parse(string, results):
    spl = string.split()

    # Raw List
    if spl[0].startswith('r'):
        print(results)
        return

    # Ordered
    if spl[0].startswith('o'):
        for d in results:
            print(d['destination'])
            for s in sorted(d['senders'], key=lambda x : x['value']):
                print('\t' + str(s['sender']) + ':', s['value'])
        return

    #CSV
    if spl[0].startswith('c'):
        for d in results:
            print(d['destination'])
            for s in sorted(d['senders'], key=lambda x : x['value']):
                print('\t' + str(s['sender']) + ':', s['value'])
        return

    else:
        raise Exception('unknown generator')
