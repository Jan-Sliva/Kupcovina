import pygame, math, random, sys

class Funkce():

    def init(ObjektFaze, SeznamGrid, SeznamLista, SeznamTlacitko):
        Funkce.Faze = ObjektFaze
        Funkce.SeznamGrid = SeznamGrid
        Funkce.SeznamList = SeznamLista
        Funkce.SeznamTlacitko = SeznamTlacitko

    def Exit():
        pygame.quit()
        sys.exit(0)

    ### city_tile - zpet do obchodniho prehledu
    def ZpetObchodCityTile():
        Funkce.Faze.NastavDefaultVeci(("ObchodCityTile", Funkce.Faze.HracNaTahu.AktPole))
        Funkce.Faze.Info.writeTyp(*Funkce.Faze.DefaultObraz, False)

    ### city_tile - koupit
    def JitKoupitHedvabi():
        Funkce.Faze.NastavDefaultVeci(("ObchodCityTileHK", Funkce.Faze.HracNaTahu.AktPole), [[Funkce.DostanCelkovouKupCenuHedvabi]])
        Funkce.Faze.WriteDefault()
        maximum = min(Funkce.Faze.HracNaTahu.MaxHedvabi - Funkce.Faze.HracNaTahu.hedvabi,
                      math.floor(Funkce.Faze.HracNaTahu.penize / Funkce.Faze.Info.Akt_objekt.KupniCenaHedvabi),
                      Funkce.Faze.Info.Akt_objekt.PocetHedvabi)
        Funkce.Faze.Info.SeznamAktivovanychPosuvnik[0].NastavRozmezi((min(1, maximum), maximum))
        Funkce.Faze.Info.Aktualizovat()

    def KoupitHedvabi():
        Funkce.Faze.Info.Akt_objekt.KoupitHedvabi(Funkce.Faze.HracNaTahu, Funkce.Faze.Info.udaj[0])
        Funkce.ZpetObchodCityTile()
        Funkce.Faze.PrehledHracu.Aktualizovat()

    def DostanCelkovouKupCenuHedvabi():
        return Funkce.Faze.Info.Akt_objekt.KupniCenaHedvabi * Funkce.Faze.Info.udaj[0]

    def JitKoupitOtroci():
        Funkce.Faze.NastavDefaultVeci(("ObchodCityTileOK", Funkce.Faze.HracNaTahu.AktPole), [[Funkce.DostanCelkovouKupCenuOtroci]])
        Funkce.Faze.WriteDefault()
        maximum = min(Funkce.Faze.HracNaTahu.MaxOtroci - Funkce.Faze.HracNaTahu.otroci,
                      math.floor(Funkce.Faze.HracNaTahu.penize / Funkce.Faze.Info.Akt_objekt.KupniCenaOtroci),
                      Funkce.Faze.Info.Akt_objekt.PocetOtroci)
        Funkce.Faze.Info.SeznamAktivovanychPosuvnik[0].NastavRozmezi((min(1, maximum), maximum))
        Funkce.Faze.Info.Aktualizovat()

    def KoupitOtroci():
        Funkce.Faze.Info.Akt_objekt.KoupitOtroci(Funkce.Faze.HracNaTahu, Funkce.Faze.Info.udaj[0])
        Funkce.ZpetObchodCityTile()
        Funkce.Faze.PrehledHracu.Aktualizovat()

    def DostanCelkovouKupCenuOtroci():
        return Funkce.Faze.Info.Akt_objekt.KupniCenaOtroci * Funkce.Faze.Info.udaj[0]

    def JitKoupitSul():
        Funkce.Faze.NastavDefaultVeci(("ObchodCityTileSK", Funkce.Faze.HracNaTahu.AktPole), [[Funkce.DostanCelkovouKupCenuSul]])
        Funkce.Faze.WriteDefault()
        maximum = min(Funkce.Faze.HracNaTahu.MaxSul - Funkce.Faze.HracNaTahu.sul,
                      math.floor(Funkce.Faze.HracNaTahu.penize / Funkce.Faze.Info.Akt_objekt.KupniCenaSul),
                      Funkce.Faze.Info.Akt_objekt.PocetSul)
        Funkce.Faze.Info.SeznamAktivovanychPosuvnik[0].NastavRozmezi((min(1, maximum), maximum))
        Funkce.Faze.Info.Aktualizovat()

    def KoupitSul():
        Funkce.Faze.Info.Akt_objekt.KoupitSul(Funkce.Faze.HracNaTahu, Funkce.Faze.Info.udaj[0])
        Funkce.ZpetObchodCityTile()
        Funkce.Faze.PrehledHracu.Aktualizovat()

    def DostanCelkovouKupCenuSul():
        return Funkce.Faze.Info.Akt_objekt.KupniCenaSul * Funkce.Faze.Info.udaj[0]

    ### city_tile - prodat
    def JitProdatHedvabi():
        Funkce.Faze.NastavDefaultVeci(("ObchodCityTileHP", Funkce.Faze.HracNaTahu.AktPole), [[Funkce.DostanCelkovouProdCenuHedvabi]])
        Funkce.Faze.WriteDefault()
        maximum = min(Funkce.Faze.HracNaTahu.hedvabi,
                      Funkce.Faze.Info.Akt_objekt.MaxHedvabi - Funkce.Faze.Info.Akt_objekt.PocetHedvabi)
        Funkce.Faze.Info.SeznamAktivovanychPosuvnik[0].NastavRozmezi((min(1, maximum), maximum))
        Funkce.Faze.Info.Aktualizovat()

    def ProdatHedvabi():
        Funkce.Faze.Info.Akt_objekt.ProdatHedvabi(Funkce.Faze.HracNaTahu, Funkce.Faze.Info.udaj[0])
        Funkce.ZpetObchodCityTile()
        Funkce.Faze.PrehledHracu.Aktualizovat()

    def DostanCelkovouProdCenuHedvabi():
        return Funkce.Faze.Info.Akt_objekt.ProdejniCenaHedvabi * Funkce.Faze.Info.udaj[0]

    def JitProdatOtroci():
        Funkce.Faze.NastavDefaultVeci(("ObchodCityTileOP", Funkce.Faze.HracNaTahu.AktPole), [[Funkce.DostanCelkovouProdCenuOtroci]])
        Funkce.Faze.WriteDefault()
        maximum = min(Funkce.Faze.HracNaTahu.otroci,
                      Funkce.Faze.Info.Akt_objekt.MaxOtroci - Funkce.Faze.Info.Akt_objekt.PocetOtroci)
        Funkce.Faze.Info.SeznamAktivovanychPosuvnik[0].NastavRozmezi((min(1, maximum), maximum))
        Funkce.Faze.Info.Aktualizovat()

    def ProdatOtroci():
        Funkce.Faze.Info.Akt_objekt.ProdatOtroci(Funkce.Faze.HracNaTahu, Funkce.Faze.Info.udaj[0])
        Funkce.ZpetObchodCityTile()
        Funkce.Faze.PrehledHracu.Aktualizovat()

    def DostanCelkovouProdCenuOtroci():
        return Funkce.Faze.Info.Akt_objekt.ProdejniCenaOtroci * Funkce.Faze.Info.udaj[0]

    def JitProdatSul():
        Funkce.Faze.NastavDefaultVeci(("ObchodCityTileSP", Funkce.Faze.HracNaTahu.AktPole), [[Funkce.DostanCelkovouProdCenuSul]])
        Funkce.Faze.WriteDefault()
        maximum = min(Funkce.Faze.HracNaTahu.sul,
                      Funkce.Faze.Info.Akt_objekt.MaxSul - Funkce.Faze.Info.Akt_objekt.PocetSul)
        Funkce.Faze.Info.SeznamAktivovanychPosuvnik[0].NastavRozmezi((min(1, maximum), maximum))
        Funkce.Faze.Info.Aktualizovat()

    def ProdatSul():
        Funkce.Faze.Info.Akt_objekt.ProdatSul(Funkce.Faze.HracNaTahu, Funkce.Faze.Info.udaj[0])
        Funkce.ZpetObchodCityTile()
        Funkce.Faze.PrehledHracu.Aktualizovat()

    def DostanCelkovouProdCenuSul():
        return Funkce.Faze.Info.Akt_objekt.ProdejniCenaSul * Funkce.Faze.Info.udaj[0]

    ### repository_tile - koupit
    def ZdrojDostanCelkovouKupCenu():
        return Funkce.Faze.Info.Akt_objekt.KupniCena * Funkce.Faze.Info.udaj[0]

    def ZdrojKoupit():
        Funkce.Faze.Info.Akt_objekt.Koupit(Funkce.Faze.HracNaTahu, Funkce.Faze.Info.udaj[0])
        Funkce.Faze.PrehledHracu.Aktualizovat()
        Funkce.Faze.HracNaTahu.AktPole.KoupitFunkce()

    def ZdrojJitKoupitHedvabi():
        Funkce.Faze.NastavDefaultVeci(("ObchodZdroj", Funkce.Faze.HracNaTahu.AktPole), [[Funkce.ZdrojDostanCelkovouKupCenu]])
        Funkce.Faze.WriteDefault()
        maximum = min(Funkce.Faze.HracNaTahu.MaxHedvabi - Funkce.Faze.HracNaTahu.hedvabi,
                      math.floor(Funkce.Faze.HracNaTahu.penize / Funkce.Faze.Info.Akt_objekt.KupniCena))
        Funkce.Faze.Info.SeznamAktivovanychPosuvnik[0].NastavRozmezi((min(1, maximum), maximum))
        Funkce.Faze.Info.Aktualizovat()

    def ZdrojJitKoupitOtroci():
        Funkce.Faze.NastavDefaultVeci(("ObchodZdroj", Funkce.Faze.HracNaTahu.AktPole), [[Funkce.ZdrojDostanCelkovouKupCenu]])
        Funkce.Faze.WriteDefault()
        maximum = min(Funkce.Faze.HracNaTahu.MaxOtroci - Funkce.Faze.HracNaTahu.otroci,
                      math.floor(Funkce.Faze.HracNaTahu.penize / Funkce.Faze.Info.Akt_objekt.KupniCena))
        Funkce.Faze.Info.SeznamAktivovanychPosuvnik[0].NastavRozmezi((min(1, maximum), maximum))
        Funkce.Faze.Info.Aktualizovat()

    def ZdrojJitKoupitSul():
        Funkce.Faze.NastavDefaultVeci(("ObchodZdroj", Funkce.Faze.HracNaTahu.AktPole), [[Funkce.ZdrojDostanCelkovouKupCenu]])
        Funkce.Faze.WriteDefault()
        maximum = min(Funkce.Faze.HracNaTahu.MaxSul - Funkce.Faze.HracNaTahu.sul,
                      math.floor(Funkce.Faze.HracNaTahu.penize / Funkce.Faze.Info.Akt_objekt.KupniCena))
        Funkce.Faze.Info.SeznamAktivovanychPosuvnik[0].NastavRozmezi((min(1, maximum), maximum))
        Funkce.Faze.Info.Aktualizovat()

    ### treasure_tile - poklad
    def PokladDostat():
        Funkce.Faze.HracNaTahu.ZmenHedvabi(Funkce.Faze.Info.Akt_objekt.DostatHedvabi)
        Funkce.Faze.HracNaTahu.ZmenSul(Funkce.Faze.Info.Akt_objekt.DostatSul)
        Funkce.Faze.HracNaTahu.ZmenPenize(Funkce.Faze.Info.Akt_objekt.DostatPenize)

        Funkce.Faze.Info.Akt_objekt.ZmenSeNaPrazdny()

        del Funkce.Faze.DefaultVlozitSeznam[0][-1]
        Funkce.Faze.NastavDefaultVeci(("PokladOtevreny", Funkce.Faze.HracNaTahu.AktPole), DefaultVlozitSeznam =  Funkce.Faze.DefaultVlozitSeznam)
        Funkce.Faze.WriteDefault()
        Funkce.Faze.PrehledHracu.Aktualizovat()

    ### začáteční nastavení
    def InitForZacatecniVyber(MainLoop, ZacatecnyLista, UkoncitZacniMainLoop, JitVybiratJmena):
        Funkce.MainLoop = MainLoop
        Funkce.ZacatecnyLista = ZacatecnyLista
        Funkce.UkoncitZacniMainLoop = UkoncitZacniMainLoop
        Funkce.JitVybiratJmena = JitVybiratJmena

    def PotvrditPocetHracu():
        Funkce.JitVybiratJmena()

    ### Akce
    def AkceDostatPenize():
        return Funkce.Faze.HracNaTahu.ZmenPenize(Funkce.Faze.ObjektAkce.AktAkce.Pocet)

    def AkceDostatHedvabi():
        return Funkce.Faze.HracNaTahu.ZmenHedvabi(Funkce.Faze.ObjektAkce.AktAkce.Pocet)

    def AkceDostatOtroci():
        return Funkce.Faze.HracNaTahu.ZmenOtroci(Funkce.Faze.ObjektAkce.AktAkce.Pocet)

    def AkceDostatSul():
        return Funkce.Faze.HracNaTahu.ZmenSul(Funkce.Faze.ObjektAkce.AktAkce.Pocet)

    def AkceDostatBodyPohybu():
        Funkce.Faze.HracNaTahu.ZmenBodyPohybu(Funkce.Faze.ObjektAkce.AktAkce.Pocet)
        return True

    def Nic():
        return True
        
