from dataclasses import dataclass


@dataclass(frozen=True)
class Area:
    xmin: int
    xmax: int
    ymin: int
    ymax: int


def solve(area: Area):
    return ((-area.miny) - 1) * (-area.miny) // 2 # is math cheating?


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
