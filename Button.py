import pygame, math, random, os

class Button():
    
    def __init__(self, pozice, rozmery, obrazek, slozka, alpha, funkce = None):
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
        self.NastavFunkci(funkce)
        self.VychoziFunkce = self.funkce

    def nic(self):
        pass

    def NastavFunkci(self, funkce):
        if funkce == None:
            self.funkce = self.nic
        else:
            self.funkce = funkce

    def ResetFunkce(self):
        self.funkce = self.VychoziFunkce

    def Ukazat(self, screen):
        screen.blit(self.obrazek, self.pozice)
       
    def NastavObr(self, obrazek, rozmery, alpha):
        """
        přenastaví obrázek na rozměry (už loadnutý obrázek)
        """
        self.AktObr = obrazek # Aktuální obrázek

        # Zaokrouhluji tady, protože chci mít uložené reálné rozměry
        # zaokrouhluji nahoru, aby nevznikly jednopixelové mezery
        self.obrazek = pygame.transform.smoothscale(obrazek, (math.ceil(rozmery[0]), math.ceil(rozmery[1])))
        self.NastavAlpha(alpha)

    def ZmenObrazekDleIndexu(self, index):
        self.IndexObrazku = index
        self.NastavObr(self.Obrazky[index], self.rozmery, self.alpha)
        
    def NastavAlpha(self, alpha = 255):
        self.alpha = alpha
        self.obrazek.set_alpha(alpha)

    def ZmenAlpha(self, alpha):
        self.NastavAlpha(self.alpha + alpha)
    
    def NastavRozmery(self, noverozmery):
        """
        Nastaví rozměry na vstup a transformuje aktuální obrázek
        """
        self.rozmery = noverozmery
        
        if self.rozmery[0] < 0:
            self.rozmery = (0, self.rozmery[1])

        if self.rozmery[1] < 0:
            self.rozmery = (self.rozmery[0], 0)

        self.NastavObr(self.AktObr, self.rozmery, self.alpha)
            
    def ZmenRozmery(self, zmena):
        """
        zmena: (X, Y)
        """
        self.NastavRozmery((self.rozmery[0] + zmena[0], self.rozmery[1] + zmena[1]))


    def ZmenPozici(self, zmena):
        """
        zmena: (X, Y)
        """
        self.pozice = (self.pozice[0] + zmena[0], self.pozice[1] + zmena[1])

    def MysJeNa(self, pozice):
        """
        Jestli je daná pozice na Buttonu, obdélník
        """
        return self.pozice[0] <= pozice[0] <= self.pozice[0] + self.rozmery[0] and self.pozice[1] <= pozice[1] <= self.pozice[1] + self.rozmery[1]
    
    def StisknutoNa(self, pozice, event, button = 1):
        """
        jestli je myš na Buttonu a je stisknuté určité tlačítko, defaultně levé (1)
        """
        return event.type == pygame.MOUSEBUTTONDOWN and self.MysJeNa(pozice) and event.button == button

    def ImportObr(self, obrazek):
        """
        Importuje obrázek a přidá jej do seznamu obrázků, obrázek neupravuje, vrátí index obrázku v seznamu
        """
        obr = pygame.image.load(os.path.join(self.slozka,  obrazek)).convert()
        self.Obrazky.append(obr)
        return len(self.Obrazky) - 1

