matching = {
    '(': ')',
    '{': '}',
    '[': ']', 
    '<': '>',
}
points = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}


def score(row):
    state = []
    for c in row:
        if c in matching:
            state.append(c)
        elif len(state) == 0:
            return 0
        else:
            o = state.pop()
            if matching[o] != c:
                return 0
    completion = ''.join([matching[c] for c in state[::-1]])
    total = 0
    for c in completion:
        total = points[c] + 5 * total
    return total


def solve(rows):
    scores = [score(row) for row in rows]
    scores = sorted([score for score in scores if score > 0])
    return scores[(len(scores) // 2)]

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
