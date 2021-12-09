d0 = 'ABCEFG'
d1 = 'CF'
d2 = 'ACDEG'
d3 = 'ACDFG'
d4 = 'BCDF'
d5 = 'ADFG'
d6 = 'ABDEFG'
d7 = 'ACF'
d8 = 'ABCDEFG'
d9 = 'ABCDFG'

def solve(messages):
    total = 0
    for message in messages:
        encoding, data = message
        total += sum([1 for d in data if len(d) in [len(d1), len(d4), len(d7), len(d8)]])
    return total


def read(filename):
    organize = lambda strings: [sorted(s) for s in strings.split(' ')]
    with open(filename, 'r') as f:
        rows = [row.rstrip() for row in  f.readlines()]
        messages = []
        for row in rows:
            left, right = row.split(' | ')
            messages.append((organize(left), organize(right)))
        return messages


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys
    if (len(sys.argv) < 2):
        print("\n{}".format(main('input.txt')))
    else:
        for f in sys.argv[1:]:
            print("\n{}".format(main(f)))
