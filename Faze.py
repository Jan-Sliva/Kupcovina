class Faze():

    def init(SeznamHracu, IndexPrvniHrac, Mrizka, TridaLista, ListaInfo, ListaPrehledFazi, ListaPrehledHracu,
            TlacitkoPokracovat, normal_tile, city_tile, repository_tile, treasure_tile, ButtonNaListe, AkceObjekt, KonecHryPenez, KonecMenu, UkoncitMainLoop):
        Faze.TridaLista = TridaLista

        Faze.KonecHryPenez = KonecHryPenez
        Faze.KonecMenu = KonecMenu
        Faze.UkoncitMainLoop = UkoncitMainLoop
        
        Faze.Info = ListaInfo
        Faze.PrehledFazi = ListaPrehledFazi
        Faze.PrehledHracu = ListaPrehledHracu

        Faze.ObjektAkce = AkceObjekt
        Faze.ObjektAkce.init(Faze.Info)

        Faze.ButtonNaListe = ButtonNaListe

        Faze.Mrizka = Mrizka

        Faze.TlacitkoPokracovat = TlacitkoPokracovat
        Faze.ZakazanoTlacitkoPokracovat = False

        Faze.Zvyrazneno = False

        Faze.SeznamHracu = SeznamHracu
        Faze.IndexHracNaTahu = IndexPrvniHrac
        Faze.PocetHracu = len(Faze.SeznamHracu)

        Faze.IndexZamichatCen = 0
        Faze.ZamichatCenyPriste = False

        Faze.ZvyrazOstPoli = -64
        Faze.ZvyrazHrace = 256 # zvýraznění hráče ne tahu

        Faze.normal_tile = normal_tile
        Faze.city_tile = city_tile
        Faze.repository_tile = repository_tile
        Faze.treasure_tile = treasure_tile

        Faze.NastavHrac(IndexPrvniHrac)
        Faze.faze = 0 # zatím žádná fáze
        Faze.NastavFaze(1)

        Faze.DefaultSeznamFunkci = []

        Faze.Mrizka.reset_zoom(200, Faze.HracNaTahu.AktPole.PoziceNaMape, False)

    def NastavFaze(faze):
        if Faze.faze == 2 and faze != 2:
            Faze.OdzvyraznitDlouho()

        Faze.faze = faze

        if Faze.Zvyrazneno:
            Faze.Odzvyraznit()

        if faze == 1: # Akce
            Faze.TlacitkoPokracovat.ZmenObrazekDleIndexu(Faze.ZakazanoTlacitkoPokracovat)
            akce = Faze.ObjektAkce.ProvedNahodnouAkci()
            Faze.UpdateListaPrehledHracu()
            Faze.NastavDefaultVeci((akce.TypText, akce))
        elif faze == 2: # Pohyb
            Faze.TlacitkoPokracovat.ZmenObrazekDleIndexu(2 + Faze.ZakazanoTlacitkoPokracovat)
            Faze.Pohyb = Faze.HracNaTahu.Pohyb()
            Faze.DostupnaPole = []
            for cesta in Faze.Pohyb:
                Faze.DostupnaPole.append(cesta[0])

            if Faze.HracNaTahu.AktPole.PoziceNaMape in Faze.HracNaTahu.blacklist and Faze.DostupnaPole != []:
                Faze.ZakazatTlacitkoPokracovat()

            Faze.ZvyraznitDlouho()
            Faze.NastavDefaultVeci((Faze.HracNaTahu.typ_text, Faze.HracNaTahu))
            Faze.WriteDefault()
        elif faze == 3: # Obchod
            Faze.TlacitkoPokracovat.ZmenObrazekDleIndexu(4 + Faze.ZakazanoTlacitkoPokracovat)
            typ_pole = type(Faze.HracNaTahu.AktPole)
            if typ_pole == Faze.city_tile:
                Faze.NastavDefaultVeci(("ObchodCityTile", Faze.HracNaTahu.AktPole))
                Faze.WriteDefault()
                Faze.HracNaTahu.ZmenPosledniMesto(Faze.HracNaTahu.AktPole)
            elif typ_pole is Faze.repository_tile:
                Faze.HracNaTahu.AktPole.KoupitFunkce()
            elif typ_pole is Faze.treasure_tile:
                Faze.HracNaTahu.AktPole.DostatPoklad(Faze.HracNaTahu, Faze.Info)
            else:
                Faze.NastavDefaultVeci((Faze.HracNaTahu.AktPole.typ_text, Faze.HracNaTahu.AktPole))
                Faze.WriteDefault()

        Faze.PrehledFazi.writeTyp("PrehledFazi", (Faze.HracNaTahu, Faze.faze), False)

    def ZakazatTlacitkoPokracovat():
        Faze.ZakazanoTlacitkoPokracovat = True
        Faze.TlacitkoPokracovat.ZmenObrazekDleIndexu(Faze.TlacitkoPokracovat.IndexObrazku + 1)
        Faze.TlacitkoPokracovat.NastavFunkci(None)

    def PovolitTlacitkoPokracovat():
        Faze.ZakazanoTlacitkoPokracovat = False
        Faze.TlacitkoPokracovat.ZmenObrazekDleIndexu(Faze.TlacitkoPokracovat.IndexObrazku - 1)
        Faze.TlacitkoPokracovat.ResetFunkce()

    def NastavHrac(IndexHracNatahu):
        """
        Nastaví aktuálního hráče podle indexu v SeznamHracu
        neobnovuje lišty
        """
        Faze.HracNaTahu = Faze.SeznamHracu[IndexHracNatahu]
        Faze.IndexHracNaTahu = IndexHracNatahu

    def Pokracovat():
        if Faze.faze == 2:
            Faze.HracNaTahu.ResetBodyPohybu()
        elif Faze.HracNaTahu.penize >= Faze.KonecHryPenez:
            poradi = sorted(Faze.SeznamHracu, key=lambda x: x.penize, reverse = True)
            Faze.KonecMenu(poradi)
            Faze.UkoncitMainLoop()

        if Faze.faze < 3:
            Faze.NastavFaze(Faze.faze + 1)
        else: # Faze.faze = 3
            if type(Faze.HracNaTahu.AktPole) is Faze.city_tile:
                Faze.HracNaTahu.AktPole.AktualizovatCeny()
            Faze.NastavHrac((Faze.IndexHracNaTahu + 1) % Faze.PocetHracu)
            Faze.UpdateListaPrehledHracu()
            if Faze.IndexHracNaTahu == Faze.IndexZamichatCen and Faze.ZamichatCenyPriste:
                for pole in Faze.Mrizka.SeznamPolicek.Dostan_Seznam():
                    if type(pole) is Faze.city_tile:
                        pole.ZamichatCeny()
                Faze.IndexZamichatCen = (Faze.IndexZamichatCen + 1) % Faze.PocetHracu
                Faze.ZamichatCenyPriste = False
            elif Faze.IndexHracNaTahu == Faze.IndexZamichatCen and not Faze.ZamichatCenyPriste:
                Faze.ZamichatCenyPriste = True
            Faze.NastavFaze(1)
            Faze.Mrizka.reset_zoom(200, Faze.HracNaTahu.AktPole.PoziceNaMape, False)

    def Zvyraznit():
        if Faze.faze == 2:
            Faze.Zvyrazneno = True
            for pole in Faze.DostupnaPole:
                pole.ZmenAlpha(-Faze.HracNaTahu.AktPole.ZvyrazOstatPoli)

    def Odzvyraznit():
        if Faze.faze == 2:
            Faze.Zvyrazneno = False
            for pole in Faze.DostupnaPole:
                pole.ZmenAlpha(Faze.HracNaTahu.AktPole.ZvyrazOstatPoli)

    def ZvyraznitDlouho():
        for pole in Faze.Mrizka.SeznamPolicek.Dostan_Seznam():
            if not pole in Faze.DostupnaPole:
                pole.ZmenAlpha(Faze.ZvyrazOstPoli)
        Faze.HracNaTahu.AktPole.ZmenAlpha(-Faze.ZvyrazOstPoli)
        Faze.HracNaTahu.ZmenAlpha(Faze.ZvyrazHrace)

    def OdzvyraznitDlouho():
        for pole in Faze.Mrizka.SeznamPolicek.Dostan_Seznam():
            if not pole in Faze.DostupnaPole:
                pole.ZmenAlpha(-Faze.ZvyrazOstPoli)
        Faze.HracNaTahu.AktPole.ZmenAlpha(Faze.ZvyrazOstPoli)
        Faze.HracNaTahu.ZmenAlpha(-Faze.ZvyrazHrace)

    def ZmenPoziciHracNaTahu(ObjektTile):
        Faze.OdzvyraznitDlouho()
        Faze.WriteDefault()
        Faze.HracNaTahu.NastavPoziciNaMape(ObjektTile.PoziceNaMape)
        Faze.HracNaTahu.AktPole.OdkryjVedlejsi(Faze.HracNaTahu.Aktualizovat)

        for cesta in Faze.Pohyb:
            if cesta[0] == ObjektTile:
                Narocnost = cesta[1]
                break
        Faze.HracNaTahu.ZmenBodyPohybu(-Narocnost)
        Faze.NastavFaze(2)

        if Faze.DostupnaPole == []:
            if Faze.ZakazanoTlacitkoPokracovat:
                Faze.PovolitTlacitkoPokracovat()
            Faze.Pokracovat()
        elif not Faze.ZakazanoTlacitkoPokracovat and Faze.HracNaTahu.AktPole.PoziceNaMape in Faze.HracNaTahu.blacklist:
            Faze.ZakazatTlacitkoPokracovat()
        elif Faze.ZakazanoTlacitkoPokracovat and not Faze.HracNaTahu.AktPole.PoziceNaMape in Faze.HracNaTahu.blacklist:
            Faze.PovolitTlacitkoPokracovat()

    def Write(mouse_pos):
        if Faze.Zvyrazneno:
            Faze.Odzvyraznit()
        objekt = Faze.Mrizka.DostanObjektDlePozice(mouse_pos)
        if objekt == Faze.Info.Akt_objekt and (objekt != Faze.DefaultObraz[1] or Faze.Info.zvyraznit): # odvýrazněné napsání defaultního textu
            Faze.WriteDefault()
        elif objekt == Faze.DefaultObraz[1]: # zvýrazněné napsání defaultního textu
            Faze.Zvyraznit()
            Faze.WriteDefault(True)
        else: # normální napsání objektu
            Faze.Info.writeObj(objekt)

    def NastavDefaultVeci(DefaultObraz, DefaultSeznamFunkci = [], DefaultVlozitSeznam = []):
        Faze.DefaultObraz = DefaultObraz
        Faze.DefaultSeznamFunkci = DefaultSeznamFunkci
        Faze.DefaultVlozitSeznam = DefaultVlozitSeznam

    def WriteDefault(zvyraznit = False):
        Faze.Info.writeTyp(*Faze.DefaultObraz, zvyraznit, Faze.DefaultSeznamFunkci, Faze.DefaultVlozitSeznam)

    def UpdateListaPrehledHracu():
        Faze.TextListaPrehledHracu = []
        for pozice in range(Faze.PocetHracu):
            Faze.TextListaPrehledHracu.append({"pozice" : (0 / 100 * Faze.PrehledHracu.VelikostPismen, 4.8 * pozice / 100 * Faze.PrehledHracu.VelikostPismen),
                                               "bold" : pozice == Faze.IndexHracNaTahu
                                               })
            PoradiHrace = pozice + 1
            Faze.TextListaPrehledHracu.append("{PoradiHrace}. {{objekt[{pozice}].jmeno}}".format(pozice = pozice, PoradiHrace = PoradiHrace))
            Faze.TextListaPrehledHracu.extend(({"pozice" : (3/ 100 * Faze.PrehledHracu.VelikostPismen, 4.8 * (pozice + 0.5) / 100 * Faze.PrehledHracu.VelikostPismen)},
                                              "{{objekt[{pozice}].penize}}".format(pozice = pozice),
                                              Faze.ButtonNaListe(("next", 4.8 * (pozice + 0.5) / 100 * Faze.PrehledHracu.VelikostPismen), (2.3/ 100 * Faze.PrehledHracu.VelikostPismen, 2.3/ 100 * Faze.PrehledHracu.VelikostPismen), "Peniz.png", None, 255,  Faze.PrehledHracu),
                                              { "pozice" : (9/ 100 * Faze.PrehledHracu.VelikostPismen, 4.8 * (pozice + 0.5) / 100 * Faze.PrehledHracu.VelikostPismen)},
                                              "{{objekt[{pozice}].hedvabi}}".format(pozice = pozice), 
                                              Faze.ButtonNaListe(("next", 4.8 * (pozice + 0.5) / 100 * Faze.PrehledHracu.VelikostPismen), (2.3/ 100 * Faze.PrehledHracu.VelikostPismen, 2.3/ 100 * Faze.PrehledHracu.VelikostPismen), "Hedvabi.png", None, 255,  Faze.PrehledHracu),
                                              {"pozice" : (14/ 100 * Faze.PrehledHracu.VelikostPismen, 4.8 * (pozice + 0.5) / 100 * Faze.PrehledHracu.VelikostPismen)},
                                              "{{objekt[{pozice}].otroci}}".format(pozice = pozice),
                                              Faze.ButtonNaListe(("next", 4.8 * (pozice + 0.5) / 100 * Faze.PrehledHracu.VelikostPismen), (2.3/ 100 * Faze.PrehledHracu.VelikostPismen, 2.3/ 100 * Faze.PrehledHracu.VelikostPismen), "Otrok.png", None, 255,  Faze.PrehledHracu),
                                              { "pozice" : (19/ 100 * Faze.PrehledHracu.VelikostPismen, 4.8 * (pozice + 0.5) / 100 * Faze.PrehledHracu.VelikostPismen)},
                                              "{{objekt[{pozice}].sul}}".format(pozice = pozice),
                                              Faze.ButtonNaListe(("next", 4.8 * (pozice + 0.5) / 100 * Faze.PrehledHracu.VelikostPismen), (2.3/ 100 * Faze.PrehledHracu.VelikostPismen, 2.3/ 100 * Faze.PrehledHracu.VelikostPismen), "Sul.png", None, 255,  Faze.PrehledHracu),
                                              ))
        Faze.PrehledHracu.writeTyp("PrehledHracu", Faze.SeznamHracu, False, VlozitSeznam = [Faze.TextListaPrehledHracu])