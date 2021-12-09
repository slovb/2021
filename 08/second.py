import itertools

from copy import copy

digits = [
    'ABCEFG',
    'CF',
    'ACDEG',
    'ACDFG',
    'BCDF',
    'ABDFG',
    'ABDEFG',
    'ACF',
    'ABCDEFG',
    'ABCDFG',
]


def finder(length, encoding):
    for enc in encoding:
        if len(enc) == length:
            return enc


def unique_digit_reducer(i, possibilities, encoding):
    digit = finder(len(digits[i]), encoding)
    for key, poss in possibilities.items():
        if key in digit: # filter out the possibilities that are taken by the unique digit
            possibilities[key] = [p for p in poss if p in digits[i]]
        else:
            possibilities[key] = [p for p in poss if p not in digits[i]]


def looper(possibilities):
    chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    for options in itertools.product(*possibilities.values()):
        if len(set(options)) < len(chars): # unique combinations only
            continue
        mapping = { char:option for char, option in zip(chars, options) }
        yield(mapping)


def translate_encoding(encoding, candidate):
    mapping = {}
    for code in encoding:
        digit = ''.join(sorted([candidate[c] for c in code]))
        if digit not in digits:
            return None
        mapping[code] = digits.index(digit)
    return mapping


def decode(encoding):
    options = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    possibilities = {   
        'a': copy(options),
        'b': copy(options),
        'c': copy(options),
        'd': copy(options),
        'e': copy(options),
        'f': copy(options),
        'g': copy(options),
    }
    for i in [1, 4, 7, 8]: # 8 probably doesn't do anything
        unique_digit_reducer(i, possibilities, encoding) # this is just an optimization, doesn't effect correctness
    for candidate in looper(possibilities):
        mapping = translate_encoding(encoding, candidate)
        if mapping is not None:
            return mapping


def solve(messages):
    total = 0
    for message in messages:
        encoding, data = message
        mapping = decode(encoding)
        value = int(''.join([str(mapping[d]) for d in data]))
        print('{}: {}'.format(str(value).rjust(4), message))
        total += value
    return total


def read(filename):
    organize = lambda strings: [''.join(sorted(s)) for s in strings.split(' ')] # sorted so they can be comparable
    with open(filename, 'r') as f:
        rows = [row.rstrip() for row in f.readlines()]
        messages = []
        for row in rows:
            left, right = row.split(' | ')
            messages.append((organize(left), organize(right)))
        return messages


def main(filename):
    return solve(read(filename))


if __name__ == "__main__":
    import sys
    if (len(sys.argv) < 2):
        print("\n{}".format(main('input.txt')))
    else:
        for f in sys.argv[1:]:
            print("\n{}".format(main(f)))
