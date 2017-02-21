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
# print p1
# print p1 & 7
# print p1 & 3
print p1 & 0 ^ p1

print p1 ^ 7
print p1 ^ 127

# assert M(['a1']) ^ M(['a2']) == S(['a1', 'a2'])
# # class PolynomeX(object):
# #     # def __new__(cls, *args, **kwargs):
# #     #     new_instance = object.__new__(cls, *args, **kwargs)
# #     #     cls._counter += 1
# #     #     return new_instance
# #     # a2,a1,a0 + 1 = a2a1a0, a2 ^ a1a0, a1 ^ a0, a0 ^ 1
# #     def __init__(self, pol=None):
# #         self.polynome = pol or [[[i]] for i in xrange(31, -1, -1)]

# #     def __repr__(self):
# #         # return str(self._counter)
# #         return '{}'.format(self.polynome)

# #     def __add__(self, value):
# #         if isinstance(value, int):
# #             bint = bin(value)[2:]
# #             return PolynomeX(tuple((('({} + {})'.format(i[0], i[1]) if int(i[1]) else (i[0])) for i in izip(self.polynome, bin(value)[2:].rjust(32, '0')))))

# #     __radd__ = __add__

# #     def __lshift__(self, value):
# #         pass

# #     def __rshift__(self, value):
# #         return 
    
# #     def __and__(self, value):
# #         return PolynomeX(tuple((i[0] if int(i[1]) else '0' for i in izip(self.polynome, bin(value)[2:].rjust(32, '0')))))

