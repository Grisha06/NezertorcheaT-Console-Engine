import math


class Vector3:
    """3D Vector"""

    def __init__(self, x=0.0, y=0.0, z=0.0):
        if self.__check(x) and self.__check(y) and self.__check(z):
            self.x = x
            self.y = y
            self.z = z
        else:
            raise ValueError("Position is need to be number")

    def __str__(self):
        return f"Vector3(x: {self.x}, y: {self.y}, z: {self.z})"

    def __add__(self, other):
        """Sum of 2 Vectors"""
        return Vector3.sum(self, other)

    def __sub__(self, other):
        """Difference between two Vectors"""
        return Vector3.substr(self, other)

    def __mul__(self, other):
        return Vector3.mult(self, other)

    def __pow__(self, other):
        """Dot product of two Vectors"""
        return Vector3.dot(self, other)

    def __truediv__(self, other):
        """Divide every component of Vector by float"""
        return Vector3.dev_by_float(self, other)

    def __mod__(self, other):
        """Multiple every component of Vector by float"""
        return Vector3.mult_by_float(self, other)

    def returnAsArray(self):
        return [self.x, self.y, self.z]

    def returnAsDict(self):
        return {'x': self.x, 'y': self.y, 'z': self.z}

    @classmethod
    def __check(cls, n):
        return type(n) in (int, float)

    @staticmethod
    def sign_value(a):
        return int(0 < a) - int(a < 0)

    @staticmethod
    def angleB2V(a, b):
        try:
            return math.degrees(math.acos((a ** b) / (Vector3.length(a) * Vector3.length(b))))
        except ZeroDivisionError:
            return 0

    @staticmethod
    def one():
        return Vector3(1, 1, 1)

    @staticmethod
    def zero():
        return Vector3(0)

    @staticmethod
    def dev_by_float(a, n=1):
        return Vector3(a.x / n, a.y / n, a.z / n)

    @staticmethod
    def sum(a, b):
        return Vector3(a.x + b.x, a.y + b.y, a.z + b.z)

    @staticmethod
    def substr(a, b):
        return Vector3(a.x - b.x, a.y - b.y, a.z - b.z)

    @staticmethod
    def lerp(a, b):
        return (a + b) % (1 / 2)

    @staticmethod
    def mult_by_float(a, n=0.0):
        return Vector3(a.x * n, a.y * n, a.z * n)

    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def abs(self):
        return Vector3(math.fabs(self.x), math.fabs(self.y), math.fabs(self.z))

    @staticmethod
    def D2V(degrees):
        return Vector3(float(math.cos(math.radians(degrees))), float(math.sin(math.radians(degrees))))

    @staticmethod
    def reflect(rd, n):
        return rd - ((n % (n ** rd)) % 2)

    def norm(self):
        if self.length() != 0.0:
            return Vector3.dev_by_float(self, self.length())
        else:
            return Vector3.zero()

    @staticmethod
    def dot(a, b):
        return a.x * b.x + a.y * b.y + a.z * b.z

    @staticmethod
    def mult(a, b):
        return Vector3(a.x * b.x, a.y * b.y, a.z * b.z)

    @staticmethod
    def div(a, b):
        return Vector3(a.x / b.x, a.y / b.y, a.z / b.z)

    @staticmethod
    def step(edge, v):
        return Vector3(int(edge.x > v.x), int(edge.y > v.y), int(edge.y > v.y))

    @staticmethod
    def distance(v1, v2):
        return math.sqrt((v1.x - v2.x) ** 2 + (v1.y - v2.y) ** 2 + (v1.z - v2.z) ** 2)

    @staticmethod
    def int(v1):
        return Vector3(int(v1.x), int(v1.y), int(v1.z))

    @staticmethod
    def round(v1):
        return Vector3(round(v1.x), round(v1.y), round(v1.z))

    def sign(self):
        return Vector3(self.sign_value(self.x), self.sign_value(self.y), self.sign_value(self.z))
