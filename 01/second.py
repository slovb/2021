def solve(measurements):
    previous = measurements[0]
    count = 0
    for measurement in measurements[1:]:
        if measurement > previous:
            count += 1
        previous = measurement
    return count


def read(filename):
    with open(filename, 'r') as f:
        lines = [int(line.rstrip()) for line in f.readlines()]
        return lines

def main(filename):
    ms = read(filename)
    sliding = [sum(ms[i:i+3]) for i in range(len(ms) - 2)]
    return solve(sliding)


if __name__ == "__main__":
    import sys
    if (len(sys.argv) < 2):
        print("\n{}".format(main('input.txt')))
    else:
        for f in sys.argv[1:]:
            print("\n{}".format(main(f)))
