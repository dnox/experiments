from itertools import izip
import collections
import copy


class M(object):
    def __init__(self, value):
        if value == 1 or value == 0:
            self.multiple = value
        else:
            self.multiple = set(value)

    def __eq__(self, value):
        return (self.multiple == value.multiple) if hasattr(value, 'multiple') else (self.multiple == value)

    def __and__(self, value):
        if value == 0:
            return M(0)
        elif value == 1:
            return M(self.multiple)
        else:
            return M(self.multiple.union(value.multiple))
    
    __rand__ = __and__

    def __repr__(self):
        return ''.join(sorted(self.multiple)) if isinstance(self.multiple, collections.Iterable) else str(self.multiple)

    def __xor__(self, value):
        if value == 0:
            return M(self.multiple)
        elif value == self:
            return 0
        else:
            return S([self, value])
    __rxor__ = __xor__


assert M(0) == 0
assert M(1) == 1
assert M(['a1', 'a2']) == M(['a1', 'a2'])
assert M(['a1', 'a2']) == M(['a1']) & M(['a2'])
assert M(['a1', 'a2']) == M(['a2']) & M(['a1'])
assert M(['a1']) & 1 == M(['a1'])
assert M(['a1']) & 0 == 0
assert M(['a1', 'a2']) & M(['a1']) == M(['a1', 'a2'])


class S(object):
    def __init__(self, summands):
        self.summands = []
        for i in summands:
            if i == 0:
                continue
            if i in self.summands:
                self.summands.pop(summands.index(i))
            else:
                self.summands.append(i)


    def __repr__(self):
        return ' ^ '.join(map(str, self.summands)) or '0'

assert S([1,0]) == 1
assert M(['a1']) ^ M(['a2']) == S(['a1', 'a2'])
# class PolynomeX(object):
#     # def __new__(cls, *args, **kwargs):
#     #     new_instance = object.__new__(cls, *args, **kwargs)
#     #     cls._counter += 1
#     #     return new_instance
#     # a2,a1,a0 + 1 = a2a1a0, a2 ^ a1a0, a1 ^ a0, a0 ^ 1
#     def __init__(self, pol=None):
#         self.polynome = pol or [[[i]] for i in xrange(31, -1, -1)]

#     def __repr__(self):
#         # return str(self._counter)
#         return '{}'.format(self.polynome)

#     def __add__(self, value):
#         if isinstance(value, int):
#             bint = bin(value)[2:]
#             return PolynomeX(tuple((('({} + {})'.format(i[0], i[1]) if int(i[1]) else (i[0])) for i in izip(self.polynome, bin(value)[2:].rjust(32, '0')))))

#     __radd__ = __add__

#     def __lshift__(self, value):
#         pass

#     def __rshift__(self, value):
#         return 
    
#     def __and__(self, value):
#         return PolynomeX(tuple((i[0] if int(i[1]) else '0' for i in izip(self.polynome, bin(value)[2:].rjust(32, '0')))))

