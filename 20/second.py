class Karta:
    def __init__(self, is_lit):
        self.min_x = None
        self.max_x = None
        self.min_y = None
        self.max_y = None
        self.minority = set()
        self.is_lit = is_lit # is the infinite lit?
    
    def add(self, x, y):
        self.minority.add((x, y))
        if self.min_x is None or x < self.min_x:
            self.min_x = x
        if self.max_x is None or x > self.max_x:
            self.max_x = x
        if self.min_y is None or y < self.min_y:
            self.min_y = y
        if self.max_y is None or y > self.max_y:
            self.max_y = y

    def getKey(self, x, y):
        adjacent = [
            (x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
            (x - 1, y    ), (x, y    ), (x + 1, y    ),
            (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]
        total = 0
        for i, c in enumerate(adjacent[::-1]):
            if c in self.minority:
                if not self.is_lit:
                    total += 2**i
            elif self.is_lit:
                total += 2**i
        return total
    
    def __str__(self) -> str:
        rows = []
        minority_symbol = '#' if not self.is_lit else '.'
        majority_symbol = '.' if not self.is_lit else '#'
        for y in range(self.min_y-2, self.max_y+3):
            row = []
            for x in range(self.min_x-2, self.max_x+3):
                if (x, y) in self.minority:
                    row.append(minority_symbol)
                else:
                    row.append(majority_symbol)
            rows.append(''.join(row))
        return '\n'.join(rows)


def enhance(karta, rules):
    is_lit = karta.is_lit
    if karta.is_lit and rules[511] == 0:
        is_lit = False
    elif not karta.is_lit and rules[0] == 1:
        is_lit = True
    ny = Karta(is_lit)
    minority_value = 1 if not is_lit else 0
    for y in range(karta.min_y-4, karta.max_y+6):
        for x in range(karta.min_x-4, karta.max_x+6):
            key = karta.getKey(x, y)
            if rules[key] == minority_value:
                ny.add(x, y)
    return ny


def solve(karta, rules):
    print(karta)
    print('')
    for _ in range(50):
        karta = enhance(karta, rules)
        print(karta)
        print('')
    return len(karta.minority)


def read(filename):
    convert = lambda c: 0 if c == '.' else 1
    with open(filename, 'r') as f:
        rows = [row.rstrip() for row in f.readlines()]
        rules = [convert(c) for c in rows[0]]
        karta = Karta(is_lit=False)
        for y, row in enumerate(rows[2::]):
            for x, c in enumerate(row):
                if c == '#':
                    karta.add(x, y)
        return karta, rules


def main(filename):
    return solve(*read(filename))


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
