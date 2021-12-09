from dataclasses import dataclass

@dataclass
class Line:
    start: tuple
    stop: tuple
    
    def isVertical(self):
        return self.start[0] == self.stop[0]
    
    def isHorizontal(self):
        return self.start[1] == self.stop[1]
    
    def isCardinal(self):
        return self.isVertical() or self.isHorizontal()
    
    def d(self, i):
        if self.start[i] < self.stop[i]:
            return 1
        elif self.start[i] > self.stop[i]:
            return -1
        return 0
    
    def dx(self):
        return self.d(0)
    
    def dy(self):
        return self.d(1)
    
    def points(self):
        dx = self.dx()
        dy = self.dy()
        x, y = self.start
        while (x, y) != self.stop:
            yield (x, y)
            x += dx
            y += dy
        yield (x, y)


def solve(lines):
    lines = [line for line in lines if line.isCardinal()]
    space = {}
    for line in lines:
        for p in line.points():
            if p not in space:
                space[p] = 0
            space[p] += 1
    return len([p for p in space if space[p] > 1])


def read(filename):
    parter = lambda coord: tuple(int(c) for c in coord.split(','))
    with open(filename, 'r') as f:
        rows = [row.rstrip() for row in f.readlines()]
        lines = []
        for row in rows:
            left, _, right = row.split(' ')
            lines.append(Line(parter(left), parter(right)))
        return lines
            
        


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys
    if (len(sys.argv) < 2):
        print("\n{}".format(main('input.txt')))
    else:
        for f in sys.argv[1:]:
            print("\n{}".format(main(f)))
