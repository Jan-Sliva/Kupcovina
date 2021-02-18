from Entita import *

class player(Entita):

    @map_obj.dekor_init
    @Entita.dekor_init
    def __init__(self, PoziceNaMape, ObjektGrid, AktualizFunk, PomerStran, obrazek_figurky, slozka, jmeno = "Bezejmenný"):
        """
        poměr stran je X/Y
        """
        self.typ_text = "Hrac"

        self.penize = 15
        self.hedvabi = 0 
        self.otroci = 0
        self.sul = 0

        self.MaxHedvabi = 10
        self.MaxOtroci = 10
        self.MaxSul = 10

        self.BodyPohybuDlouho = 3
        self.ResetBodyPohybu()

        self.jmeno = jmeno

        self.blacklist = set() # na jaká políčka tento hráč nemůže vstoupit
        self.PosledniMesto = None

    def Zvyraznit(self):
        self.AktPole.Zvyraznit()
        self.ZmenAlpha(self.Zvyraz)
        self.zvyrazneno = True

    def Odzvyraznit(self):
        self.AktPole.Odzvyraznit()
        self.ZmenAlpha(-self.Zvyraz)
        self.zvyrazneno = False

    def Pohyb(self):
        return self.Pohyb_rekurz(self.BodyPohybu, self.blacklist, self.AktPole.PoziceNaMape, 0, [], False)[:-1]

    def Pohyb_rekurz(self, okolik, blacklist, PoziceNaMape, plusnaroc, CestaSem, PridatSe = False):
        """
        Pokud není zadané PozicaNaMape, tak to přenastaví na pozici daného hráče
        Na PoziceNaMape musí existovat políčko
        """
        TotoPole = self.Grid.SeznamPolicek.Dostan(PoziceNaMape)
        
        if okolik >= 0:
            new_blacklist = blacklist.copy()
            new_blacklist.add(PoziceNaMape)
            new_blacklist.update([(PoziceNaMape[0] + vedle[0], PoziceNaMape[1] + vedle[1]) for vedle in map_obj.okoli])
        
            SeznamCest = []
            for vedle in map_obj.okoli:
                pozice = (PoziceNaMape[0] + vedle[0], PoziceNaMape[1] + vedle[1])
                policko = self.Grid.SeznamPolicek.Dostan(pozice)
                if policko != None and not pozice in blacklist:
                    delsi_cesta = CestaSem.copy()
                    delsi_cesta.append(vedle)
                    SeznamCest.extend(self.Pohyb_rekurz(okolik - policko.narocnost, new_blacklist, pozice, plusnaroc + policko.narocnost, delsi_cesta))
            
            DictCest = {}
            for index in range(len(SeznamCest)):
                pozice = SeznamCest[index][0].PoziceNaMape
                if DictCest.get(pozice) != None:
                    DictCest[pozice].append(index)
                else:
                    DictCest[pozice] = [index]

            KonecnySeznam = []
            for value in DictCest.values():
                if len(value) > 1:
                    nej_cesta = SeznamCest[value[0]]
                    for index in value[1:]:
                        cesta = SeznamCest[index]
                        if cesta[1] < nej_cesta[1] or (cesta[1] == nej_cesta[1] and len(cesta[2]) < len(nej_cesta[2])):
                            nej_cesta = cesta
                    KonecnySeznam.append(nej_cesta)
                else:
                    KonecnySeznam.append(SeznamCest[value[0]])
            KonecnySeznam.append((TotoPole, plusnaroc, CestaSem))
            return KonecnySeznam

        else:
            return []

    @map_obj.Update_dekor
    def NastavBodyPohybu(self, hodnota):
        self.BodyPohybu = hodnota

    def ZmenBodyPohybu(self, okolik):
        self.NastavBodyPohybu(self.BodyPohybu + okolik)

    def ResetBodyPohybu(self):
        self.NastavBodyPohybu(self.BodyPohybuDlouho)

    def NastavBodyPohybuDlouho(self, novebodypohybu):
        self.BodyPohybuDlouho = novebodypohybu

    def ZmenBodyPohybuDlouho(self, okolik):
        self.NastavBodyPohybu(self.BodyPohybuDlouho + okolik)

    def ZmenPenize(self, okolik):
        if 0 <= self.penize + okolik:
            self.penize += okolik
            return True
        return False

    def ZmenHedvabi(self, okolik):
        if 0 <= self.hedvabi + okolik <= self.MaxHedvabi:
            self.hedvabi += okolik
            return True
        return False

    def ZmenOtroci(self, okolik):
        if 0 <= self.otroci + okolik <= self.MaxOtroci:
            self.otroci += okolik
            return True
        return False

    def ZmenSul(self, okolik):
        if 0 <= self.sul + okolik <= self.MaxSul:
            self.sul += okolik
            return True
        return False

    def ZmenJmeno(self, novejmeno):
        self.jmeno = novejmeno

    def ZmenPosledniMesto(self, PosledniMesto):
        if self.PosledniMesto != None:
            self.blacklist.remove(self.PosledniMesto.PoziceNaMape)
        self.PosledniMesto = PosledniMesto
        self.blacklist.add(self.PosledniMesto.PoziceNaMape)
