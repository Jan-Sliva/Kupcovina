from ButtonNaListe import *

class Posuvnik(ButtonNaListe):

    def __init__(self, PoziceNaListe, rozmery, obrazek, obrazekPosuvniku, sirkaPosuvniku, rozmeziPosuvniku, alpha, ObjektLista, dalsi_radek = False):
        
        self.Lista = ObjektLista

        self.dalsi_radek = dalsi_radek # jestli je na dalším řádku

        self.posunuti = 0
        self.rozmezi = rozmeziPosuvniku
        self.sirkaPosuvniku = sirkaPosuvniku
        self.udaj = rozmeziPosuvniku[0]
        
        self.Posun_started = False
        self.PoziceMysiNaPosuvniku = 0

        self.PoziceNaListe = PoziceNaListe
        self.NextOnLine = self.PoziceNaListe[0] == "next" # jestli je to následující text na stejném řádku
        
        self.alpha = alpha
        self.Obrazky = [] # Sem se ukládají obrázky
        
        x = self.ImportObr(obrazek)
        self.AktObr = self.Obrazky[x]

        x = self.ImportObr(obrazekPosuvniku)
        self.AktObrPosuvniku = self.Obrazky[x]

        self.NastavRozmery(rozmery)

        self.maxPosunuti = self.rozmery[0] - self.sirkaPosuvniku

    def Ukazat(self):
        self.Lista.pozadi.blit(self.obrazek, self.pozice)
        self.Lista.pozadi.blit(self.obrazekPosuvniku, (self.pozice[0] + self.posunuti, self.pozice[1]))

    def NastavObr(self, obrazek, obrazekPosuvniku, rozmery, sirkaPosuvniku, alpha):
        """
        přenastaví obrázek na rozměry (už loadnutý obrázek)
        """
        self.AktObr = obrazek # Aktuální obrázek
        self.AktObrPosuvniku = obrazekPosuvniku # Aktuální obrázek posuvníku

        # Zaokrouhluji tady, protože chci mít uložené reálné rozměry
        # zaokrouhluji nahoru, aby nevznikly jednopixelové mezery
        self.obrazek = pygame.transform.smoothscale(obrazek, (math.ceil(rozmery[0]), math.ceil(rozmery[1])))
        self.obrazekPosuvniku = pygame.transform.smoothscale(obrazekPosuvniku, (math.ceil(sirkaPosuvniku), math.ceil(rozmery[1])))
        self.NastavAlpha(alpha)
        
    def NastavAlpha(self, alpha = 255):
        self.alpha = alpha
        self.obrazek.set_alpha(alpha)
        self.obrazekPosuvniku.set_alpha(alpha)

    def NastavRozmery(self, noverozmery):
        """
        Nastaví rozměry na vstup a transformuje aktuální obrázek
        """
        self.rozmery = noverozmery
        
        if self.rozmery[0] < 0:
            self.rozmery = (0, self.rozmery[1])

        if self.rozmery[1] < 0:
            self.rozmery = (self.rozmery[0], 0)

        self.NastavObr(self.AktObr, self.AktObrPosuvniku, self.rozmery, self.sirkaPosuvniku, self.alpha)

    def NastavPosunuti(self, noveposunuti):
        self.posunuti = noveposunuti
        if self.posunuti < 0:
            self.posunuti = 0
        elif  self.posunuti > self.maxPosunuti:
            self.posunuti = self.maxPosunuti

    def start_Posun(self, mouse_sirka):
        self.Posun_started = True
        self.PoziceMysiNaPosuvniku = mouse_sirka  - self.Lista.pozice[0] - self.pozice[0]- self.posunuti 

    def Posun(self, mouse_sirka):
        if self.Posun_started:
            mouse_sirka -= self.Lista.pozice[0] + self.pozice[0]
            self.NastavPosunuti(mouse_sirka - self.PoziceMysiNaPosuvniku)
            self.Lista.Aktualizovat()
            self.PrenastavUdaj()

    def end_Posun(self):
        self.Posun_started = False

    def Aktivovat(self):
        self.posunuti = 0
        self.PrenastavUdaj()
        self.end_Posun()
        self.Lista.SeznamAktivovanychPosuvnik.append(self)
        if not self.NextOnLine:
            self.UpdatePozice()

    def PrenastavUdaj(self):
        self.udaj = round(self.posunuti / self.maxPosunuti * (self.rozmezi[1] - self.rozmezi[0]) + self.rozmezi[0])

    def MysJeNaPosuvnik(self, pozice):
       """
       Jestli je daná pozice na Posuvník, obdélník
       """
       PoziceNaScreen = (self.pozice[0] + self.posunuti + self.Lista.pozice[0], self.pozice[1] + self.Lista.pozice[1])
       return PoziceNaScreen[0] <= pozice[0] <= PoziceNaScreen[0] + self.sirkaPosuvniku and PoziceNaScreen[1] <= pozice[1] <= PoziceNaScreen[1] + self.rozmery[1]

    def StisknutoNaPosuvnik(self, pozice, event, button = 1):
        """
        jestli je myš na Posuvník a je stisknuté určité tlačítko, defaultně levé (1)
        """
        return event.type == pygame.MOUSEBUTTONDOWN and self.MysJeNaPosuvnik(pozice) and event.button == button

    def NastavRozmezi(self, noverozmezi):
        self.rozmezi = noverozmezi
        self.PrenastavUdaj()
        if self in self.Lista.SeznamAktivovanychPosuvnik:
            self.Lista.Aktualizovat()
            self.posunuti = 0