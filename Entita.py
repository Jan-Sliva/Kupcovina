from ObjektNaMape import *
from Button import *

class Entita(map_obj, Button):
    
    def dekor_init(funkce):
        def inner(self, PoziceNaMape, ObjektGrid, AktualizFunk, PomerStran, obrazek_figurky, slozka, *args):
            self.slozka = slozka
            self.alpha = 255
            self.Obrazky = []
            x = self.ImportObr(obrazek_figurky)
            self.AktObr = self.Obrazky[x]

            self.PomerStran = PomerStran
            
            self.Grid.SeznamHracu.append(self)
            funkce(self, PoziceNaMape, ObjektGrid, AktualizFunk, PomerStran, obrazek_figurky, slozka, *args)
            
            self.NastavPoziciNaMape_Poprve = True
            self.NastavPoziciNaMape(PoziceNaMape)
            self.Zvyraz = -self.AktPole.ZvyrazHrace # zvýraznění, když má být hráč zvýryzněn

            self.AktPole.OdkryjVedlejsi(self.Aktualizovat)
        return inner

    def ImportObr(self, obrazek):
        """
        Importuje obrázek a přidá jej do seznamu obrázků, obrázek neupravuje, vrátí index obrázku v seznamu
        """
        obr = pygame.image.load(os.path.join(self.slozka,  obrazek)).convert()
        obr.set_colorkey((0, 0, 0))
        self.Obrazky.append(obr)
        return len(self.Obrazky) - 1

    @map_obj.Update_dekor
    def NastavPoziciNaMape(self, PoziceNaMape):
        """
        upraví pozici a rozměry dle políčka, pořadí na políčku a velikosti mřížky
        formát pořadí (kolikátý je na tom políčku):
        (A, B) = A z B
        """
        policko = self.Grid.SeznamPolicek.Dostan(PoziceNaMape)
        policko_existuje = policko != None

        if policko_existuje or self.NastavPoziciNaMape_Poprve:
            if not self.NastavPoziciNaMape_Poprve:
                self.AktPole.Odeber(self)
                policko.Pridej(self)
                SeznamSeznamuEntit = [self.AktPole.SeznamHracu, policko.SeznamHracu]
            elif not policko_existuje:
                policko = self.Grid.create_tile(PoziceNaMape, self.Aktualizovat)
                seznam = policko.SeznamHracu.copy()
                seznam.append(self)
                SeznamSeznamuEntit = [seznam] # metodu Pridej() zavolám až nakonec, protože vyžaduje, aby už byl initován obrázek, což dělá až metoda NastavRozmery()
            else:
                seznam = policko.SeznamHracu.copy()
                seznam.append(self)
                SeznamSeznamuEntit = [seznam]

            self.AktPole = policko
        
            for SeznamEntitNaPolicku in SeznamSeznamuEntit: # upravuju i políčko, z kterého odcházím
        
                for index in range(len(SeznamEntitNaPolicku)):
                    entita = SeznamEntitNaPolicku[index]
                    poradi = (index + 1, len(SeznamEntitNaPolicku))

                    # uspořádání do čtverce
                    # na daném políčku (počty entit)
                    entita.delka_radku = math.ceil(math.sqrt(poradi[1]))
                    entita.pocet_radku = math.ceil(poradi[1]/entita.delka_radku)

                    if (entita.pocet_radku - 1) * entita.delka_radku < poradi[0]: # jestli je to poslední řádek, tak zarovnání do řádku je jiné
                        delka_daneho_radku = poradi[1] - ((entita.pocet_radku - 1) * entita.delka_radku)
                    else: # jinak je stejné
                        delka_daneho_radku = entita.delka_radku

                    # nastavení rozměrů
                    x = min((entita.Grid.RozmeryPole[0] / 2) / entita.delka_radku, (entita.Grid.RozmeryPole[1] / 2) / entita.pocet_radku * entita.PomerStran)
                    entita.NastavRozmery((x, x / entita.PomerStran))

                    entita.PoziceNaPolicku = ((- 0.5 * delka_daneho_radku * entita.rozmery[0] + ((poradi[0]-1) % entita.delka_radku) * entita.rozmery[0]) / entita.Grid.RozmeryPole[0],
                                            ( - 0.5 * entita.pocet_radku * entita.rozmery[1] + math.floor((poradi[0]-1) / entita.delka_radku)* entita.rozmery[1]) / entita.Grid.RozmeryPole[1])

                    entita.UpdatePozice()

            if self.NastavPoziciNaMape_Poprve:
                self.AktPole.Pridej(self)
                self.NastavPoziciNaMape_Poprve = False

    def UpdatePoziceRozmery(self):
        """
        přenastaví rozměry a pozici hráče podle aktuální (self) pozice na mapě a pořadí na políčku
        """
        # nastavení rozměrů
        x = min((self.Grid.RozmeryPole[0] / 2) / self.delka_radku, (self.Grid.RozmeryPole[1] / 2) / self.pocet_radku * self.PomerStran)
        self.NastavRozmery((x, x / self.PomerStran))

        self.UpdatePozice()

    def UpdatePozice(self):
        """
        přenastaví pozici hráče podle aktuální (self) pozice na mapě a pořadí na políčku
        """
        # nastavení pozice
        # přičítám 0.5 od PoziceNaMape, abych se dostal do středu políčka, ne do levého horního rohu
        pozice_stredu_policka = (self.Grid.centrum[0] + self.AktPole.PoziceNaMape[0]*self.Grid.VzdalenostiPoli[0] + 0.5*self.Grid.RozmeryPole[0],
                                 self.Grid.centrum[1] + self.AktPole.PoziceNaMape[1]*self.Grid.VzdalenostiPoli[1] + 0.5*self.Grid.RozmeryPole[1])

        self.pozice = (pozice_stredu_policka[0] + self.PoziceNaPolicku[0] * self.Grid.RozmeryPole[0],
                       pozice_stredu_policka[1] + self.PoziceNaPolicku[1] * self.Grid.RozmeryPole[1])

    def Ukazat(self):
        self.Grid.pozadi.blit(self.obrazek, self.pozice)

    def ZmenPoziceNaMape(self, zmena):
        self.NastavPoziciNaMape((self.AktPole.PoziceNaMape[0] + zmena[0], self.AktPole.PoziceNaMape[1] + zmena[1]))
        