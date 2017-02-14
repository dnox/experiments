from itertools import izip
import copy


class PolynomeX(object):
    _counter = 0
    # def __new__(cls, *args, **kwargs):
    #     new_instance = object.__new__(cls, *args, **kwargs)
    #     cls._counter += 1
    #     return new_instance
    # a2,a1,a0 + 1 = a2a1a0, a2 ^ a1a0, a1 ^ a0, a0 ^ 1
    def __init__(self, pol=None):
        self.polynome = pol or [[[i]] for i in xrange(31, -1, -1)]

    def __repr__(self):
        # return str(self._counter)
        return '{}'.format(self.polynome)

    def __add__(self, value):
        if isinstance(value, int):
            bint = bin(value)[2:]
            return PolynomeX(tuple((('({} + {})'.format(i[0], i[1]) if int(i[1]) else (i[0])) for i in izip(self.polynome, bin(value)[2:].rjust(32, '0')))))

    __radd__ = __add__

    def __lshift__(self, value):
        pass

    def __rshift__(self, value):
        return 
    
    def __and__(self, value):
        return PolynomeX(tuple((i[0] if int(i[1]) else '0' for i in izip(self.polynome, bin(value)[2:].rjust(32, '0')))))

