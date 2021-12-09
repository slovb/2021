class BingoBoard:
    def __init__(self, rows):
        self.rows = rows
        self.marked = []
        values = {}
        for y, row in enumerate(rows):
            for x, val in enumerate(row):
                values[val] = (x, y)
        self.values = values


    def mark(self, value):
        if value in self.values:
            self.marked.append(value)
        return self


    def score(self):
        total = sum([value for value in self.values if value not in self.marked])
        return total * self.marked[-1]


    def has_won(self):
        check = lambda x, y: self.rows[y][x] in self.marked
        for i in range(5):
            if all([check(x, i) for x in range(5)]):
                return True
            if all([check(i, y) for y in range(5)]):
                return True
        # if all([check(i, i) for i in range(5)]):
        #     return True
        # if all([check(4-i, i) for i in range(5)]):
        #     return True
        return False


    def __str__(self) -> str:
        output = []
        for row in self.rows:
            o = []
            for n in row:
                prefix = ''
                if n < 10:
                    prefix = ' '
                value = str(n)
                if n in self.marked:
                    value = '\033[1m{}\033[0m'.format(str(n))
                o.append(prefix + value)
            output.append(' '.join(o))
        return '\n'.join(output)


def solve(numbers, boards):
    for number in numbers:
        print(number)
        reduced = [board for board in boards if not board.mark(number).has_won()] #cursed loop don't do this, works by sideeffects
        if len(reduced) == 0:
            print(boards[0])
            return boards[0].score()
        boards = reduced


def read_bingo_board(lines):
    rows = []
    for line in lines:
        # reduced = list(filter(lambda s: len(s) > 0, line.split(' ')))
        # row = [int(i) for i in reduced]
        row = [int(s) for s in line.split(' ') if len(s) > 0]
        rows.append(row)
    return BingoBoard(rows)


def read(filename):
    with open(filename, 'r') as f:
        lines = [line.rstrip() for line in f.readlines()]
        numbers = [int(i) for i in lines[0].split(',')]
        boards = []
        l = 2
        while l < len(lines):
            boards.append(read_bingo_board(lines[l:l+5]))
            l += 6
        return numbers, boards


def main(filename):
    return solve(*read(filename))


if __name__ == "__main__":
    import sys
    if (len(sys.argv) < 2):
        print("\n{}".format(main('input.txt')))
    else:
        for f in sys.argv[1:]:
            print("\n{}".format(main(f)))
