from heapq import heappush, heappop
from itertools import product


def generate_dice_outcomes():
    totals = {}
    for vals in product(range(1, 4), repeat=3):
        s = sum(vals)
        if s not in totals:
            totals[s] = 0
        totals[s] += 1
    return list(totals.items())


def solve(initial_state):
    dice_outcomes = generate_dice_outcomes()
    counts = { initial_state: 1 }
    heap = []
    heappush(heap, initial_state)
    
    winsP1 = 0
    winsP2 = 0
    while len(heap) > 0:
        if len(heap) > 10*10*21*21*2:
            raise Exception('something is wrong')
        state = heappop(heap)
        count = counts[state]
        _, p1, p2, p1score, p2score, is_p1_turn = state
        
        # check for wins
        if p1score >= 21:
            print(winsP1, winsP2)
            winsP1 += count
            continue
        if p2score >= 21:
            print(winsP1, winsP2)
            winsP2 += count
            continue
        
        # add new states
        for val, multiplier in dice_outcomes:
            if is_p1_turn:
                p = (p1 + val) % 10
                pscore = p1score + p + 1
                neu = (pscore + p2score, p, p2, pscore, p2score, False)
            else:
                p = (p2 + val) % 10
                pscore = p2score + p + 1
                neu = (p1score + pscore, p1, p, p1score, pscore, True)
            if neu not in counts:
                heappush(heap, neu)
                counts[neu] = 0
            counts[neu] += count * multiplier
    return max(winsP1, winsP2)


def read(filename):
    convert = lambda c: 0 if c == '.' else 1
    with open(filename, 'r') as f:
        rows = [row.rstrip() for row in f.readlines()]
        p1 = int(rows[0].split(': ')[1]) - 1 # note adjusted for zeroing
        p2 = int(rows[1].split(': ')[1]) - 1 # note adjusted for zeroing
        return (0, p1, p2, 0, 0, True) # score_sum, count, p1 position, p2 position, p1 score, p2 score, is p1 turn


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
