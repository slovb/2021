from dataclasses import dataclass

@dataclass
class Submarine:
    depth = 0
    position = 0
    aim = 0
    
    def forward(self, x):
        self.position += x
        self.depth += x * self.aim

    def down(self, x):
        self.aim += x
    
    def up(self, x):
        self.aim -= x
    
    def product(self):
        return self.depth * self.position


def solve(inputs):
    sub = Submarine()
    for d, x in inputs:
        if d == 'forward':
            sub.forward(x)
        elif d == 'down':
            sub.down(x)
        elif d == 'up':
            sub.up(x)
    return sub.product()


def read(filename):
    with open(filename, 'r') as f:
        lines = [line.rstrip() for line in f.readlines()]
        inputs = []
        for line in lines:
            direction, x = line.split(' ')
            inputs.append((direction, int(x)))
        return inputs

def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys
    if (len(sys.argv) < 2):
        print("\n{}".format(main('input.txt')))
    else:
        for f in sys.argv[1:]:
            print("\n{}".format(main(f)))
