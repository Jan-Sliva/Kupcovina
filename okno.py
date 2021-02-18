from Button import *

class okno(Button):
    
    Pripona = ".txt"

    def Init_Pozadi(funkce): # dekorátor
        def inner(self, pozice, rozmery, slozka, *args):
            self.pozadi = None
            funkce(self, pozice, rozmery, slozka, *args)
        return inner

    def ZmenPozadi(self, rozmery):
        del self.pozadi
        self.pozadi = pygame.Surface(rozmery)

    def NastavRozmery(self, noverozmery):
        """
        Nastaví rozměry na vstup
        """
        self.rozmery = noverozmery
        
        if self.rozmery[0] < 0:
            self.rozmery = (0, self.rozmery[1])

        if self.rozmery[1] < 0:
            self.rozmery = (self.rozmery[0], 0)
        
        self.NastavObr(self.AktObr, self.rozmery, self.alpha)
        self.ZmenPozadi(self.rozmery)

    def dekor_ukazat(funkce):
        def inner(self, screen):
            funkce(self, screen)
            screen.blit(self.pozadi, self.pozice)
        return inner

