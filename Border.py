class Border:
    """Representation of border like symbol image"""
    def __init__(self):
        self.width = 5
        self.height = 5
        self.border_r = '│'
        self.border_l = '│'
        self.border_u = '─'
        self.border_d = '─'
        self.border_angle_rd = '┘'
        self.border_angle_dl = '└'
        self.border_angle_lu = '┌'
        self.border_angle_ur = '┐'

    def get(self):
        f = []
        f.append([])
        f[0].append(self.border_angle_lu)
        for j in range(self.width):
            f[0].append(self.border_u)
        f[0].append(self.border_angle_ur)
        for i in range(1, self.height):
            f.append([])
            f[i].append(self.border_l)
            for j in range(self.width):
                f[i].append(" ")
            f[i].append(self.border_r)
        f.append([])
        f[self.height].append(self.border_angle_dl)
        for j in range(self.width):
            f[self.height].append(self.border_d)
        f[self.height].append(self.border_angle_rd)
        return f
