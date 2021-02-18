from okno import *
from Posuvnik import *
from Funkce import *
import ast, glob

class lista(okno):
    
    

    @okno.Init_Pozadi
    def __init__(self, pozice, rozmery, slozka, VelikostPismen, alpha):
        """
        VelikostPismen: ostatní velikosti písmen uložené v souborech a jsou uváděny v % této výšky 
        """
        self.pozice = pozice
        self.SeznamAktivovanychButton = []
        self.SeznamAktivovanychPosuvnik = []
        self.posunuti = 0 # posunutí lišty (pomocí kolečka na myši)
        self.alpha = alpha

        self.VlozitSeznam = []

        self.SeznamFunkce = []
        self.Seznam = []

        # rychlý posun lišty
        self.posun_pozice = 0
        self.started_RychlyPosun = False
        kurzor = pygame.cursors.compile(pygame.cursors.sizer_y_strings)
        self.Rychly_Posun_kurzor = [(16, 24), (0, 0), kurzor[0], kurzor[1]]

        self.NacistSlozku(slozka, VelikostPismen)
        self.Akt_objekt = None
        self.Akt_text = []
        self.Akt_typ = None
        self.posledni_radek = 0
        self.NastavRozmery(rozmery)
        
    def NacistSlozku(self, slozka, VelikostPismen):
        self.slozka = slozka
        self.VelikostPismen = VelikostPismen

        with open(os.path.join(slozka, "init" + okno.Pripona), "r", encoding = "utf_8_sig") as file:
            nacteny_text_init = file.read().splitlines()

        odsazeni = ast.literal_eval(nacteny_text_init[0])
        self.odsazeni = (odsazeni[0] / 100 * VelikostPismen, odsazeni[1] / 100 * VelikostPismen, odsazeni[2] / 100 * VelikostPismen) # odsazení od okraje lišty zleva zeshora zprava

        pozadi = ast.literal_eval(nacteny_text_init[1])
        self.Obrazky = [] # Sem se ukládají obrázky
        x = self.ImportObr(os.path.join("Obrazky", pozadi))
        self.AktObr = self.Obrazky[x]

        self.obrazek_pomerXY = ast.literal_eval(nacteny_text_init[2])

        # nahráváni textů ze složky
        self.texty = {}
        for nazev in glob.iglob(os.path.join(self.slozka, "Texty", "*" + okno.Pripona)):
            with open(nazev, "r", encoding = "utf_8") as file:
                nacteny_text = file.read().splitlines()
            nazev = nazev[len(os.path.join(self.slozka, "Texty", "")): -1 *len(okno.Pripona)] # vymazání adresáře do složky a přípony
            
            text_seznam = []
            
            def NebylNalezenDict():
                nonlocal text_seznam
                print(nazev + okno.Pripona + ": Na prvním řádku nebyly nalezeny informace o formátování textu za ním, bude to nahrazeno defaultní hodnotou")
                # velikost a mezera meziradky jsou v procentech oproti výšce lišty
                text_seznam = [{"font" : "arial", "velikost" : 2, "pozice" : (0, 0), "bold" : False, "italic" : False, "underline" : False, "meziradky" : 0.4, "barva": (0, 0, 0), "zarovnani" : (0, 0)}]

            
            try:
                if nacteny_text[0][0] == "{":
                    mod_text = ast.literal_eval(nacteny_text[0])
                    text_seznam.append(mod_text) # první musí být dict určující parametry textu za ním
                    nacteny_text = nacteny_text[1:]
                else:
                    NebylNalezenDict()
            except:
                NebylNalezenDict()
            
            for line in nacteny_text:
                if len(line) >= 2:
                    if line[0:2] == "/{" or line[0:2] == "//" or line[0:2] == "/[": # abych mohl napsat "{" a "/" normálně
                        line = line[1:]
                    elif line[0] == "{" or line[0] == "[": # dict určjící parametry textu za ním nebo list definující tlačítko nebo posuvník
                        try:
                            line = ast.literal_eval(line)
                        except:
                            pass
                    elif line[0:7] == "/vlozit":
                        try:
                            line = ast.literal_eval(line[7:])
                        except:
                            pass
                text_seznam.append(line)
            
            posledni_radek = 0
            Parametry = {}
            for line in text_seznam:
                if type(line) is dict:
                    if line.get("pozice") != None:
                        if line["pozice"][0] == "same": # stejné odsazení
                            line["pozice"] = (Parametry["pozice"][0], line["pozice"][1])
                        else:
                            line["pozice"] = (line["pozice"][0] / 100 * VelikostPismen, line["pozice"][1])

                        if line["pozice"][1] == "same": # stejný řádek
                            line["pozice"] = (line["pozice"][0], zacatek_radku - self.odsazeni[1])
                        elif line["pozice"][1] == "next": # další řádek
                            line["pozice"] = (line["pozice"][0], zacatek_radku - self.odsazeni[1] + Parametry["meziradky"] + MinulaVelikost)
                        else:
                            line["pozice"] = (line["pozice"][0], line["pozice"][1] / 100 * VelikostPismen)

                    if line.get("velikost") != None:
                        if line["velikost"] == "same":
                            line["velikost"] = Parametry["velikost"]
                        else:
                            line["velikost"] = round(line["velikost"] / 100 * VelikostPismen)

                    if line.get("meziradky") != None:
                        if line["meziradky"] == "same":
                            line["meziradky"] = Parametry["meziradky"]
                        else:
                            line["meziradky"] = line["meziradky"] / 100 * VelikostPismen

                    if line.get("pozice") != None:
                        if line.get("meziradky") == None:
                            Meziradky = Parametry["meziradky"]
                        else:
                            Meziradky = line["meziradky"]
                        if line.get("velikost") == None:
                            Velikost = Parametry["velikost"]
                        else:
                            Velikost = line["velikost"]
                        zacatek_radku = self.odsazeni[1] + line["pozice"][1] - (Meziradky + Velikost)

                    if line.get("font") != None:
                        if line.get("velikost") == None:
                            Velikost = Parametry["velikost"]
                        else:
                            Velikost = line["velikost"]
                        JmenoFontu = line["font"]
                        line["font"] = lista.DostanFontBezFormatu(line["font"], Velikost)
                    elif line.get("velikost") != None and line.get("velikost") != Parametry["velikost"]:
                        line["font"] = lista.DostanFontBezFormatu(JmenoFontu, line["velikost"])
                    
                    Parametry = Parametry.copy()
                    Parametry.update(line)
                    MinulaVelikost = Parametry["velikost"]
                elif type(line) is list:
                    
                    if line[0][0] == "same": # stejné odsazení
                        line[0] = (Parametry["pozice"][0], line[0][1])
                    elif not line[0][0] == "next":
                        line[0] = (line[0][0] / 100 * VelikostPismen, line[0][1])

                    if line[0][1] == "same": # stejný řádek
                        line[0] = (line[0][0], zacatek_radku - self.odsazeni[1])
                        dalsi_radek = False
                    elif line[0][1] == "next": # další řádek
                        line[0] = (line[0][0], zacatek_radku - self.odsazeni[1] + Parametry["meziradky"] + MinulaVelikost)
                        dalsi_radek = True
                    else:
                        line[0] = (line[0][0], line[0][1] / 100 * VelikostPismen)
                        dalsi_radek = False

                    line[1] = (line[1][0] / 100 * VelikostPismen, line[1][1])

                    if line[1][1] == "same":
                        line[1] = (line[1][0], Parametry["velikost"])
                    elif line[1][1] == "same+":
                        line[1] = (line[1][0], Parametry["velikost"] + Parametry["meziradky"])
                    else:
                        line[1] = (line[1][0], line[1][1] / 100 * VelikostPismen)

                    if dalsi_radek:
                        zacatek_radku += Parametry["meziradky"] + MinulaVelikost
                        if zacatek_radku > posledni_radek:
                            posledni_radek = zacatek_radku
                    else:
                        if line[0][1] + self.odsazeni[1] > posledni_radek:
                            posledni_radek = line[0][1] + self.odsazeni[1]

                    if len(line) == 5:
                        line[3] = eval(line[3])
                        text_seznam[text_seznam.index(line)] = ButtonNaListe(*line, self)
                    elif len(line) == 7:
                        line[4] = line[4] / 100 * VelikostPismen
                        text_seznam[text_seznam.index(line)] = Posuvnik(*line, self)

                    MinulaVelikost = line[1][1]
                elif type(line) is str:
                    zacatek_radku += Parametry["meziradky"] + Parametry["velikost"]
                    if zacatek_radku > posledni_radek:
                        posledni_radek = zacatek_radku
                    MinulaVelikost = Parametry["velikost"]

            self.texty[nazev] = [text_seznam, posledni_radek]

    @okno.dekor_ukazat
    def Ukazat(self, screen):

        for i in range(math.ceil(self.rozmery[1] / self.obrazek_rozmery[1]) + 1):
            self.pozadi.blit(self.obrazek, (0, self.posunuti + ((math.floor(self.posunuti / self.obrazek_rozmery[1]) + i) * self.obrazek_rozmery[1])))
        
        for line in self.Akt_text:
            typ = type(line)
            if typ is dict:
                Parametry = line
                Font = Parametry["font"]
                lista.NastavFormatovani(Font, Parametry["bold"], Parametry["italic"], Parametry["underline"])
                zacatek_radku = [self.odsazeni[0] + Parametry["pozice"][0],
                                 self.odsazeni[1] + Parametry["pozice"][1] + self.posunuti]
            elif typ is ButtonNaListe or typ is Posuvnik:
                line.Ukazat()
                if line.dalsi_radek:
                    zacatek_radku[1] += Parametry["meziradky"] + line.rozmery[1]
            elif typ is str:
                delka = Font.size(line)[0]
                zacatek = zacatek_radku[0] - Parametry["zarovnani"][0] * delka + Parametry["zarovnani"][1] * (self.konec_radku - zacatek_radku[0])
                self.pozadi.blit(Font.render(line, True, Parametry["barva"]), (zacatek, zacatek_radku[1]))
                zacatek_radku[1] += Parametry["meziradky"] + Parametry["velikost"]

    def writeTyp(self, typ, objekt = None, zvyraznit = True, SeznamFunkce = [], VlozitSeznam = []):
        """
        Jestli je některý z argumentů jiný, než daná věc napsaná na liště, tak to napíše něco na lištu:
        typ - šablona, podle které to napíše (uložená ve složce "Texty" od této lišty bez .txt)
        objekt - objekt, kterým má být tato šablona interpolována
        zvyraznit - jestli spustit od tohoto objektu metodu .Zvyraznit() a potom, jak se tato metoda zavolá znovu s jinými argumenty tak metodu .Odvyraznit()
        SeznamFunkce - při každém update lišty se každý prvek([0] - funkce, [1] - args) tohoto seznamu provede: prvek[0](*prvek[1]), výsledek uloží do self.Seznam,
                        Na liště lze self.Seznam zobrazit jako "seznam"
        """
        if objekt != self.Akt_objekt or typ != self.Akt_typ:
            if self.Akt_objekt != None and self.zvyraznit and self.Akt_objekt.zvyrazneno:
                self.Akt_objekt.Odzvyraznit()
            self.zvyraznit = zvyraznit
            
            self.posunuti = 0
            self.Akt_objekt = objekt
            self.Akt_typ = typ
            self.posledni_radek = self.texty[typ][1]

            self.SeznamAktivovanychButton = [] # Seznam Aktivovaných buttonů na liště
            self.SeznamAktivovanychPosuvnik = []

            del self.Akt_text
            self.Akt_text = self.texty[typ][0].copy()

            for line in self.Akt_text:
                typ = type(line)
                if typ is ButtonNaListe or typ is Posuvnik:
                    line.Aktivovat()

            self.PredeslePosuvnikyTlacitka = []

        elif self.zvyraznit != zvyraznit:
            self.zvyraznit = zvyraznit
            if not self.Akt_objekt.zvyrazneno and zvyraznit:
                self.Akt_objekt.Zvyraznit()
            elif self.Akt_objekt.zvyrazneno and not zvyraznit:
                self.Akt_objekt.Odzvyraznit()

        self.NastavSeznamFunkce(SeznamFunkce)
        self.NastavVlozitSeznam(VlozitSeznam)
        self.Aktualizovat()

    def writeObj(self, objekt, zvyraznit = True):
        self.writeTyp(objekt.typ_text, objekt, zvyraznit)

    def NastavSeznamFunkce(self, novyseznam):
        self.SeznamFunkce = novyseznam

    def NastavVlozitSeznam(self, seznam):
        self.VlozitSeznam = seznam
       
    def Update_text_typ(self, typ, objekt = None, Aktualizovat = False):
        """
        jestli je objekt na vstupu napsaný na liště, aktualizuje se lišta
        jestli se Aktualizovat == True, tak to taky aktualizuje
        """
        if (self.Akt_objekt == objekt and objekt != None) or Aktualizovat:
            
            if self.Akt_text != self.texty[typ][0].copy():
                del self.Akt_text
                self.Akt_text = self.texty[typ][0].copy()

            index = 0
            while index < len(self.Akt_text):
                if type(self.Akt_text[index]) is int:
                    if len(self.VlozitSeznam) > self.Akt_text[index]:
                        Mezitext = self.Akt_text[:index]
                        Mezitext.extend(self.VlozitSeznam[self.Akt_text[index]])
                        if len(self.Akt_text) > index + 1:
                            Mezitext.extend(self.Akt_text[index+1:])
                        # teď provedu aktivaci buttonů ve vloženém textu
                        MeziSeznam = []
                        for line in self.VlozitSeznam[self.Akt_text[index]]:
                            typ = type(line)
                            if typ is ButtonNaListe or typ is Posuvnik and not line in self.PredeslePosuvnikyTlacitka: # změna tlačítka, přidám to do dalšího seznamu
                                line.Aktivovat()
                                MeziSeznam.append(line)
                            elif typ is ButtonNaListe or typ is Posuvnik and line in self.PredeslePosuvnikyTlacitka: # tlačítko, které bylo již predešle, smažu ho z toho seznamu, přidám to do dalšího seznamu
                                self.PredeslePosuvnikyTlacitka.remove(line)
                        for tlacitko in self.PredeslePosuvnikyTlacitka: # smažu tlačítka, která zůstala v seznamu
                            typ = type(tlacitko)
                            if typ is ButtonNaListe:
                                self.SeznamAktivovanychButton.remove(tlacitko)
                            elif typ is Posuvnik:
                                self.SeznamAktivovanychPosuvnik.remove(tlacitko)
                        self.PredeslePosuvnikyTlacitka = MeziSeznam
                        self.Akt_text = Mezitext
                    else:
                        self.Akt_text.pop(index)
                index += 1

            self.udaj = []
            for posuvnik in self.SeznamAktivovanychPosuvnik:
                self.udaj.append(posuvnik.udaj)

            self.Seznam = []
            for prvek in self.SeznamFunkce:
                if len(prvek) == 2:
                    self.Seznam.append(prvek[0](*prvek[1]))
                else:
                    self.Seznam.append(prvek[0]())

            if objekt != None and self.zvyraznit and not objekt.zvyrazneno:
                self.Akt_objekt.Zvyraznit()

            Predesly_dict = {}
            for index in range(len(self.Akt_text)):
               typ = type(self.Akt_text[index])
               if typ is str:
                   try:
                       self.Akt_text[index] = self.Akt_text[index].format(objekt = self.Akt_objekt, udaj = self.udaj, seznam = self.Seznam) # interpolace
                   except:
                       pass
               elif typ is dict:
                   TentoDictKeys = self.Akt_text[index].keys()
                   for key in Predesly_dict.keys():
                       if not key in TentoDictKeys:
                           self.Akt_text[index][key] = Predesly_dict[key]
                   Predesly_dict = self.Akt_text[index]

               if (typ is dict and self.Akt_text[index]["pozice"][0] == "next") or ((typ is ButtonNaListe or typ is Posuvnik) and self.Akt_text[index].NextOnLine):
                   PredeslyRadek = self.Akt_text[index - 1]
                   TypPredesliRadek = type(PredeslyRadek)
                   if TypPredesliRadek is str:
                       line = None
                       index_line = index
                       while not type(line) is dict:
                           index_line -= 1
                           line = self.Akt_text[index_line]
                       lista.NastavFormatovani(line["font"], line["bold"], line["italic"], line["underline"])

                       delka = line["font"].size(PredeslyRadek)[0]
                       if typ is dict:
                           self.Akt_text[index]["pozice"] = ( (line["pozice"][0] + delka) - line["pozice"][0] - line["zarovnani"][0] * delka + line["zarovnani"][1] * 
                                                             (self.konec_radku - line["pozice"][0]),  self.Akt_text[index]["pozice"][1])
                       elif typ is ButtonNaListe or typ is Posuvnik:
                           self.Akt_text[index].PoziceNaListe = ( (line["pozice"][0] + delka) - line["zarovnani"][0] * delka + line["zarovnani"][1] * 
                                                                 (self.konec_radku - line["pozice"][0]), self.Akt_text[index].PoziceNaListe[1])
                           self.Akt_text[index].UpdatePozice()
                   elif  TypPredesliRadek is ButtonNaListe or TypPredesliRadek is Posuvnik:
                       if typ is dict:
                           self.Akt_text[index]["pozice"] = (PredeslyRadek.PoziceNaListe[0] + PredeslyRadek.rozmery[0], self.Akt_text[index]["pozice"][1])
                       elif typ is ButtonNaListe or typ is Posuvnik:
                           self.Akt_text[index].PoziceNaListe = (PredeslyRadek.PoziceNaListe[0] + PredeslyRadek.rozmery[0], self.Akt_text[index].PoziceNaListe[1])
                           self.Akt_text[index].UpdatePozice()
                   elif TypPredesliRadek is dict:
                       if typ is dict:
                           self.Akt_text[index]["pozice"] = (PredeslyRadek["pozice"][0], self.Akt_text[index]["pozice"][1])
                       elif typ is ButtonNaListe or typ is Posuvnik:
                           self.Akt_text[index].PoziceNaListe = (PredeslyRadek["pozice"][0], self.Akt_text[index].PoziceNaListe[1])
                           self.Akt_text[index].UpdatePozice()

    def Update_text_obj(self, objekt):
        """
        jestli je objekt na vstupu napsaný na liště, aktualizuje se lišta
        """
        self.Update_text_typ(self.Akt_typ, objekt)

    def Aktualizovat(self):
        """
        Aktualizuje text na liště
        """
        self.Update_text_typ(self.Akt_typ, self.Akt_objekt, True)

    Fonty = {}

    def DostanFontBezFormatu(font, velikost):
        list_fontu = lista.Fonty.get(font)
        if list_fontu == None:
            lista.Fonty[font] = {}
            list_fontu = lista.Fonty[font]

        Font = list_fontu.get(velikost)
        
        if Font == None:
            list_fontu[velikost] = pygame.font.SysFont(font, velikost)
            Font = list_fontu[velikost]
            return Font
        return Font

    def DostanFont(font, velikost, bold, italic, underline):
        Font = lista.DostanFontBezFormatu(font, velikost)
        lista.NastavFormatovani(Font, bold, italic, underline)
        return Font

    def UpdateTlacitek(funkce):
        def inner(self, *args):
            funkce(self, *args)
            for tlacitko in self.SeznamAktivovanychButton:
                tlacitko.UpdatePozice()
            for posuvnik in self.SeznamAktivovanychPosuvnik:
                posuvnik.UpdatePozice()
        return inner

    @UpdateTlacitek
    def Posunout(self, okolik):
        """
        okolik je v procentech výšky 
        """
        self.posunuti += okolik / 100 * self.rozmery[1]
        if self.posunuti > 0:
            self.posunuti = 0
        elif -1 * self.posunuti > self.posledni_radek:
            self.posunuti = -1 * self.posledni_radek


    def RychlyPosun_start(self, pozice_y):
        pygame.mouse.set_cursor(self.Rychly_Posun_kurzor[0], self.Rychly_Posun_kurzor[1], self.Rychly_Posun_kurzor[2], self.Rychly_Posun_kurzor[3])
        self.posun_pozice = pozice_y
        self.started_RychlyPosun = True

    @UpdateTlacitek
    def RychlyPosun_move(self, pozice_y):
        if self.started_RychlyPosun:
            self.posunuti += (self.posun_pozice - pozice_y) / 2
            if self.posunuti > 0:
                self.posunuti = 0
            elif -1 * self.posunuti > self.posledni_radek:
                self.posunuti = -1 *self.posledni_radek

    def RychlyPosun_end(self):
        pygame.mouse.set_cursor(*pygame.cursors.arrow)
        self.started_RychlyPosun = False

    def NastavFormatovani(Font, bold, italic, underline):
        if bold != Font.get_bold():
                Font.set_bold(bold)

        if italic != Font.get_italic():
                Font.set_italic(italic)

        if underline != Font.get_underline():
                Font.set_underline(underline)

    def NastavRozmery(self, noverozmery):
        """
        Nastaví rozměry na vstup a transformuje aktuální obrázek
        """
        self.rozmery = noverozmery
        
        if self.rozmery[0] <= 0: # je tam rovná se, aby self.obrazek_rozmery([0] i [1]) se nerovnalo nule
            self.rozmery = (0, self.rozmery[1])

        if self.rozmery[1] < 0:
            self.rozmery = (self.rozmery[0], 0)

        self.konec_radku = self.rozmery[0] - self.odsazeni[2]
        self.obrazek_rozmery = (self.rozmery[0], self.rozmery[0] / self.obrazek_pomerXY)
        self.NastavObr(self.AktObr, self.obrazek_rozmery, self.alpha)
        self.ZmenPozadi(self.rozmery)

    def ZarovnatTlacitkaNaStred(self):
        ListVeciNaListe = self.SeznamAktivovanychButton.copy()
        ListVeciNaListe.extend(self.SeznamAktivovanychPosuvnik)
        for Tlacitko in ListVeciNaListe:
            if not (type(Tlacitko) is ButtonNaListe and Tlacitko.funkce == Tlacitko.nic):
                Tlacitko.PoziceNaListe = ((self.rozmery[0] - self.odsazeni[0] - self.odsazeni[2] - Tlacitko.rozmery[0]) / 2, Tlacitko.PoziceNaListe[1])
                Tlacitko.UpdatePozice()


