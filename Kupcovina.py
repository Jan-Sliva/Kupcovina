from grid import *
from Faze import *
from lista import *
from Akce import *
from TextovyButton import *
import sys

def Menu(MenuObr, Slozka):
    MenuScreenObrUnscal = pygame.image.load(os.path.join(Slozka,  MenuObr)).convert()
    MenuScreenObr = pygame.transform.smoothscale(MenuScreenObrUnscal, (math.ceil(screen_rozmery[0]), math.ceil(screen_rozmery[1])))

    # initování tlačítek
    SeznamTlacitek = []
    TlacitkoHrat = Button((screen_rozmery[0] * 220/707, screen_rozmery[1] * 250/500), (screen_rozmery[0] * 260 / 707, screen_rozmery[1] * 45/500), "Hrat.png", "Obrazky", 255, ZacitMainLoop)
    TlacitkoOdejit = Button((screen_rozmery[0] * 220/707, screen_rozmery[1] * 325/500), (screen_rozmery[0] * 260 / 707, screen_rozmery[1] * 45/500), "Odejit.png", "Obrazky", 255, Funkce.Exit)
    SeznamTlacitek.append(TlacitkoHrat)
    SeznamTlacitek.append(TlacitkoOdejit)

    #jestli je nová hra
    global NewGame
    NewGame = False

    menu_quit = False
    while not menu_quit:

        screen.blit(MenuScreenObr, (0, 0))
        for Tlacitko in SeznamTlacitek:
            Tlacitko.Ukazat(screen)
        pygame.display.flip()
        pygame.display.update()
        main_clock.tick(FPS)

        screen.fill((0, 0, 0))
        mouse_pos = pygame.mouse.get_pos()
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_quit = True
                Funkce.Exit()

            if event.type == pygame.KEYDOWN:
                klavesy = pygame.key.get_pressed()
        
                if (klavesy[pygame.K_F4] and (klavesy[pygame.K_RALT] or klavesy[pygame.K_LALT])):
                    menu_quit = True
                    Funkce.Exit()

                if klavesy[pygame.K_ESCAPE]: # Pozor escape ukončuje mainloop!
                    menu_quit = True

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for Tlacitko in SeznamTlacitek:
                    if Tlacitko.MysJeNa(mouse_pos):
                        Tlacitko.funkce()

            

def ZacitMainLoop():
    JmenaHracu = []
    
    def UkoncitZacniMainLoop():
        nonlocal vyber_quit
        vyber_quit = True
    def DalsiVybiratJmena():
        nonlocal JmenaHracu
        global Text, PocetHracu
        JmenaHracu.append(Text.Text)
        ZacatecniVyber.writeTyp("VyberJmena", [len(JmenaHracu) + 1], False)
        Text.ResetText()
        if PocetHracu == len(JmenaHracu):
            MainLoop(JmenaHracu, 70)
            UkoncitZacniMainLoop()
    def JitVybiratJmena():
        nonlocal SeznamTlacitek, DalsiVybiratJmena, SeznamText, ZacatecniVyber, mouse_pos
        global Text, PocetHracu
        mouse_pos = (0, 0)
        PocetHracu = Funkce.ZacatecnyLista.udaj[0]
        Text = TextovyButton((screen_rozmery[0] * 220/707, screen_rozmery[1] * 250/500), (screen_rozmery[0] * 260 / 707, screen_rozmery[1] * 45/500), "PozadiTextu.png", "Obrazky", 255, "", "Kurzor.png")
        SeznamText.append(Text)
        Confirm = Button((screen_rozmery[0] * 220/707, screen_rozmery[1] * 325/500), (screen_rozmery[0] * 260 / 707, screen_rozmery[1] * 45/500), "Dale.png", "Obrazky", 255, DalsiVybiratJmena)
        SeznamTlacitek.append(Text)
        SeznamTlacitek.append(Confirm)
        ZacatecniVyber.writeTyp("VyberJmena", [1], False)

    

    SeznamList = []
    ZacatecniVyber = lista((0, 0), screen_rozmery, "Menu", screen_rozmery[1], 255)
    ZacatecniVyber.writeTyp("VyberPoctuHracu", None, False)
    SeznamList.append(ZacatecniVyber)
    ZacatecniVyber.ZarovnatTlacitkaNaStred()

    SeznamTlacitek = []
    SeznamText = []
    
    Funkce.InitForZacatecniVyber(MainLoop, ZacatecniVyber, UkoncitZacniMainLoop, JitVybiratJmena)

    vyber_quit = False
    while not vyber_quit:

        for Lista in SeznamList:
            Lista.Ukazat(screen)
        for Tlacitko in SeznamTlacitek:
            Tlacitko.Ukazat(screen)
        pygame.display.flip()
        pygame.display.update()
        main_clock.tick(FPS)

        screen.fill((0, 0, 0))
        mouse_pos = pygame.mouse.get_pos()
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                vyber_quit = True
                Funkce.Exit()

            if event.type == pygame.KEYDOWN:
                klavesy = pygame.key.get_pressed()
        
                if (klavesy[pygame.K_F4] and (klavesy[pygame.K_RALT] or klavesy[pygame.K_LALT])):
                    vyber_quit = True
                    Funkce.Exit()

                if klavesy[pygame.K_ESCAPE]: # Pozor escape ukončuje mainloop!
                    vyber_quit = True

            for Lista in SeznamList:
                if Lista.MysJeNa(mouse_pos):
                    for tlacitko in Lista.SeznamAktivovanychButton:
                        if tlacitko.StisknutoNa(mouse_pos, event):
                            tlacitko.funkce()
                for posuvnik in Lista.SeznamAktivovanychPosuvnik:
                    if posuvnik.StisknutoNaPosuvnik(mouse_pos, event):
                        posuvnik.start_Posun(mouse_pos[0])
                    elif event.type == pygame.MOUSEBUTTONUP:
                        posuvnik.end_Posun()
                    else:
                        posuvnik.Posun(mouse_pos[0])

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for Tlacitko in SeznamTlacitek:
                    if Tlacitko.MysJeNa(mouse_pos):
                        Tlacitko.funkce()
                for TextLista in SeznamText:
                    if not TextLista.MysJeNa(mouse_pos):
                        TextLista.UkoncitPsat()

            if event.type == pygame.KEYDOWN:
                for TextLista in SeznamText:
                    if event.key == pygame.K_BACKSPACE:
                        TextLista.Vymaz()
                    else:
                        TextLista.Napis(event.unicode)

    global NewGame
    if NewGame:
        NewGame = False
        ZacitMainLoop()

           

def KonecMenu(PoradiHracu):
    def UkoncitKonecMenu(): 
        nonlocal end_quit
        end_quit = True

    SeznamList = []
    TabulkaHracu = []
    KonecMenu = lista((0, 0), screen_rozmery, "Menu", screen_rozmery[1], 255)
    for i in range(0, len(PoradiHracu)):
        Misto = i + 1
        TabulkaHracu.append(f"{Misto}. místo: {{objekt[{i}].jmeno}} s {{objekt[{i}].penize}}")
        TabulkaHracu.append(ButtonNaListe(("next", (9 * (i + 1) + 6) / 100 * KonecMenu.VelikostPismen), (9 / 100 * KonecMenu.VelikostPismen, 9/ 100 * KonecMenu.VelikostPismen), "Peniz.png", None, 255,  KonecMenu))

    def DvojFunkce():
        global NewGame
        UkoncitKonecMenu()
        NewGame = True
    TabulkaHracu.append(ButtonNaListe((0, (9 * (len(PoradiHracu) + 1.5) + 6)/ 100 * KonecMenu.VelikostPismen), ((9 * 260/45)/ 100 * KonecMenu.VelikostPismen, 9/ 100 * KonecMenu.VelikostPismen), "HratZnovu.png", DvojFunkce, 255,  KonecMenu))
    TabulkaHracu.append(ButtonNaListe((0, (9 * (len(PoradiHracu) + 3) + 6)/ 100 * KonecMenu.VelikostPismen), ((9 * 260/45)/ 100 * KonecMenu.VelikostPismen, 9/ 100 * KonecMenu.VelikostPismen), "HlavniMenu.png", UkoncitKonecMenu, 255,  KonecMenu))
    
    KonecMenu.writeTyp("KonecMenu", PoradiHracu, False, [], [TabulkaHracu])
    SeznamList.append(KonecMenu)
    KonecMenu.ZarovnatTlacitkaNaStred()

    end_quit = False
    while not end_quit:
        for Lista in SeznamList:
            Lista.Ukazat(screen)
        pygame.display.flip()
        pygame.display.update()
        main_clock.tick(FPS)

        screen.fill((0, 0, 0))
        mouse_pos = pygame.mouse.get_pos()
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                vyber_quit = True
                Funkce.Exit()

            if event.type == pygame.KEYDOWN:
                klavesy = pygame.key.get_pressed()
        
                if (klavesy[pygame.K_F4] and (klavesy[pygame.K_RALT] or klavesy[pygame.K_LALT])):
                    vyber_quit = True
                    Funkce.Exit()

                if klavesy[pygame.K_ESCAPE]: # Pozor escape ukončuje mainloop!
                    end_quit = True

            for Lista in SeznamList:
                if Lista.MysJeNa(mouse_pos):
                    for tlacitko in Lista.SeznamAktivovanychButton:
                        if tlacitko.StisknutoNa(mouse_pos, event):
                            tlacitko.funkce()
                for posuvnik in Lista.SeznamAktivovanychPosuvnik:
                    if posuvnik.StisknutoNaPosuvnik(mouse_pos, event):
                        posuvnik.start_Posun(mouse_pos[0])
                    elif event.type == pygame.MOUSEBUTTONUP:
                        posuvnik.end_Posun()
                    else:
                        posuvnik.Posun(mouse_pos[0])

            

def MainLoop(SeznamJmen, KonecHryPenez):
    def UkoncitMainLoop():
        nonlocal game_quit
        game_quit = True

    #nastavení lišt
    SeznamList = []
    Info = lista((screen_rozmery[0] - screen_rozmery[1]/3, screen_rozmery[1]/15 + screen_rozmery[1] * 1 / 20), (screen_rozmery[1]/3, screen_rozmery[1] * (8 / 15 - 1 / 20 )), "Lista", screen_rozmery[1], 255)
    PrehledFazi = lista((screen_rozmery[0] - screen_rozmery[1]/3, screen_rozmery[1] * 1 / 15), (screen_rozmery[1]/3, screen_rozmery[1] * 1 / 20), "PrehledFazi", screen_rozmery[1], 255)
    PrehledHracu = lista((screen_rozmery[0] - screen_rozmery[1]/3, screen_rozmery[1] * 9 / 15), (screen_rozmery[1]/3, screen_rozmery[1] * 6 / 15), "PrehledHracu", screen_rozmery[1], 255)
    SeznamList.append(Info)
    SeznamList.append(PrehledFazi)
    SeznamList.append(PrehledHracu)

    #funkce Aktualizovat, ktrerá aktualizuje lišty
    def Aktualizovat(objekt):
        Info.Update_text_obj(objekt)
        typAktObjekt = type(PrehledHracu.Akt_objekt)
        if (typAktObjekt is tuple or typAktObjekt is list) and objekt in PrehledHracu.Akt_objekt:
            PrehledHracu.Aktualizovat()

    #nastavení mřížka
    Mrizka = grid((0, 0), (screen_rozmery[0] - screen_rozmery[1]/3, screen_rozmery[1]), "Mrizka", 1.2, 140, 255)
    Mrizka.create_tile((0, 0), Aktualizovat)
    for pole in map_obj.okoli:
        Mrizka.create_tile(pole, Aktualizovat)

    PoziceHracu = [[(0, -4), (0, 4)], [(0, -4), (2, 2), (-2, 2)], [(0, -4), (2, 0), (0, 4), (-2, 0)], [(2, -2), (2, 2), (0, 4), (-2, 2), (-2, -2)], [(0, -4), (2, -2), (2, 2), (0, 4), (-2, 2), (-2, -2)]]
    ObrazkyHracu = ("red.png", "blue.png", "green.png", "yellow.png", "purple.png", "grey.png")
    #nastavení hráčů
    PocetHracu = len(SeznamJmen)
    Seznam_hracu = []
    for i in range(PocetHracu):
        Seznam_hracu.append(player(PoziceHracu[PocetHracu-2][i], Mrizka, Aktualizovat, 2.4, ObrazkyHracu[i], "Obrazky", SeznamJmen[i]))

    
    #nastavení tlačítek
    SeznamTlacitek = []
    TlacitkoPokracovat = Button((screen_rozmery[0] - screen_rozmery[1]/3, 0), (screen_rozmery[1]/3, screen_rozmery[1] /15), "Pokracovat1ku5.png", "Obrazky", 255, Faze.Pokracovat)
    TlacitkoPokracovat.ImportObr("Pokracovat1ku5Neakt.png")
    TlacitkoPokracovat.ImportObr("UkoncitPohyb1ku5.png")
    TlacitkoPokracovat.ImportObr("UkoncitPohyb1ku5Neakt.png")
    TlacitkoPokracovat.ImportObr("UkoncitTah1ku5.png")
    TlacitkoPokracovat.ImportObr("UkoncitTah1ku5Neakt.png")
    SeznamTlacitek.append(TlacitkoPokracovat)

    #nastavení objektu pro funkce pro tlačítka
    Funkce.init(Faze, (Mrizka), SeznamList, SeznamTlacitek)

    #nastavení objektu pro počítání fází
    Faze.init(Seznam_hracu, 0, Mrizka, lista, Info, PrehledFazi, PrehledHracu, TlacitkoPokracovat, normal_tile, city_tile, repository_tile, treasure_tile, ButtonNaListe, AkceSeznam,
             KonecHryPenez, KonecMenu, UkoncitMainLoop)

    #napsání správných věcí na lištách
    Faze.UpdateListaPrehledHracu()


    game_quit = False
    while not game_quit:
        Mrizka.Ukazat(screen)
        for Lista in SeznamList:
            Lista.Ukazat(screen)
        for Tlacitko in SeznamTlacitek:
            Tlacitko.Ukazat(screen)
        pygame.display.flip()
        pygame.display.update()
        main_clock.tick(FPS)

        screen.fill((0, 0, 0))
        mouse_pos = pygame.mouse.get_pos()
    
        for event in pygame.event.get():
        
            if event.type == pygame.QUIT:
                game_quit = True
                Funkce.Exit()

            if event.type == pygame.KEYDOWN:
                klavesy = pygame.key.get_pressed()
        
                if (klavesy[pygame.K_F4] and (klavesy[pygame.K_RALT] or klavesy[pygame.K_LALT])):
                    game_quit = True
                    Funkce.Exit()

                if klavesy[pygame.K_ESCAPE]: # Pozor escape ukončuje mainloop!
                    game_quit = True

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
                doubleclick = doubleclick_clock.tick() <= 500
                if doubleclick and Faze.faze == 2:
                    objekt = Mrizka.DostanObjektDlePozice(mouse_pos)
                    if tile in type(objekt).__bases__ and objekt in Faze.DostupnaPole:
                        Faze.ZmenPoziciHracNaTahu(objekt)


            if Mrizka.MysJeNa(mouse_pos):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if Mrizka.MysJeNaPolicku(mouse_pos):
                        if event.button == 4: # zvětšování
                            Mrizka.Pribliz(True, mouse_pos)
                        elif event.button == 5: # zmenšování
                            Mrizka.Pribliz(False, mouse_pos)
                        elif event.button == 1:
                            Mrizka.start_move()
                        elif event.button == 3: # pravé tlačítko, zobrazit (změnit) informace
                            Faze.Write(mouse_pos)
                    if event.button == 2: # stisknuté kolečko od myši, reset zvětšení
                        pozicenamape = Faze.HracNaTahu.AktPole.PoziceNaMape
                        if Mrizka.started_move:
                            Mrizka.end_move()
                            Mrizka.reset_zoom(200, pozicenamape, True)
                        else:
                            Mrizka.reset_zoom(200, pozicenamape, True)
                        Mrizka.last_mouse = mouse_pos

                    
            if event.type == pygame.MOUSEMOTION: # pohyb s mapou
                if event.buttons[0] == 1:
                    Mrizka.move(mouse_pos)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and Mrizka.started_move: # konec pohybu s mapou
                    Mrizka.end_move()
        
            for Lista in SeznamList:
                if Lista.MysJeNa(mouse_pos):
                    for tlacitko in Lista.SeznamAktivovanychButton:
                        if tlacitko.StisknutoNa(mouse_pos, event):
                            tlacitko.funkce()
                for posuvnik in Lista.SeznamAktivovanychPosuvnik:
                    if posuvnik.StisknutoNaPosuvnik(mouse_pos, event):
                        posuvnik.start_Posun(mouse_pos[0])
                    elif event.type == pygame.MOUSEBUTTONUP:
                        posuvnik.end_Posun()
                    else:
                        posuvnik.Posun(mouse_pos[0])

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for Tlacitko in SeznamTlacitek:
                    if Tlacitko.MysJeNa(mouse_pos):
                        Tlacitko.funkce()


# Nastavení rozměrů
pygame.init()
pygame.display.set_caption("Kupcovina")
screen = pygame.display.set_mode(flags = pygame.FULLSCREEN) # na celou obrazovku
#screen = pygame.display.set_mode((1500, 1000))
screen_rozmery = screen.get_size()

#nastavení časovačů
main_clock = pygame.time.Clock()
FPS = 120
doubleclick_clock = pygame.time.Clock()

Menu("UvodniStrana.png", "Obrazky")
        
Funkce.Exit()