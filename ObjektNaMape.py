import pygame, math, random

class map_obj():
    
    okoli = ((1, 1), (-1, 1), (1, -1), (-1, -1), (0, 2), (0, -2))

    def ZmenPoziceNaMape(self, zmena):
        self.PoziceNaMape = (self.PoziceNaMape[0] + zmena[0], self.PoziceNaMape[1] + zmena[1])

    def dekor_init(funkce):
        def inner(self, PoziceNaMape, ObjektGrid, AktualizFunk, *args):
            """
            AktualizFunk - funkce, která se zavolá, vždy, když se změní nějaký údaj od tohoto map_obj, argumenty jsou tento map_obj, použít pro aktualizaci lišt
            """
            self.zvyrazneno = False
            self.Aktualizovat = AktualizFunk
            self.Grid = ObjektGrid
            funkce(self, PoziceNaMape, ObjektGrid, AktualizFunk, *args)
        return inner

    def Update_dekor(funkce):
        def inner(self, *args):
            funkce(self, *args)
            self.Aktualizovat(self)
        return inner
