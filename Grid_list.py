import pygame, math

class Grid_list():

    def __init__(self):
        self.list = []

    def Zmen_x(x):
        if x >= 0:
            x = 2 * x
        else:
            x = -1 * 2 * x -1
        return x

    def Zmen_y(y):
        y = y - y % 2
        if y < 0:
            y = - y -1
        return y

    def Nastav(self, pozice, obsah):
        x = Grid_list.Zmen_x(pozice[0])
        y = Grid_list.Zmen_y(pozice[1])

        if x > len(self.list) - 1: # Jestli neexistuje řada, vytvoří ji to
            for _ in range(len(self.list), x + 1):
                self.list.append([])

        if y > len(self.list[x]) - 1:
            for _ in range(len(self.list[x]), y):
                self.list[x].append(None)
            self.list[x].append(obsah)
        else:
            self.list[x][y] = obsah

    def Dostan(self, pozice):
        x = Grid_list.Zmen_x(pozice[0])
        y = Grid_list.Zmen_y(pozice[1])

        if x > len(self.list) - 1 or y > len(self.list[x]) - 1:
            return None

        return self.list[x][y]

    def Dostan_Seznam(self):
        for x in range(0, len(self.list)):
            for obj in self.list[x]:
                if obj != None:
                    yield obj