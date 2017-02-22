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

    def __or__(self, other):
        result = []
        if isinstance(other, int):
            value = map(int, bin(other)[2:][::-1])
        else:
            value = other.value
        for i in izip_longest(self.value, value, fillvalue=0):
            result.append(i[0] | i[1])
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

    def __lshift__(self, other):
        return Polynome([0]*other + list(self.value))

    def __rshift__(self, other):
        return Polynome(self.value[other:])
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
    def __or__(self, other):
        return self ^ other ^ (self & other)
    __ror__ = __or__
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
print p1 >> 2
print p1 + 3
print (p1 + p1)


testp = Polynome([S([M(['a%s' % i])]) for i in xrange(32)])
print testp

ROR = lambda x, y: (((x & 0xffffffff) >> (y & 31)) | (x << (32 - (y & 31)))) & 0xffffffff
Ch = lambda x, y, z: (z ^ (x & (y ^ z)))
Maj = lambda x, y, z: (((x | y) & z) | (x & y))
_S = lambda x, n: ROR(x, n)
_R = lambda x, n: (x & 0xffffffff) >> n
Sigma0 = lambda x: (_S(x, 2) ^ _S(x, 13) ^ _S(x, 22))
Sigma1 = lambda x: (_S(x, 6) ^ _S(x, 11) ^ _S(x, 25))
Gamma0 = lambda x: (_S(x, 7) ^ _S(x, 18) ^ _R(x, 3))
Gamma1 = lambda x: (_S(x, 17) ^ _S(x, 19) ^ _R(x, 10))


print Gamma1(testp)

# 3345589828 / 11000111011010011010011001000100

# a0 = 0, a1 = 0, a2 = 1, a3 = 0, a4 = 0, a5 = 0, a6 = 1, a7 = 0, a8 = 0, a9 = 1, a10 = 1, a11 = 0, a12 = 0, a13 = 1, a14 = 0, a15 = 1,
# a16 = 1, a17 = 0, a18 = 0, a19 = 1, a20 = 0, a21 = 1, a22 = 1, a23 = 0, a24 = 1, a25 = 1, a26 = 1, a27 = 0, a28 = 0,
# a29 = 0, a30 = 1, a31 = 1

# a16 ^ a18, a15 ^ a17, a14 ^ a16, a13 ^ a15, a12 ^ a14, a11 ^ a13, a10 ^ a12, a9 ^ a11, a8 ^ a10, a7 ^ a9, a6 ^ a8 ^ a31, a5 ^ a7 ^ a30, a4 ^ a6 ^ a29, a3 ^ a5 ^ a28, a2 ^ a4 ^ a27, a1 ^ a3 ^ a26, a0 ^ a2 ^ a25, a31 ^ a1 ^ a24, a30 ^ a0 ^ a23, a29 ^ a31 ^ a22, a28 ^ a30 ^ a21, a27 ^ a29 ^ a20, a26 ^ a28 ^ a19, a25 ^ a27 ^ a18, a24 ^ a26 ^ a17, a23 ^ a25 ^ a16, a22 ^ a24 ^ a15, a21 ^ a23 ^ a14, a20 ^ a22 ^ a13, a19 ^ a21 ^ a12, a18 ^ a20 ^ a11, a17 ^ a19 ^ a10



# a0 = 0, a1 = 0, a2 = 1, a3 = 0, a4 = 0, a5 = 0, a6 = 1, a7 = 0, a8 = 0, a9 = 1, a10 = 1, a11 = 0, a12 = 0, a13 = 1, a14 = 0, a15 = 1,
# a16 = 1, a17 = 0, a18 = 0, a19 = 1, a20 = 0, a21 = 1, a22 = 1, a23 = 0, a24 = 1, a25 = 1, a26 = 1, a27 = 0, a28 = 0,
# a29 = 0, a30 = 1, a31 = 1

# 11100111110110110010000100110000
