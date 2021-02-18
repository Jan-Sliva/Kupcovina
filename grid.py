from okno import *
from Grid_list import *
from tile import *
from mob import *
from hrac import *
import ast


class grid(okno):
    
    
    @okno.Init_Pozadi
    def __init__(self, pozice, rozmery, slozka, RychlostPribliz, VyskaPole, alpha):
        self.pozice = pozice
        self.alpha = alpha
        self.NacistSlozku(slozka)
        self.NastavRozmery(rozmery)

        self.SeznamPolicek = Grid_list()
        self.SeznamHracu = []

        self.mod_obr = None

        self.RychlostPribliz = RychlostPribliz
        self.Nastav_VyskaPole(VyskaPole)
        self.centrum = self.get_center((0, 0))

        # pohyb s mapou pomoci myši
        self.lastly_pressed = False # jestli minule byla držena myš (levé tlačítko)
        self.last_mouse = [0, 0] # poslední pozice myši, x = [0], y = [1]
        self.started_move = False # jestli byl odstartován tah

    def NacistSlozku(self, slozka):
        self.slozka = slozka

        with open(os.path.join(self.slozka, "init" + okno.Pripona)) as file:
            init_text = file.read().splitlines() 

        obrazek = init_text[0]
        self.Obrazky = [] # Sem se ukládají obrázky
        x = self.ImportObr(obrazek)
        self.AktObr = self.Obrazky[x]

        self.ObrazkyPolicek = ast.literal_eval(init_text[1])
        slozka_policek = os.path.join(self.slozka, "Policka")

        for key in self.ObrazkyPolicek.keys():
            self.ObrazkyPolicek[key] = pygame.image.load(os.path.join(slozka_policek, self.ObrazkyPolicek[key])).convert()
            self.ObrazkyPolicek[key].set_colorkey((0, 0, 0))

        self.ObrazkyPolicek["pozadi"] = pygame.image.load(os.path.join(slozka_policek, init_text[2])).convert()
        self.ObrazkyPolicek["pozadi"].set_colorkey(ast.literal_eval(init_text[3]))
        
    def Nastav_VyskaPole(self, VyskaPole):
       """
       Nastaví mřížku na velikost, kde vstup je délka mezi dvěma řádky
       """
       ZaokrVyskaPole = math.ceil(VyskaPole)
       if ZaokrVyskaPole < 0:
           ZaokrVyskaPole = 0
       self.RozmeryPole = (ZaokrVyskaPole, math.ceil(ZaokrVyskaPole * math.sqrt(3) / 2)) # zaokrouhluji nahoru, aby nevznikly jednopixelové mezery
       self.VzdalenostiPoli = (ZaokrVyskaPole * 3 / 4, self.RozmeryPole[1] / 2) # [0] = vzdálenost sloupců, [1] = vzdálenost řádků
       self.VyskaPole = VyskaPole

       del self.mod_obr
       self.mod_obr = self.ObrazkyPolicek.copy() # modifikované obrázky

       for key in self.mod_obr.keys():
           self.mod_obr[key] = pygame.transform.scale(self.mod_obr[key], (self.RozmeryPole[0], self.RozmeryPole[1])) 

    def create_tile(self, pozice, AktualizovatFunk):
        """
        Když existuje tile se vstupní pozicí na mapě, vrátí None:
        Jinak vytvoří tile se vstupní pozicí na mapě, přidá tile do SeznamPolicek a vrátí tento tile
        """
        if self.SeznamPolicek.Dostan(pozice) == None:
            if not self.is_around_city(pozice):
                rand = random.randint(1, 20)
                if rand == 1:
                    pole = city_tile(pozice, self, AktualizovatFunk)
                elif rand == 2:
                    pole = repository_tile(pozice, self, AktualizovatFunk)
                elif rand == 3:
                    pole = treasure_tile(pozice, self, AktualizovatFunk)
                else:
                    pole = normal_tile(pozice, self, AktualizovatFunk)
            else:
                pole = normal_tile(pozice, self, AktualizovatFunk)
            return pole
        else:
            return None

    def is_around_city(self, pozice):
        """
        zkontroluje jestli je vedle město nebo zdroj
        """
        for i in map_obj.okoli:
            Policko = self.SeznamPolicek.Dostan((pozice[0] + i[0], pozice[1] + i[1]))
            if  Policko != None and (type(Policko) is city_tile or type(Policko) is repository_tile or type(Policko) is treasure_tile):
                return True
        return False


    def PoziceNaMrizce(self, pozice):
        """
        argument přijímá jako pozici v pygame okně
        vrací pozici v mřížce
        """
        PoziceOdCentra = [pozice[0] - self.pozice[0] - self.centrum[0] - self.RozmeryPole[0]/2,
                          pozice[1] - self.pozice[1] - self.centrum[1] - self.RozmeryPole[1]/2]
        Kvadrant = (round(PoziceOdCentra[0]/self.VzdalenostiPoli[0]), round(PoziceOdCentra[1]/self.VzdalenostiPoli[1])) # obdélníková čtvercová síť
        if (Kvadrant[0] + Kvadrant[1])%2 == 0: # Tento kvadrant je součástí jednoho políčka
            return Kvadrant
        else:
            # teď budu měřit vzdálenosti ke všem středům sousedních políček, ta nejvyšší vzdálenost patří středu hledaného políčka
            nejnizsi_vzdalenost = self.RozmeryPole[0]/2 + 1 # nejnižší vzdálenost plus jedna
            for vedle in ((-1, 0), (1, 0), (0, 1), (0, -1)): # pro všechna vedlejší políčka
                tato_vzdalenost = math.sqrt(((Kvadrant[0] + vedle[0]) * self.VzdalenostiPoli[0] - PoziceOdCentra[0])**2 + 
                                            ((Kvadrant[1] + vedle[1]) * self.VzdalenostiPoli[1] - PoziceOdCentra[1])**2)
                if tato_vzdalenost < nejnizsi_vzdalenost:
                    nejnizsi_vzdalenost = tato_vzdalenost
                    ret = (Kvadrant[0] + vedle[0], Kvadrant[1] + vedle[1])
            return ret

    def DostanPolickoDlePozice(self, pozice):
        """
        argument přijímá jako pozici v pygame okně
        vrací objekt políčka nebo None, když neexistuje
        """
        MrizkaPozice = self.PoziceNaMrizce(pozice)
        return self.SeznamPolicek.Dostan(MrizkaPozice)

    def DostanHraceDlePozice(self, pozice):
        """
        pozice v pygame okně --> objekt hráče, nebo None, když tam žádný není
        """
        for hrac in self.SeznamHracu:
            if hrac.MysJeNa(pozice):
                return hrac
        return None

    def DostanObjektDlePozice(self, pozice):
        vysledek = self.DostanHraceDlePozice(pozice)
        if vysledek == None:
            vysledek = self.DostanPolickoDlePozice(pozice)
        return vysledek

    def MysJeNaPolicku(self, mouse_pos):
        if self.DostanObjektDlePozice(mouse_pos) != None:
            return True
        return False
    
    def UpdateMapyPoziceRozmery(funkce): # dekorátor
        def inner(self, *args):
            funkce(self, *args)
            for hrac in self.SeznamHracu:
                hrac.UpdatePoziceRozmery()
            for policko in self.SeznamPolicek.Dostan_Seznam():
                policko.UpdatePozice()
        return inner

    def UpdateMapyPozice(funkce): # dekorátor
        def inner(self, *args):
            funkce(self, *args)
            for hrac in self.SeznamHracu:
                hrac.UpdatePozice()
            for policko in self.SeznamPolicek.Dostan_Seznam():
                policko.UpdatePozice()
        return inner

    @UpdateMapyPoziceRozmery
    def Pribliz(self, change, PoziceMysi):
        """
        vstup "change": True - zvětšení
                        False - zmenšení
        """
        PoziceMysi = (PoziceMysi[0] - self.pozice[0], PoziceMysi[1] - self.pozice[1]) # přenastavení na pozici v grid okně
        if change: # zvětšení
            zoom_change = self.RychlostPribliz
        else: # zmenšení
            zoom_change = self.RychlostPribliz**-1
        stare_rozmery = self.RozmeryPole
        self.Nastav_VyskaPole(self.VyskaPole * zoom_change)
        zoom_change_real = self.RozmeryPole[0] / stare_rozmery[0], self.RozmeryPole[1] / stare_rozmery[1] # reálné zvětšení
        self.centrum = [PoziceMysi[0] - (PoziceMysi[0]-self.centrum[0])*zoom_change_real[0], 
                       PoziceMysi[1] - (PoziceMysi[1]-self.centrum[1])*zoom_change_real[1]]
    
    @UpdateMapyPoziceRozmery
    def reset_zoom(self, velikost, pozice, NastavitMys):
        """
        přenastaví mapu na velikost první vstupní hodnoty
        zarovná mapu aby políčko na druhé vstupní pozici bylo ve středu
        myš nastaví doprostřed, jestli je třetí vstup True
        vrátí novou pozici myši
        """
        self.Nastav_VyskaPole(velikost)
        self.centrum = self.get_center(pozice)
        if NastavitMys:
            pygame.mouse.set_pos((self.rozmery[0]/2 + self.pozice[0], self.rozmery[1]/2 + self.pozice[1]))

    def get_center(self, pozice):
        """
        argumenty jsou souřadnice, vezme políčko (nebo prázdné pole) s těmito souřadnicemi
        vrátí, jaká by byla pozice políčka 0, 0, kdyby dané pole bylo veprostřed
        """
        # vypočítá to vzdálenost pole od středu, obrátí tuto hodnotu a přičte hodnotu středu plus polovinu políčka, aby toto políčko mělo střed ve středu
        return [-1 * pozice[0]*self.VzdalenostiPoli[0] + self.rozmery[0]/2 - self.RozmeryPole[0]/2, 
                -1 * pozice[1]*self.VzdalenostiPoli[1] + self.rozmery[1]/2 - self.RozmeryPole[1]/2] 

    def start_move(self):
        """
        začátek pohybu s mapou
        """
        self.started_move = True
    
    @UpdateMapyPozice
    def move(self, mouse_pos):
        """
        pohyb s mapou
        """
        if self.started_move:
            if self.lastly_pressed:
                self.centrum = [self.centrum[0] + (mouse_pos[0] - self.last_mouse[0]),
                                self.centrum[1] + (mouse_pos[1] - self.last_mouse[1])]
            self.last_mouse = mouse_pos
            self.lastly_pressed = True
            
    def end_move(self):
        """
        konec pohybu s mapou
        """
        self.lastly_pressed = False
        self.started_move = False

    @okno.dekor_ukazat
    def Ukazat(self, screen):
        self.pozadi.blit(self.obrazek, (0,0))

        pozadi = self.mod_obr["pozadi"]

        for obj in self.SeznamPolicek.Dostan_Seznam():
            obraz = self.mod_obr[obj.typ_obr]
            if obraz.get_alpha() != obj.alpha:
                obraz.set_alpha(obj.alpha)
            if pozadi.get_alpha() != obj.alpha:
                pozadi.set_alpha(obj.alpha)

            self.pozadi.blit(pozadi, obj.pozice)
            self.pozadi.blit(obraz, obj.pozice)

        for hrac in self.SeznamHracu:
            hrac.Ukazat()