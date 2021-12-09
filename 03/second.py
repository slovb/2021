zero_picker = lambda i: lambda bin: bin[i] == 0
ones_picker = lambda i: lambda bin: bin[i] == 1


def count(bins, i):
    zeroes, ones = 0, 0
    for bin in bins:
        if bin[i] == 0:
            zeroes += 1
        else:
            ones += 1
    return zeroes, ones


def oxygen_rating(bins, i=0):
    if len(bins) == 1:
        return bins[0]
    zeroes, ones = count(bins, i)
    if zeroes > ones:
        bins = list(filter(zero_picker(i), bins))
    else:
        bins = list(filter(ones_picker(i), bins))
    return oxygen_rating(bins, i + 1)


def scrubber_rating(bins, i=0):
    if len(bins) == 1:
        return bins[0]
    zeroes, ones = count(bins, i)
    if zeroes <= ones:
        bins = list(filter(zero_picker(i), bins))
    else:
        bins = list(filter(ones_picker(i), bins))
    return scrubber_rating(bins, i + 1)


def solve(bins):
    oxygen = oxygen_rating(bins)
    scrubber = scrubber_rating(bins)
    print(oxygen)
    print(scrubber)
    return bin2dec(oxygen) * bin2dec(scrubber)


def bin2dec(bin):
    d = 0
    for e, b in enumerate(bin[::-1]):
        d += b * 2**e
    return d


def read(filename):
    with open(filename, 'r') as f:
        lines = [line.rstrip() for line in f.readlines()]
        bins = [[int(i) for i in line] for line in lines]
        return bins

def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys
    if (len(sys.argv) < 2):
        print("\n{}".format(main('input.txt')))
    else:
        for f in sys.argv[1:]:
            print("\n{}".format(main(f)))
