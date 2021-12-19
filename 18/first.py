from __future__ import annotations
from dataclasses import dataclass
from typing import Literal


@dataclass
class Snail:
    left: Snail|Literal = None
    right: Snail|Literal = None
    root: Snail = None
    
    def explode(self, depth=0):
        if depth == 3:
            print('explode {}'.format(str(self)))
            ll = self.left_literal()
            if ll is not None:
                ll.value += self.left.value
            rl = self.right_literal()
            if rl is not None:
                rl.value += self.right.value
            self.replace_with(Literal(0, root=self.root))
            return True
        return self.left.explode(depth + 1) or self.right.explode(depth + 1)
    
    def split(self):
        return self.left.split() or self.right.split()    

    def validate(self):
        if self.left is not None and not (self.left.root == self and self.left.validate()):
            return False
        if self.left is not None and not (self.right.root == self and self.right.validate()):
            return False
        return True
    
    def replace_with(self, neu):
        if self.is_left_of_root():
            self.root.left = neu
        else:
            self.root.right = neu
    
    def is_left_of_root(self):
        if self.root is not None and self.root.left == self:
            return True
        return False
    
    def is_right_of_root(self):
        if self.root is not None and self.root.right == self:
            return True
        return False
    
    def left_literal(self):
        prev = self
        while prev.is_left_of_root():
            prev = prev.root
            if prev.root is None:
                return None
        prev = prev.root.left
        while not isinstance(prev, Literal):
            prev = prev.right
        return prev
    
    def right_literal(self):
        prev = self
        while prev.is_right_of_root():
            prev = prev.root
            if prev.root is None:
                return None
        prev = prev.root.right
        while not isinstance(prev, Literal):
            prev = prev.left
        return prev
    
    def __str__(self) -> str:
        return '[{}, {}]'.format(str(self.left), str(self.right))


@dataclass
class Literal:
    value: int
    root: Snail
    
    def explode(self, depth=0):
        return False
    
    def split(self):
        if self.value > 10:
            print('split {}'.format(str(self)))
            snail = Snail(root=self.root)
            snail.left = Literal(self.value // 2, root=snail)
            snail.right = Literal((self.value + 1) // 2, root=snail)
            self.replace_with(snail)
            return True
        return False
    
    def validate(self):
        return True
    
    def replace_with(self, neu):
        if self.is_left_of_root():
            self.root.left = neu
        else:
            self.root.right = neu
    
    def is_left_of_root(self):
        if self.root is not None and self.root.left == self:
            return True
        return False
    
    def is_right_of_root(self):
        if self.root is not None and self.root.right == self:
            return True
        return False
    
    def __str__(self) -> str:
        return str(self.value)


def solve(snails: list[Snail]):
    for snail in snails:
        print(snail)
        while snail.explode() or snail.split():
            print('-> {}'.format(str(snail)))
            if not snail.validate():
                raise Exception('hell')        
        print('')
    for snail in snails:
        print(snail)
    return 0


def build_snail(row, root=None):
    if not isinstance(row, list):
        return Literal(row, root=root)
    snail = Snail(root=root)
    snail.left = build_snail(row[0], root=snail)
    snail.right = build_snail(row[1], root=snail)
    return snail


def read(filename):
    with open(filename, 'r') as f:
        rows = [eval(row.rstrip()) for row in f.readlines()]
        snails = []
        for row in rows:
            snails.append(build_snail(row))
        return snails


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
