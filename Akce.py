import random
from Funkce import *

class Akce():
    def __init__(self, pravdepodobnost, texttyp, funkce, pocet, nazev):
        self.Pocet = pocet
        self.Pravdepodobnost = pravdepodobnost
        self.TypText = texttyp
        self.funkce = funkce
        self.Nazev = nazev


class AkceSeznam():
    def init(lista):
        AkceSeznam.Lista = lista
        AkceSeznam.SeznamAkci = []
        AkceSeznam.CelkovaPravdepodobnost = 0

        Akce1 = Akce(1, "ZtratitPenize", Funkce.AkceDostatPenize, -7, "Byl jsi okraden")
        Akce2 = Akce(2, "ZtratitPenize", Funkce.AkceDostatPenize, -5, "Byl jsi okraden")
        Akce3 = Akce(3, "ZtratitPenize", Funkce.AkceDostatPenize, -3, "Byl jsi okraden")
        
        Akce4 = Akce(5, "DostatPenize", Funkce.AkceDostatPenize, 3, "Šťastný nález")
        Akce5 = Akce(4, "DostatPenize", Funkce.AkceDostatPenize, 5, "Šťastný nález")
        Akce6 = Akce(3, "DostatPenize", Funkce.AkceDostatPenize, 7, "Šťastný nález")
        Akce7 = Akce(2, "DostatPenize", Funkce.AkceDostatPenize, 9, "Šťastný nález")
        Akce8 = Akce(1, "DostatPenize", Funkce.AkceDostatPenize, 11, "Šťastný nález")
        Akce9 = Akce(1, "DostatPenize", Funkce.AkceDostatPenize, 13, "Šťastný nález")


        Akce10 = Akce(1, "ZtratitHedvabi", Funkce.AkceDostatHedvabi, -2, "Potrhané hedvábí")
        Akce11 = Akce(3, "ZtratitHedvabi", Funkce.AkceDostatHedvabi, -1, "Potrhané hedvábí")

        Akce12 = Akce(3, "DostatHedvabi", Funkce.AkceDostatHedvabi, 1, "Vzácný dar")
        Akce13 = Akce(2, "DostatHedvabi", Funkce.AkceDostatHedvabi, 2, "Vzácný dar")
        Akce14 = Akce(1, "DostatHedvabi", Funkce.AkceDostatHedvabi, 3, "Vzácný dar")


        Akce15 = Akce(1, "ZtratitOtroci", Funkce.AkceDostatOtroci, -2, "Útěk")
        Akce16 = Akce(3, "ZtratitOtroci", Funkce.AkceDostatOtroci, -1, "Útěk")

        Akce17 = Akce(3, "DostatOtroci", Funkce.AkceDostatOtroci, 1, "Dobrovolník")
        Akce18 = Akce(2, "DostatOtroci", Funkce.AkceDostatOtroci, 2, "Dobrovolníci")
        Akce19 = Akce(1, "DostatOtroci", Funkce.AkceDostatOtroci, 3, "Dobrovolníci")


        Akce20 = Akce(1, "ZtratitSul", Funkce.AkceDostatSul, -2, "Vysypaný pytel soli")
        Akce21 = Akce(3, "ZtratitSul", Funkce.AkceDostatSul, -1, "Vysypaný pytel soli")

        Akce22 = Akce(3, "DostatSul", Funkce.AkceDostatSul, 1, "Nehlídaná kopa soli")
        Akce23 = Akce(2, "DostatSul", Funkce.AkceDostatSul, 2, "Nehlídaná kopa soli")
        Akce24 = Akce(1, "DostatSul", Funkce.AkceDostatSul, 3, "Nehlídaná kopa soli")


        Akce25 = Akce(2, "ZtratitBodyPohybu", Funkce.AkceDostatBodyPohybu, -1, "Rozbité kolo")

        Akce26 = Akce(3, "DostatBodyPohybu", Funkce.AkceDostatBodyPohybu, 1, "Zkratka")
        Akce27 = Akce(2, "DostatBodyPohybu", Funkce.AkceDostatBodyPohybu, 2, "Zkratka")

        
        Akce28 = Akce(10, "AkceNicSeNedeje", Funkce.Nic, 0, "Klidný den")

        AkceSeznam.PridejViceAkci(Akce1, Akce2, Akce3, Akce4, Akce5, Akce6, Akce7, Akce8, Akce9, Akce10, Akce11, Akce12, Akce13, Akce14,
                                 Akce15, Akce16, Akce17, Akce18, Akce19, Akce20, Akce21, Akce22, Akce23, Akce24, Akce25, Akce26, Akce27, Akce28)

    def PridejAkci(akce):
        AkceSeznam.SeznamAkci.append(akce)
        AkceSeznam.CelkovaPravdepodobnost += akce.Pravdepodobnost

    def PridejViceAkci(*ViceAkci):
        for akce in ViceAkci:
            AkceSeznam.PridejAkci(akce)

    def ProvedNahodnouAkci():
        loop_quit = False
        while not loop_quit:
            randint = random.randint(1, AkceSeznam.CelkovaPravdepodobnost)
            cislo = 0
            for akce in AkceSeznam.SeznamAkci:
                cislo += akce.Pravdepodobnost
                if randint <= cislo:
                    AkceSeznam.AktAkce = akce
                    break
            loop_quit = AkceSeznam.AktAkce.funkce()
        AkceSeznam.Lista.writeTyp(AkceSeznam.AktAkce.TypText, AkceSeznam.AktAkce, False)
        return akce




