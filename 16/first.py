from __future__ import annotations
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Package:
    version: int
    contents: Literal|Operation
    
    
    def version_sum(self):
        return self.version + self.contents.version_sum()


@dataclass(frozen=True)
class Literal:
    value: int
    
    def version_sum(self):
        return 0


@dataclass(frozen=True)
class Operation:
    op: int
    subpackages: List[Package]
    
    def version_sum(self):
        return sum([p.version_sum() for p in self.subpackages])


def hex2bin(hex):
    conversion = {
        '0': [0,0,0,0],
        '1': [0,0,0,1],
        '2': [0,0,1,0],
        '3': [0,0,1,1],
        '4': [0,1,0,0],
        '5': [0,1,0,1],
        '6': [0,1,1,0],
        '7': [0,1,1,1],
        '8': [1,0,0,0],
        '9': [1,0,0,1],
        'A': [1,0,1,0],
        'B': [1,0,1,1],
        'C': [1,1,0,0],
        'D': [1,1,0,1],
        'E': [1,1,1,0],
        'F': [1,1,1,1],
    }
    output = []
    for h in hex:
        output += conversion[h].copy()
    return output


def bin2dec(bin):
    total = 0
    for i, b in enumerate(bin[::-1]):
        total += b*(2**i)
    return total


def display(binary):
    return ''.join(str(b) for b in binary)


def parse_version(binary):
    return bin2dec(binary[:3:]), binary[3::]


def parse_literal(binary):
    parts = []
    sub = []
    for i, b in enumerate(binary):
        sub.append(b)
        if i % 5 == 4:
            parts += sub[1::]
            if sub[0] == 0:
                return bin2dec(parts), binary[i+1::]
            sub = []


def parse_length(binary):
    lti = binary[0]
    if lti == 0:
        return lti, bin2dec(binary[1:16:]), binary[16::]
    return lti, bin2dec(binary[1:12:]), binary[12::]


def parse_op(binary):
    op = bin2dec(binary[:3:])
    return op, binary[3::]


def parse_package(binary):
    version, binary = parse_version(binary)
    op, binary = parse_op(binary)
    
    # literal
    if op == 4:
        value, binary = parse_literal(binary)
        return Package(version, Literal(value)), binary
    
    # operation
    lti, length, binary = parse_length(binary)
    
    # fixed length
    if lti == 0:
        partial = binary[:length:]
        subpackages = []
        while len(partial) > 0:
            sub, partial = parse_package(partial)
            subpackages.append(sub)
        return Package(version, Operation(op, subpackages)), binary[length::]
    
    # fixed count
    subpackages = []
    for i in range(length):
        sub, binary = parse_package(binary)
        subpackages.append(sub)
    return Package(version, Operation(op, subpackages)), binary


def solve(binary):
    package, _ = parse_package(binary)
    print(package)
    return package.version_sum()


def read(filename):
    with open(filename, 'r') as f:
        row = f.readline().rstrip()
        print(row)
        packet = hex2bin(row)
        return packet


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
