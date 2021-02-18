from ObjektNaMape import *
from Funkce import *
from Faze import *
from Posuvnik import *


class tile(map_obj):

    
    def dekor_init(funkce):
        def inner(self, PoziceNaMape, ObjektGrid, AktualizFunk, *args):            
            self.PoziceNaMape = PoziceNaMape
            self.SeznamHracu = []
            self.ZvyrazHrace = -32 # změna alphy hráče
            self.ZvyrazOstatPoli = -96 # změna alphy ostatních polí, když je toto pole zvýrazněný
            self.NastavAlpha(255)
            self.Grid.SeznamPolicek.Nastav(PoziceNaMape, self)
            self.UpdatePozice()
            funkce(self, PoziceNaMape, ObjektGrid, AktualizFunk, *args)
        return inner

    def UpdatePozice(self):
        self.pozice = (self.Grid.centrum[0] + self.PoziceNaMape[0]*self.Grid.VzdalenostiPoli[0],
                       self.Grid.centrum[1] + self.PoziceNaMape[1]*self.Grid.VzdalenostiPoli[1])

    def NastavAlpha(self, alpha):
        for hrac in self.SeznamHracu:
            hrac.ZmenAlpha(alpha - self.alpha)
        self.alpha = alpha
        

    def ZmenAlpha(self, alpha):
        self.NastavAlpha(self.alpha + alpha)

    def Zvyraznit(self):
        for policko in self.Grid.SeznamPolicek.Dostan_Seznam():
            policko.ZmenAlpha(self.ZvyrazOstatPoli)
        self.AlphaPredZvyraz = self.alpha
        self.NastavAlpha(255)
        self.zvyrazneno = True

    def Odzvyraznit(self):
        for policko in self.Grid.SeznamPolicek.Dostan_Seznam():
            policko.ZmenAlpha(-self.ZvyrazOstatPoli)
        self.ZmenAlpha(-255 + self.AlphaPredZvyraz)
        self.zvyrazneno = False

    def Pridej(self, hrac):
        self.SeznamHracu.append(hrac)
        hrac.ZmenAlpha(-255 + self.alpha + self.ZvyrazHrace)

    def Odeber(self, hrac):
        self.SeznamHracu.remove(hrac)
        hrac.ZmenAlpha(255 - self.alpha - self.ZvyrazHrace)

    def ZmenPoziceNaMape(self, zmena):
        self.NastavPoziceNaMape((self.PoziceNaMape[0] + zmena[0], self.PoziceNaMape[1] + zmena[1]))

    @map_obj.Update_dekor
    def NastavPoziceNaMape(self, PoziceNaMape):
        dalsi_pole = self.Grid.SeznamPolicek.Dostan(PoziceNaMape)
        self.Grid.SeznamPolicek.Nastav(PoziceNaMape, self)
        self.Grid.SeznamPolicek.Nastav(self.PoziceNaMape, dalsi_pole)
        if dalsi_pole != None:
            dalsi_pole.PoziceNaMape = self.PoziceNaMape
            dalsi_pole.UpdatePozice()
            dalsi_pole.SeznamHracu, self.SeznamHracu = self.SeznamHracu, dalsi_pole.SeznamHracu
            self.Aktualizovat(dalsi_pole)
            for hrac in self.SeznamHracu:
                hrac.AktPole = self
            for hrac in dalsi_pole.SeznamHracu:
                hrac.AktPole = dalsi_pole
        
        self.PoziceNaMape = PoziceNaMape
        self.UpdatePozice()
        if self.SeznamHracu != []:
            for hrac in self.SeznamHracu:
                hrac.UpdatePozice()

    def OdkryjVedlejsi(self, AktualizFunk):
        for vedle in map_obj.okoli:
            self.Grid.create_tile((self.PoziceNaMape[0] + vedle[0], self.PoziceNaMape[1] + vedle[1]), AktualizFunk)

class normal_tile(tile):
    @map_obj.dekor_init
    @tile.dekor_init
    def __init__(self, PoziceNaMape, ObjektGrid, AktualizFunk):
        self.narocnost = random.randint(1,3)
        self.typ_obr = f"norm{self.narocnost}"
        self.typ_text = "Policko"
        if self.narocnost == 1:
            self.Jmeno = "Nížiny"
        elif self.narocnost == 2:
            self.Jmeno = "Kopce"
        elif self.narocnost == 3:
            self.Jmeno = "Hory"

class treasure_tile(tile):
    @map_obj.dekor_init
    @tile.dekor_init
    def __init__(self, PoziceNaMape, ObjektGrid, AktualizFunk):
        self.narocnost = 3
        self.typ_obr = "trea"
        self.typ_text = "Policko"
        self.Jmeno = "Poklad"

    def DostatPoklad(self, hrac, ObjektLista):
        MaxHedvabi = Funkce.Faze.HracNaTahu.MaxHedvabi - Funkce.Faze.HracNaTahu.hedvabi
        MaxSul = Funkce.Faze.HracNaTahu.MaxSul - Funkce.Faze.HracNaTahu.sul
        MaxSuroviny = MaxHedvabi + MaxSul

        self.DostatHedvabi = 0
        self.DostatSul = 0
        self.DostatSuroviny = random.randint(2, 3)

        write_text = []

        for _ in range(0, min(MaxSuroviny, self.DostatSuroviny)):
            typ = random.randint(0, 1)
            loop_quit = False
            while not loop_quit:
                if typ == 0 and MaxHedvabi > 0:
                    self.DostatHedvabi += 1
                    loop_quit = True
                elif typ == 1 and MaxSul > 0:
                    self.DostatSul += 1
                    loop_quit = True
                else:
                    typ = (typ + 1) % 2

        if self.DostatHedvabi >= 1:
             write_text.append("    {objekt.DostatHedvabi} hedvábí")
        if self.DostatSul == 1:
            write_text.append("    {objekt.DostatSul} sůl")
        elif self.DostatSul > 1:
            write_text.append("    {objekt.DostatSul} soli")

        if self.DostatSuroviny > MaxSuroviny:
            self.DostatPenize = random.randint(3, 7) + (self.DostatSuroviny - MaxSuroviny) * 3
        else:
            self.DostatPenize = random.randint(3, 7)

        if self.DostatPenize <= 4:
            write_text.append("    {objekt.DostatPenize} peníze")
        elif self.DostatPenize >= 5:
            write_text.append("    {objekt.DostatPenize} peněz")

        button = ButtonNaListe((0.2 / 100 * ObjektLista.VelikostPismen, (5.5 + len(write_text) * 2.4) / 100 * ObjektLista.VelikostPismen), 
                               (8/ 100 * ObjektLista.VelikostPismen, 5/ 100 * ObjektLista.VelikostPismen), "Vzit.png", Funkce.PokladDostat, 255, ObjektLista)
        write_text.append(button)

        Faze.NastavDefaultVeci(("PokladDostat", self), DefaultVlozitSeznam = [write_text])
        Faze.WriteDefault()

    def ZmenSeNaPrazdny(self):
        self.Jmeno = "Prázdný poklad"
        self.typ_obr = "trea_empty"

class repository_tile(tile):
    @map_obj.dekor_init
    @tile.dekor_init
    def __init__(self, PoziceNaMape, ObjektGrid, AktualizFunk):
        self.narocnost = 3
        self.typ_text = "Zdroj"

        self.typ = random.randint(1, 3) # 1 - hedvábí, 2 - otroci, 3 - sůl
        self.typ_obr = f"repo{self.typ}"
        if self.typ == 1:
            self.Koupit = self.KoupitHedvabi
            self.KoupitFunkce = Funkce.ZdrojJitKoupitHedvabi
            self.Surovina4Pad = "hedvábí"
            self.Surovina2Pad = "hedvábí"
            self.Nazev = "Farma s hedvábím"
        elif self.typ == 2:
            self.Koupit = self.KoupitOtroci
            self.KoupitFunkce = Funkce.ZdrojJitKoupitOtroci
            self.Surovina4Pad = "otroky"
            self.Surovina2Pad = "otroků"
            self.Nazev = "Podezřelé stavení"
        elif self.typ == 3:
            self.Koupit = self.KoupitSul
            self.KoupitFunkce = Funkce.ZdrojJitKoupitSul
            self.Surovina4Pad = "sůl"
            self.Surovina2Pad = "soli"
            self.Nazev = "Solný důl"

        self.KupniCena = random.randint(3, 4)

    def KoupitHedvabi(self, hrac, kolik):
        if hrac.ZmenPenize(-kolik * self.KupniCena):
            if hrac.ZmenHedvabi(kolik):
                return True
            else:
                hrac.ZmenPenize(kolik * self.KupniCena)
                return False
        else:
            return False

    def KoupitOtroci(self, hrac, kolik):
        if hrac.ZmenPenize(-kolik * self.KupniCena):
            if hrac.ZmenOtroci(kolik):
                return True
            else:
                hrac.ZmenPenize(kolik * self.KupniCena)
                return False
        else:
            return False

    def KoupitSul(self, hrac, kolik):
        if hrac.ZmenPenize(-kolik * self.KupniCena):
            if hrac.ZmenSul(kolik):
                return True
            else:
                hrac.ZmenPenize(kolik * self.KupniCena)
                return False
        else:
            return False

class city_tile(tile):
    @map_obj.dekor_init
    @tile.dekor_init
    def __init__(self, PoziceNaMape, ObjektGrid, AktualizFunk):
        self.narocnost = 0
        self.typ_obr = "city"

        self.MaxHedvabi = 10
        self.MaxOtroci = 10
        self.MaxSul = 10

        self.NastavHedvabi(random.randint(4, 7))
        self.NastavOtroci(random.randint(4, 7))
        self.NastavSul(random.randint(4, 7))
        self.AktualizovatCeny()

        self.typ_text = "Mesto"

    def KoupitHedvabi(self, hrac, kolik):
        if hrac.ZmenPenize(-kolik * self.KupniCenaHedvabi):
            if hrac.ZmenHedvabi(kolik):
                if self.ZmenHedvabi(- kolik + random.randint(0, min(kolik, 2))):
                    return True
                else:
                    hrac.ZmenPenize(kolik * self.KupniCenaHedvabi)
                    hrac.ZmenHedvabi(-kolik)
                    return False
            else:
                hrac.ZmenPenize(kolik * self.KupniCenaHedvabi)
                return False
        else:
            return False

    def ProdatHedvabi(self, hrac, kolik):
        if hrac.ZmenPenize(kolik * self.ProdejniCenaHedvabi):
            if hrac.ZmenHedvabi(-kolik):
                if self.ZmenHedvabi(kolik - random.randint(0, round(kolik/2))):
                    return True
                else:
                    hrac.ZmenPenize(-kolik * self.ProdejniCenaHedvabi)
                    hrac.ZmenHedvabi(kolik)
                    return False
            else:
                hrac.ZmenPenize(- kolik * self.KupniCenaHedvabi)
                return False
        else:
            return False

    def NastavHedvabi(self, nakolik):
        if 0 <= nakolik <= self.MaxHedvabi:
            self.PocetHedvabi = nakolik
            return True
        return False

    def ZmenHedvabi(self, okolik):
        return self.NastavHedvabi(self.PocetHedvabi + okolik)

    def KoupitOtroci(self, hrac, kolik):
        if hrac.ZmenPenize(-kolik * self.KupniCenaOtroci):
            if hrac.ZmenOtroci(kolik):
                if self.ZmenOtroci(- kolik + random.randint(0, round(kolik/2))):
                    return True
                else:
                    hrac.ZmenPenize(kolik * self.KupniCenaOtroci)
                    hrac.ZmenOtroci(-kolik)
                    return False
            else:
                hrac.ZmenPenize(kolik * self.KupniCenaOtroci)
                return False
        else:
            return False

    def ProdatOtroci(self, hrac, kolik):
        if hrac.ZmenPenize(kolik * self.ProdejniCenaOtroci):
            if hrac.ZmenOtroci(-kolik):
                if self.ZmenOtroci(kolik - random.randint(0, round(kolik/2))):
                    return True
                else:
                    hrac.ZmenPenize(-kolik * self.ProdejniCenaOtroci)
                    hrac.ZmenOtroci(kolik)
                    return False
            else:
                hrac.ZmenPenize(- kolik * self.KupniCenaOtroci)
                return False
        else:
            return False

    def NastavOtroci(self, nakolik):
        if 0 <= nakolik <= self.MaxOtroci:
            self.PocetOtroci = nakolik
            return True
        return False

    def ZmenOtroci(self, okolik):
        return self.NastavOtroci(self.PocetOtroci + okolik)

    def KoupitSul(self, hrac, kolik):
        if hrac.ZmenPenize(-kolik * self.KupniCenaSul):
            if hrac.ZmenSul(kolik):
                if self.ZmenSul(- kolik + random.randint(0, round(kolik/2))):
                    return True
                else:
                    hrac.ZmenPenize(kolik * self.KupniCenaSul)
                    hrac.ZmenSul(-kolik)
                    return False
            else:
                hrac.ZmenPenize(kolik * self.KupniCenaSul)
                return False
        else:
            return False

    def ProdatSul(self, hrac, kolik):
        if hrac.ZmenPenize(kolik * self.ProdejniCenaSul):
            if hrac.ZmenSul(-kolik):
                if self.ZmenSul(kolik - random.randint(0, round(kolik/2))):
                    return True
                else:
                    hrac.ZmenPenize(-kolik * self.ProdejniCenaSul)
                    hrac.ZmenSul(kolik)
                    return False
            else:
                hrac.ZmenPenize(- kolik * self.KupniCenaSul)
                return False
        else:
            return False

    def NastavSul(self, nakolik):
        if 0 <= nakolik <= self.MaxSul:
            self.PocetSul = nakolik
            return True
        return False

    def ZmenSul(self, okolik):
        return self.NastavSul(self.PocetSul + okolik)

    def AktualizovatCeny(self):
        self.KupniCenaHedvabi = self.MaxHedvabi - self.PocetHedvabi + 1
        self.ProdejniCenaHedvabi = self.MaxHedvabi - self.PocetHedvabi
            
        self.KupniCenaOtroci = self.MaxOtroci - self.PocetOtroci + 1
        self.ProdejniCenaOtroci = self.MaxOtroci - self.PocetOtroci
        
        self.KupniCenaSul = self.MaxSul - self.PocetSul + 1
        self.ProdejniCenaSul = self.MaxSul - self.PocetSul

    def ZamichatCeny(self):
        self.ZmenHedvabi(random.randint(-2, 2))
        self.ZmenOtroci(random.randint(-2, 2))
        self.ZmenSul(random.randint(-2, 2))
        self.AktualizovatCeny()