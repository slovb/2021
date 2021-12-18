from dataclasses import dataclass
import math


@dataclass(frozen=True)
class Area:
    xmin: int
    xmax: int
    ymin: int
    ymax: int


@dataclass(frozen=True)
class Projectile:
    vx: int
    vy: int
    x: int = 0
    y: int = 0
    
    def move(self):
        return Projectile(
            x=self.x+self.vx, 
            y=self.y+self.vy, 
            vx=max(0, self.vx - 1), # assume target is positive x, 
            vy=self.vy-1
        )
    
    def is_above(self, area: Area):
        return self.y > area.ymax
    
    def is_inside(self, area: Area):
        return (area.xmin <= self.x <= area.xmax) and (area.ymin <= self.y <= area.ymax)
    
    def is_below(self, area: Area):
        return self.y < area.ymin


def will_hit(vx: int, vy: int, area: Area):
    p = Projectile(vx, vy)
    while p.is_above(area):
        p = p.move()
    while not p.is_below(area):
        if p.is_inside(area):
            return True
        p = p.move()
    return False


def solve(area: Area):
    xmin = int(math.sqrt(2*area.xmin)) - 1
    xmax = area.xmax
    ymin = area.ymin
    ymax = -1-area.ymin # only valid if area is below 0
    count = 0
    # could make this search smarter or make a more effective will_hit
    for y in range(ymin, ymax + 1):
        for x in range(xmin, xmax + 1):
            if will_hit(x, y, area):
                count += 1
    return count


def read(filename):
    with open(filename, 'r') as f:
        row = f.readline().rstrip()
        print(row)
        _, _, xpart, ypart = row.split(' ')
        xpart = xpart.rstrip(',').lstrip('x=')
        ypart = ypart.lstrip('y=')
        xdim = [int(x) for x in xpart.split('..')]
        ydim = [int(y) for y in ypart.split('..')]
        return Area(xmin=min(xdim), xmax=max(xdim), ymin=min(ydim), ymax=max(ydim))


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
