from functools import reduce


def solve(heightmap):
    bound_x = len(heightmap[0])
    bound_y = len(heightmap)
    explored = set()
    unexplored_in_bounds = lambda c: 0 <= c[0] < bound_x and 0 <= c[1] < bound_y and c not in explored
    results = []
    def explore(x, y):
        v = heightmap[y][x]
        if v == 9:
            return 0
        adjacents = [c for c in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)] if unexplored_in_bounds(c)]
        for a in adjacents:
            explored.add(a)
        return 1 + sum([explore(*a) for a in adjacents])
    for y, row in enumerate(heightmap):
        for x, h in enumerate(row):
            p = (x, y)
            if h == 9 or p in explored:
                continue
            explored.add(p)
            results.append(explore(x, y))
    return reduce(lambda a,b: a*b, sorted(results)[-3:])


def read(filename):
    with open(filename, 'r') as f:
        rows = [row.rstrip() for row in  f.readlines()]
        heightmap = []
        for row in rows:
            heightmap.append([int(h) for h in row])
        return heightmap


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys
    if (len(sys.argv) < 2):
        print("\n{}".format(main('input.txt')))
    else:
        for f in sys.argv[1:]:
            print("\n{}".format(main(f)))
