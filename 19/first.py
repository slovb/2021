from __future__ import annotations
from itertools import permutations, product


def generate_rotators():
    for a,b,c in product([-1, 1], repeat=3):
        for i,j,k in permutations([0, 1, 2]):
            yield lambda d: tuple([a*d[i], b*d[j], c*d[k]])

class Scanner:
    def __init__(self, id, beacons) -> None:
        self.id = id
        self.beacons = beacons

    def align_beacons(self, beacons) -> list:
        best_score = -1
        best_beacons = []
        for rotator in generate_rotators():
            for fixpoint in beacons:
                fr = rotator(fixpoint)
                for candidate in self.beacons:
                    aligner = lambda b: (
                        b[0] + candidate[0] - fr[0],
                        b[1] + candidate[1] - fr[1],
                        b[2] + candidate[2] - fr[2],
                    )
                    score = sum([1 for b in beacons if aligner(rotator(b)) in self.beacons])
                    if score > best_score:
                        best_score = score
                        best_beacons = [aligner(rotator(b)) for b in beacons]
        return best_score, best_beacons
    
    def __str__(self) -> str:
        output = ['---  scanner {}  ---'.format(self.id)]
        for b in self.beacons:
            output.append(' ' + ''.join([str(v).rjust(6) for v in b]))
        return '\n'.join(output)


def solve(scanners: list[Scanner]):
    final_beacons = set()
    fixed = [scanners.pop(0)]
    print(fixed[0])
    for b in fixed[0].beacons:
        final_beacons.add(b)
    print('')
    
    while len(scanners) > 0:
        if len(fixed) == 0:
            raise Exception('bleh')
        new_fixed = []
        to_remove = set()
        for fix, scanner in product(fixed, scanners):
            if scanner.id in to_remove:
                continue
            score, aligned_beacons = fix.align_beacons(scanner.beacons)
            print(score)
            if score >= 12:
                to_remove.add(scanner.id)
                neu = Scanner(scanner.id, aligned_beacons)
                print(neu)
                new_fixed.append(neu)
                for b in neu.beacons:
                    final_beacons.add(b)
                print('total', len(final_beacons))
        fixed = new_fixed
        scanners = [scan for scan in scanners if scan.id not in to_remove]        
    return len(final_beacons)


def read(filename):
    with open(filename, 'r') as f:
        rows = [row.rstrip() for row in f.readlines()]
        scanners = []
        beacons = []
        id = 0
        for row in rows:
            if '---' in row:
                continue
            if row == '':
                scanners.append(Scanner(id, beacons))
                id += 1
                beacons = []
            else:
                beacons.append(tuple([int(v) for v in row.split(',')]))
            
        return scanners


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
