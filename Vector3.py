class Vec3:
    """Трёхмерный вектор"""

    def __init__(self, x=0.0, y=0.0, z=0.0):
        if self.__check(x) and self.__check(y) and self.__check(z):
            self.x = x
            self.y = y
            self.z = z
        else:
            raise ValueError("Position is need to be number")

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
    def one():
        return Vec3(1, 1, 1)

    @staticmethod
    def zero():
        return Vec3(0)

    @staticmethod
    def dev_by_float(a, n=1):
        return Vec3(a.x / n, a.y / n, a.z / n)

    @staticmethod
    def sum(a, b):
        return Vec3(a.x + b.x, a.y + b.y, a.z + b.z)

    @staticmethod
    def substr(a, b):
        return Vec3(a.x - b.x, a.y - b.y, a.z - b.z)

    @staticmethod
    def mult_by_float(a, n=0.0):
        return Vec3(a.x * n, a.y * n, a.z * n)

    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def abs(self):
        return Vec3(fabs(self.x), fabs(self.y), fabs(self.z))

    @staticmethod
    def reflect(rd, n):
        return Vec3.substr(rd, Vec3.mult_by_float(n, Vec3.dot(n, rd) * 2))

    def norm(self):
        if self.length() != 0.0:
            return Vec3.dev_by_float(self, self.length())
        else:
            return Vec3.zero()

    @staticmethod
    def dot(a, b):
        return a.x * b.x + a.y * b.y + a.z * b.z

    @staticmethod
    def mult(a, b):
        return Vec3(a.x * b.x, a.y * b.y, a.z * b.z)

    @staticmethod
    def div(a, b):
        return Vec3(a.x / b.x, a.y / b.y, a.z / b.z)

    @staticmethod
    def step(edge, v):
        return Vec3(int(edge.x > v.x), int(edge.y > v.y), int(edge.y > v.y))

    @staticmethod
    def distance(v1, v2):
        return math.sqrt((v1.x - v2.x) ** 2 + (v1.y - v2.y) ** 2 + (v1.z - v2.z) ** 2)

    @staticmethod
    def int(v1):
        return Vec3(int(v1.x), int(v1.y), int(v1.z))

    @staticmethod
    def round(v1):
        return Vec3(round(v1.x), round(v1.y), round(v1.z))

    def sign(self):
        return Vec3(self.sign_value(self.x), self.sign_value(self.y), self.sign_value(self.z))