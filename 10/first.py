matching = {
    '(': ')',
    '{': '}',
    '[': ']', 
    '<': '>',
}
points = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}


def score(row):
    state = []
    for c in row:
        if c in matching:
            state.append(c)
        elif len(state) == 0:
            return points(c)
        else:
            o = state.pop()
            if matching[o] != c:
                return points[c]
    return 0


def solve(rows):
    return sum([score(row) for row in rows])


def read(filename):
    with open(filename, 'r') as f:
        rows = [row.rstrip() for row in  f.readlines()]
        return rows


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys
    if (len(sys.argv) < 2):
        print("\n{}".format(main('input.txt')))
    else:
        for f in sys.argv[1:]:
            print("\n{}".format(main(f)))
