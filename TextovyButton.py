from Button import *

class TextovyButton(Button):
    def __init__(self, pozice, rozmery, obrazek, slozka, alpha, vychoztext, obrazekkurzoru):
        """
        pozice, rozmery: (X, Y)
        obrazek: název
        """
        self.slozka = slozka
        self.pozice = pozice
        self.alpha = alpha
        self.Obrazky = [] # Sem se ukládají obrázky
        self.IndexObrazku = self.ImportObr(obrazek)
        self.AktObr = self.Obrazky[self.IndexObrazku]
        self.NastavRozmery(rozmery)
        self.Font = pygame.font.SysFont("arial", round(rozmery[1] * 2/3))
        self.VychozText = vychoztext
        self.Psano = False
        self.NastavText(self.VychozText)
        self.funkce = self.ZacitPsat

        obr = pygame.image.load(os.path.join(self.slozka,  obrazekkurzoru))
        self.Kurzor = pygame.transform.smoothscale(obr, (round(0.5 * rozmery[1]), round(rozmery[1])))

    def Ukazat(self, screen):
        UkazObr = self.obrazek.copy()
        UkazObr.blit(self.ObrazText, (0, round(1/6 * self.rozmery[1])))
        if self.Psano:
            UkazObr.blit(self.Kurzor, (self.DelkaText, 0))
        screen.blit(UkazObr, self.pozice)


    def NastavText(self, text):
        self.Text = text
        self.ObrazText = self.Font.render(self.Text, True, (0, 0, 0))
        self.DelkaText = self.Font.size(self.Text)[0]

    def ZacitPsat(self):
        self.Psano = True

    def Napis(self, text):
        if self.Psano:
            self.NastavText(self.Text + text)

    def Vymaz(self):
        if self.Psano and not self.Text == "":
            self.NastavText(self.Text[:-1])

    def UkoncitPsat(self):
        self.Psano = False

    def ResetText(self):
        self.UkoncitPsat()
        self.NastavText(self.VychozText)



