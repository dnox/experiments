from itertools import izip

class PolynomeX(object):
    _counter = 0
    # def __new__(cls, *args, **kwargs):
    #     new_instance = object.__new__(cls, *args, **kwargs)
    #     cls._counter += 1
    #     return new_instance
    
    def __init__(self, pol=None):
        self.polynome = pol or tuple((('a%s' % i, i) for i in xrange(31, -1, -1)))

    def __repr__(self):
        # return str(self._counter)
        return '{}'.format(self.polynome)

    def __add__(self, value):
        return PolynomeX(tuple((('({} + {})'.format(i[0][0], i[1]), i[0][1]) if int(i[1]) else (i[0][0], i[0][1]) for i in izip(self.polynome, bin(value)[2:].rjust(32, '0')))))

    __radd__ = __add__

    def __lshift__(self, value):
        pass

    def __and__(self, value):
        return PolynomeX(tuple((((i[0][0] if int(i[1]) else '0', i[0][1]) for i in izip(self.polynome, bin(value)[2:].rjust(32, '0'))))))