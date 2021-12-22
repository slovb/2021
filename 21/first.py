class Dice:
    def __init__(self) -> None:
        self.i = 0
        self.count = 0
    
    def roll(self) -> int:
        out = self.i + 1
        self.i = out % 100
        self.count += 1
        return out
    
    def roll_3(self) -> int:
        return sum([self.roll() for _ in range(3)])
        

def solve(a, b):
    score_a = 0
    score_b = 0
    dice = Dice()
    while True:
        a = (a + dice.roll_3()) % 10
        score_a += a + 1
        if score_a >= 1000:
            break
        b = (b + dice.roll_3()) % 10
        score_b += b + 1
        if score_b >= 1000:
            break
    return dice.count * min(score_a, score_b)


def read(filename):
    convert = lambda c: 0 if c == '.' else 1
    with open(filename, 'r') as f:
        rows = [row.rstrip() for row in f.readlines()]
        p1 = int(rows[0].split(': ')[1]) - 1 # note adjusted for zeroing
        p2 = int(rows[1].split(': ')[1]) - 1 # note adjusted for zeroing
        return p1, p2


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
