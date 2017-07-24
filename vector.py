import math

class vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return vector(self.x - other.x, self.y - other.y)

    def __mul__(self, c):
        return vector(self.x * c, self.y * c)

    def __div__(self, c):
        return vector(self.x / c, self.y / c)
        
    def __neg__(self):
        return vector(-self.x, -self.y)

    def mod(self):
        return float(math.sqrt(self.x ** 2 + self.y ** 2))

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y

    def __imul__(self, c):
        self.x *= c
        self.y *= c


    def unit(self):
        return self / self.mod()

    def tuple(self):
        return (self.x, self.y)

    def int_tuple(self):
        return map(int, self.tuple())