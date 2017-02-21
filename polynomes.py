from itertools import izip, izip_longest
import collections
import copy


class Polynome(object):
    def __init__(self, list_of_sums):
        self.value = list_of_sums

    def __repr__(self):
        return '0' if not self.value else ', '.join(str(i) for i in self.value[::-1])

    def __and__(self, value):
        result = []
        if isinstance(value, int):
            value = map(int, bin(value)[2:][::-1])
        else:
            value = value.value
        for i in izip_longest(self.value, value, fillvalue=0):
            result.append(i[0] & i[1])
        while result and not result[-1]:
            result.pop()
        return Polynome(result)


    def __xor__(self, value):
        result = []
        if isinstance(value, int):
            value = map(int, bin(value)[2:][::-1])
        else:
            value = value.value

        for i in izip_longest(self.value, value, fillvalue=0):
            result.append(i[0] ^ i[1])
        while not result[-1]:
            result.pop()
        return Polynome(result)

    def __add__(self, value):
        if isinstance(value, int):
            value = map(int, bin(value)[2:][::-1])
        else:
            value = value.value

        r = list(self.value)
        for position, item in enumerate(value):
            new_r = r[:position]
            additional = item
            for j in r[position:]:
                new_r.append(j ^ additional) # 1.a3 ^ 1
                additional = j & additional # 1. add = a3
            new_r.append(additional)
            r = new_r
        return Polynome(r)
# (a1, a2, a3) + 1 = (a0 ^ a1a2a3, a1 ^ a2a3, a2 ^ a3, a3 ^ 1)

class M(object):
    def __init__(self, value):
        self.multiple = set(value)

    def __eq__(self, value):
        return (self.multiple == value.multiple) if hasattr(value, 'multiple') else (self.multiple == value)

    def __and__(self, value):
        if isinstance(value, int):
            if value == 0:
                return 0
            elif value == 1:
                return M(self.multiple)
        else:
            return M(set(self.multiple).union(value.multiple))
    
    def __repr__(self):
        return ''.join(sorted(self.multiple)) if isinstance(self.multiple, collections.Iterable) else str(self.multiple)

    __str__ = __repr__
    __rand__ = __and__

class S(object):
    def __init__(self, summands):
        self.summands = list(summands)
        
    def __repr__(self):
        return ' ^ '.join(map(str, self.summands)) or '0'
    __str__ = __repr__
    def __xor__(self, value):
        new_summands = list(self.summands)
        if isinstance(value, int):
            if value == 0:
                pass
            elif value in new_summands:
                new_summands.pop(new_summands.index(value))
            else:
                new_summands.append(value)
            return S(new_summands)
        for x in value.summands:
            if x in new_summands:
                new_summands.pop(new_summands.index(x))
            else:
                new_summands.append(x)
        return S(new_summands)
    __rxor__ = __xor__
    def __and__(self, value):
        if isinstance(value, int):
            if value == 0:
                return 0
            else:
                return S(list(self.summands))

        new_summands = S([])
        for i in self.summands:
            for j in value.summands:
                new_summands ^= S([i&j])
        return new_summands

    __rand__ = __and__

assert M(['a1', 'a2']) == M(['a1', 'a2'])
assert M(['a1', 'a2']) == M(['a1']) & M(['a2'])
assert M(['a1', 'a2']) == M(['a2']) & M(['a1'])
assert M(['a1']) & 1 == M(['a1'])
assert M(['a1']) & 0 == 0
assert M(['a1', 'a2']) & M(['a1']) == M(['a1', 'a2'])

p1 = Polynome([S([M(['a0'])]), S([M(['a1'])]), S([M(['a2'])]), S([M(['a3'])]), S([M(['a4'])])])
print p1
# print p1 & 7
# print p1 & 3
# print p1 & 0 ^ p1

# print p1 ^ 7
# print p1 ^ 127
print p1 + 1
print p1 + 3
print (p1 + p1)

# a4, a3, a2, a1, a0
# a4 ^ a0a1a2a3, a3 ^ a0a1a2, a2 ^ a0a1, a1 ^ a0, a0 ^ 1
# a4 ^ a0a1a2a3 ^ a1a2a3 ^ a0a2a3, a3 ^ a0a1a2 ^ a1a2 ^ a0a2, a2 ^ a0a1 ^ a1 ^ a0, a1 ^ a0 ^ 1, a0 ^ 1

# 22 --- 10110 --- a0 = 1, a1 = 1, a2 = 1, a3 = 1, a4 = 1
# 0, 1, 0, 0, 0, 1, 0
