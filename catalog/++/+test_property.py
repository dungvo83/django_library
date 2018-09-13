class C:
    def __init__(self):
        self._x = None

    def getx(self):
        return self._x

    def setx(self, value):
        self._x = value

    def delx(self):
        del self._x

    x = property(getx, setx, delx, " I'm the x property. ")


c = C()

c.x = 10
print(c.x)
# print('%r', c.x.__doc__) ???


class Parrot:
    def __init__(self):
        self._voltage = 10000

    @property
    def voltage(self):
        """Get the current voltage."""
        return self._voltage


a = Parrot()
print('Parrot: ', a.voltage)


class D:
    def __init__(self):
        self._x = None

    @property  # getter
    def x(self):
        """I'm the 'x' property."""
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @x.deleter
    def x(self):
        del self._x


d = D()
d.x = 123
print(d.x)
del d.x
print(d.x)
