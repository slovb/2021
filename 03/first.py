def solve(bins):
    l = len(bins[0])
    gamma = []
    epsilon = []
    for i in range(l):
        ones = 0
        zeros = 0
        for bin in bins:
            if bin[i] == '1':
                ones += 1
            else:
                zeros += 1
        if ones > zeros:
            gamma.append(1)
            epsilon.append(0)
        else:
            gamma.append(0)
            epsilon.append(1)
    g = binToDec(gamma)
    e = binToDec(epsilon)
    print(gamma, g)
    print(epsilon, e)
    return g * e

def binToDec(bin):
    d = 0
    for e, b in enumerate(bin[::-1]):
        d += b * 2**e
    return d


def read(filename):
    with open(filename, 'r') as f:
        lines = [line.rstrip() for line in f.readlines()]
        return lines

def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys
    if (len(sys.argv) < 2):
        print("\n{}".format(main('input.txt')))
    else:
        for f in sys.argv[1:]:
            print("\n{}".format(main(f)))
