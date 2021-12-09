def distance(i, crabs):
    return sum([abs(i - c) for c in crabs])
    

def solve(crabs):
    a = min(crabs)
    b = max(crabs)
    return min([distance(i, crabs) for i in range(a, b)])


def read(filename):
    with open(filename, 'r') as f:
        row = f.readline().rstrip()
        numbers = [int(n) for n in row.split(',')]
        return numbers


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys
    if (len(sys.argv) < 2):
        print("\n{}".format(main('input.txt')))
    else:
        for f in sys.argv[1:]:
            print("\n{}".format(main(f)))
