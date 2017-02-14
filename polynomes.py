from itertools import izip
import copy


class A(object):
    def __init__(self, value):
        self.summands = set((value,),)

    def __xor__(self, value):
        new_a = copy.deepcopy(self)

        if isinstance(value, int) and value == 1:
            new_a.summands.add(1)
        elif isinstance(value, A):
            for i in value.summands:
                if i in self.summands:
                    new_a.summands.remove(i)
                else:
                    new_a.summands.add(i)
        return new_a

    def __and__(self, value):
        new_a = copy.deepcopy(self)
        if isinstance(value, int) and value == 0:
            new_a.summands = set(tuple(),)
        elif isinstance(value, int) and value == 1:
            pass
        else isinstance(value, A):
            for j in self.summands: 
                for i in value.summands:
                    # if i in self.summands:
                        # new_a.summands.remove(i)
                    # else:
                    #     new_a.summands.add(i)
        return new_a
    def __repr__(self):
        return ' ^ '.join([''.join(i for i in j) for j in  self.summands]) or '0'

class PolynomeX(object):
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

