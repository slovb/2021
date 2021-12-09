def solve(heightmap):
    bound_x = len(heightmap[0])
    bound_y = len(heightmap)
    in_bounds = lambda c: 0 <= c[0] < bound_x and 0 <= c[1] < bound_y
    risk = 0
    for y, row in enumerate(heightmap):
        for x, h in enumerate(row):
            adjacents = [c for c in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)] if in_bounds(c)]
            values = [heightmap[y][x] for x, y in adjacents]
            if h < min(values):
                risk += h + 1
    return risk


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
