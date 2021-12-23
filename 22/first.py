from dataclasses import dataclass

clamp = lambda x: min(50, max(-50, x))


@dataclass
class Instruction:
    action: str
    x_min: int
    x_max: int
    y_min: int
    y_max: int
    z_min: int
    z_max: int
    
    def execute(self, memory):
        if any([self.x_min == self.x_max, self.y_min == self.y_max, self.z_min == self.z_max]):
            return
        if self.action == 'on':
            run = lambda p: memory.add(p)
        else:
            run = lambda p: memory.discard(p)
        for x in range(self.x_min, 1 + self.x_max):
            for y in range(self.y_min, 1 + self.y_max):
                for z in range(self.z_min, 1 + self.z_max):
                    run((x, y, z))


def solve(instructions):
    memory = set()
    for instruction in instructions:
        instruction.execute(memory)
        print(instruction, len(memory))
    return len(memory)


def read(filename):
    with open(filename, 'r') as f:
        rows = [row.rstrip() for row in f.readlines()]
        instructions = []
        for row in rows:
            action, coords = row.split(' ')
            xs, ys, zs = [[clamp(int(c)) for c in cs.split('=')[1].split('..')] for cs in coords.split(',')]
            instructions.append(Instruction(
                action=action,
                x_min=xs[0], x_max=xs[1],
                y_min=ys[0], y_max=ys[1],
                z_min=zs[0], z_max=zs[1],
            ))
        return instructions

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
