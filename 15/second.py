from heapq import heappush, heappop


bold = lambda s: '\033[1m{}\033[0m'.format(s)


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
    positions = []
    heappush(positions, (0, 0, start))
    while len(positions) > 0:
        cost, steps, pos = heappop(positions)
        for candidate in adjacent(*pos):
            c = cost + risks[candidate[1]][candidate[0]]
            if candidate not in costs or (candidate in costs and costs[candidate] > c):
                costs[candidate] = c
                heappush(positions, (c, steps + 1, candidate))
    return costs[goal]


def read(filename):
    inc = lambda r, i: r + i if r + i <= 9 else r + i - 9
    with open(filename, 'r') as f:
        rows = [row.rstrip() for row in f.readlines()]
        risks = [[int(r) for r in row] for row in rows]
        
        # fatten
        for row in risks:
            extra_cols = []
            for i in range(1, 5):
                extra_cols += [inc(r, i) for r in row]
            row += extra_cols
        # lengthen
        extra_rows = []
        for i in range(1, 5):
            for row in risks:
                extra_rows.append([inc(r, i) for r in row])
        risks += extra_rows
        return risks


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import time
    start_time = time.time()
    import sys
    if (len(sys.argv) < 2):
        print("\n{}".format(main('input.txt')))
    else:
        for f in sys.argv[1:]:
            print("\n{}".format(main(f)))
    print('--- %s seconds ---' % (time.time() - start_time))
