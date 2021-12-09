def step(fish):
    f = {}
    for a in fish:
        c = fish[a]
        if a == 0:
            a = 7
            f[8] = c
        if a - 1 not in f:
            f[a - 1] = 0
        f[a - 1] += c
    return f


def solve(fish):
    for i in range(256):
        print('{}: {}'.format(str(i).rjust(3), str(fish)))
        fish = step(fish)
    return sum([fish[k] for k in fish])


def read(filename):
    with open(filename, 'r') as f:
        row = f.readline().rstrip()
        numbers = [int(n) for n in row.split(',')]
        fish = {}
        for n in numbers:
            if n not in fish:
                fish[n] = 0
            fish[n] += 1
        return fish


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys
    if (len(sys.argv) < 2):
        print("\n{}".format(main('input.txt')))
    else:
        for f in sys.argv[1:]:
            print("\n{}".format(main(f)))
