from __future__ import annotations
from dataclasses import dataclass

class Cube:   
    def __init__(self, x_min: int, x_max: int, y_min: int, y_max: int, z_min: int, z_max: int):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.z_min = z_min
        self.z_max = z_max
        self.volume = (x_max + 1 - x_min) * (y_max + 1 - y_min) * (z_max + 1 - z_min)
    
    def has_collision(self, cube: Cube):
        return all([
            self.x_min <= cube.x_max and self.x_max >= cube.x_min,
            self.y_min <= cube.y_max and self.y_max >= cube.y_min,
            self.z_min <= cube.z_max and self.z_max >= cube.z_min,
        ])
        
    def with_change(self, x_min=None, x_max=None, y_min=None, y_max=None, z_min=None, z_max=None):
        return Cube(
            x_min if x_min is not None else self.x_min,
            x_max if x_max is not None else self.x_max,
            y_min if y_min is not None else self.y_min,
            y_max if y_max is not None else self.y_max,
            z_min if z_min is not None else self.z_min,
            z_max if z_max is not None else self.z_max,
        )
        
    def remove(self, cube: Cube) -> list[Cube]:
        out = []
        # above
        if self.z_max > cube.z_max:
            out.append(self.with_change(z_min=cube.z_max+1))
        # below
        if self.z_min < cube.z_min:
            out.append(self.with_change(z_max=cube.z_min-1))
        z_min = max(self.z_min, cube.z_min)
        z_max = min(self.z_max, cube.z_max)
        # front
        if self.x_max > cube.x_max:
            out.append(self.with_change(z_min=z_min, z_max=z_max, x_min=cube.x_max+1))
        # behind
        if self.x_min < cube.x_min:
            out.append(self.with_change(z_min=z_min, z_max=z_max, x_max=cube.x_min-1))
        x_min = max(self.x_min, cube.x_min)
        x_max = min(self.x_max, cube.x_max)
        # left
        if self.y_max > cube.y_max:
            out.append(self.with_change(z_min=z_min, z_max=z_max, x_min=x_min, x_max=x_max, y_min=cube.y_max+1))
        # right
        if self.y_min < cube.y_min:
            out.append(self.with_change(z_min=z_min, z_max=z_max, x_min=x_min, x_max=x_max, y_max=cube.y_min-1))
        return out
    
    def __str__(self) -> str:
        return '{}..{} {}..{} {}..{} ({})'.format(self.x_min, self.x_max, self.y_min, self.y_max, self.z_min, self.z_max, self.volume)


@dataclass
class Instruction:
    action: str
    x_min: int
    x_max: int
    y_min: int
    y_max: int
    z_min: int
    z_max: int
    
    def as_cube(self):
        return Cube(
            x_min=self.x_min, x_max=self.x_max,
            y_min=self.y_min, y_max=self.y_max,
            z_min=self.z_min, z_max=self.z_max,
        )
    
    def execute(self, cubes):
        neu = self.as_cube()
        out = []               
        for cube in cubes:
            if cube.has_collision(neu):
                out += cube.remove(neu)
            else:
                out.append(cube)
        if self.action == 'on':
            out.append(neu)
        return out


def solve(instructions):
    cubes = []
    for instruction in instructions:
        print(instruction)
        cubes = instruction.execute(cubes)
        # for cube in cubes:
        #     print(cube)
        # print(sum([cube.volume for cube in cubes]))
        # print(' ')
    return sum([cube.volume for cube in cubes])


def read(filename):
    with open(filename, 'r') as f:
        rows = [row.rstrip() for row in f.readlines()]
        instructions = []
        for row in rows:
            action, coords = row.split(' ')
            xs, ys, zs = [[int(c) for c in cs.split('=')[1].split('..')] for cs in coords.split(',')]
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
