bold = lambda s: '\033[1m{}\033[0m'.format(s)


def display(risks, path):
    output = []
    for y, row in enumerate(risks):
        line = []
        for x, risk in enumerate(row):
            if (x, y) in path:
                line.append(bold(risk))
            else:
                line.append(str(risk))
        output.append(''.join(line))
    return '\n'.join(output)



def solve(risks):
    start = (0, 0)
    max_x = len(risks[0]) - 1
    max_y = len(risks) - 1
    goal = (max_x, max_y)
    def adjacent(x, y):
        if x < max_x:
            yield (x + 1, y)
        if y < max_y:
            yield (x, y + 1)
        if x > 0:
            yield (x - 1, y)
        if y > 0:
            yield (x, y - 1)
    
    costs = {start: 0}
    positions = [start]
    paths = {start: [start]}
    while len(positions) > 0:
        pos = positions.pop(0)
        cost = costs[pos]
        path = paths[pos]
        for candidate in adjacent(*pos):
            c = cost + risks[candidate[1]][candidate[0]]
            if candidate not in costs or (candidate in costs and costs[candidate] > c):
                costs[candidate] = c
                positions.append(candidate)
                paths[candidate] = path.copy() + [candidate]
    print(display(risks, paths[goal]))
    return costs[goal]


def read(filename):
    with open(filename, 'r') as f:
        rows = [row.rstrip() for row in f.readlines()]
        risks = [[int(r) for r in row] for row in rows]
        return risks


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys
    if (len(sys.argv) < 2):
        print("\n{}".format(main('input.txt')))
    else:
        for f in sys.argv[1:]:
            print("\n{}".format(main(f)))
