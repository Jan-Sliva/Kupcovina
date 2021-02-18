from Button import *

class ButtonNaListe(Button):

    def __init__(self, PoziceNaListe, rozmery, obrazek, funkce, alpha, ObjektLista, dalsi_radek = False):
        
        self.Lista = ObjektLista

        self.dalsi_radek = dalsi_radek # jestli je na dalším řádku

        self.PoziceNaListe = PoziceNaListe
        self.NextOnLine = self.PoziceNaListe[0] == "next"
        
        self.alpha = alpha
        self.Obrazky = [] # Sem se ukládají obrázky
        x = self.ImportObr(obrazek)
        self.AktObr = self.Obrazky[x]
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

    def UpdatePozice(self):
        self.pozice = (self.PoziceNaListe[0] + self.Lista.odsazeni[0], 
                       self.PoziceNaListe[1] + self.Lista.posunuti + self.Lista.odsazeni[1])

    def Ukazat(self):
        self.Lista.pozadi.blit(self.obrazek, self.pozice)

    def Aktivovat(self):
        self.Lista.SeznamAktivovanychButton.append(self)
        if not self.NextOnLine:
            self.UpdatePozice()

    def MysJeNa(self, pozice):
       """
       Jestli je daná pozice na Buttonu, obdélník
       """
       PoziceNaScreen = (self.pozice[0] + self.Lista.pozice[0], self.pozice[1] + self.Lista.pozice[1])
       return PoziceNaScreen[0] <= pozice[0] <= PoziceNaScreen[0] + self.rozmery[0] and PoziceNaScreen[1] <= pozice[1] <= PoziceNaScreen[1] + self.rozmery[1]

    def ImportObr(self, obrazek, alpha = 255):
        """
        Importuje obrázek a přidá jej do seznamu obrázků, obrázek neupravuje, vrátí index obrázku v seznamu
        """
        obr = pygame.image.load(os.path.join(self.Lista.slozka, "Obrazky",  obrazek))
        obr.set_alpha(alpha)
        self.Obrazky.append(obr)
        return len(self.Obrazky) - 1;