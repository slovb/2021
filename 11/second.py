from itertools import product

class State:
    def __init__(self, state):
        self.state = state
        self.count = 0
        self.limit_x = len(state[0])
        self.limit_y = len(state)
        self.to_flash = []
        self.has_flashed = set()
        self.finished = False
    
    def adjacent(self, x, y):
        xs = [p for p in [x - 1, x, x + 1] if 0 <= p < self.limit_x]
        ys = [p for p in [y - 1, y, y + 1] if 0 <= p < self.limit_y]
        return product(xs, ys)

    def increment(self, x, y):
        self.state[y][x] += 1
        if self.state[y][x] > 9:
            self.to_flash.append((x, y))

    def flash(self, x, y):
        if (x, y) in self.has_flashed:
            return
        self.has_flashed.add((x, y))
        for p in self.adjacent(x, y):
            self.increment(*p)
    
    def step(self):
        self.count += 1
        for y in range(self.limit_y):
            for x in range(self.limit_x):
                self.increment(x, y)
        while len(self.to_flash) > 0:
            x, y = self.to_flash.pop()
            self.flash(x, y)
        for x, y in self.has_flashed:
            self.state[y][x] = 0
        if len(self.has_flashed) == self.limit_x * self.limit_y:
            self.finished = True
        self.has_flashed = set()

    
    def __str__(self):
        return '\n'.join([''.join([str(c) for c in row]) for row in self.state])



def solve(state):
    print(state)
    print()
    while not state.finished:
        state.step()
        print(state)
        print()
    return state.count


def read(filename):
    with open(filename, 'r') as f:
        rows = [[int(c) for c in row.rstrip()] for row in f.readlines()]
        return State(rows)


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys
    if (len(sys.argv) < 2):
        print("\n{}".format(main('input.txt')))
    else:
        for f in sys.argv[1:]:
            print("\n{}".format(main(f)))
