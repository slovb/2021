from __future__ import annotations
from dataclasses import dataclass
from typing import List
from abc import ABC
from functools import reduce
import operator


class Operation(ABC):
    def evaluate(self):
        pass


@dataclass(frozen=True)
class Package(Operation):
    version: int
    operation: Operation
    
    def evaluate(self):
        return self.operation.evaluate()


@dataclass(frozen=True)
class Literal(Operation):
    value: int
    
    def evaluate(self):
        return self.value


@dataclass(frozen=True)
class Sum(Operation):
    subpackages: List[Package]
    
    def evaluate(self):
        return sum([p.evaluate() for p in self.subpackages])


@dataclass(frozen=True)
class Product(Operation):
    subpackages: List[Package]
    
    def evaluate(self):
        return reduce(operator.mul, [p.evaluate() for p in self.subpackages])


@dataclass(frozen=True)
class Minimum(Operation):
    subpackages: List[Package]
    
    def evaluate(self):
        return min([p.evaluate() for p in self.subpackages])


@dataclass(frozen=True)
class Maximum(Operation):
    subpackages: List[Package]
    
    def evaluate(self):
        return max([p.evaluate() for p in self.subpackages])


@dataclass(frozen=True)
class GreatherThan(Operation):
    subpackages: List[Package]
    
    def evaluate(self):
        if self.subpackages[0].evaluate() > self.subpackages[1].evaluate():
            return 1
        return 0


@dataclass(frozen=True)
class LessThan(Operation):
    subpackages: List[Package]
    
    def evaluate(self):
        if self.subpackages[0].evaluate() < self.subpackages[1].evaluate():
            return 1
        return 0


@dataclass(frozen=True)
class EqualsTo(Operation):
    subpackages: List[Package]
    
    def evaluate(self):
        if self.subpackages[0].evaluate() == self.subpackages[1].evaluate():
            return 1
        return 0


def generate_operation(op, contents):
    if op == 0:
        return Sum(contents)
    elif op == 1:
        return Product(contents)
    elif op == 2:
        return Minimum(contents)
    elif op == 3:
        return Maximum(contents)
    elif op == 4:
        return Literal(contents)
    elif op == 5:
        return GreatherThan(contents)
    elif op == 6:
        return LessThan(contents)
    elif op == 7:
        return EqualsTo(contents)


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
    binary = binary[3::]
    
    # literal
    if op == 4:
        value, binary = parse_literal(binary)
        operation = generate_operation(op, value)
        return generate_operation(op, value), binary
    
    # operation
    lti, length, binary = parse_length(binary)
    
    # fixed length
    if lti == 0:
        partial = binary[:length:]
        subpackages = []
        while len(partial) > 0:
            sub, partial = parse_package(partial)
            subpackages.append(sub)
        return generate_operation(op, subpackages), binary[length::]
    
    # fixed count
    subpackages = []
    for _ in range(length):
        sub, binary = parse_package(binary)
        subpackages.append(sub)
    return generate_operation(op, subpackages), binary


def parse_package(binary):
    version, binary = parse_version(binary)
    op, binary = parse_op(binary)
    return Package(version, op), binary


def solve(binary):
    package, _ = parse_package(binary)
    print(package)
    return package.evaluate()


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
