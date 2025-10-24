class Agente:
    def __init__(self, MapaJuego):
        self.MapaJuego = MapaJuego
        self.PosicionInicial = [0,0]
        self.PosicionActual = [0,0]
        self.ObjetivoActual = [0,0]
################## KB #################################################
        self.AreasSeguras = [] # Se actualiza si es un cuarto vacio o son puro tesoro
        self.AreasVisitadas = [[0,0]] # Se actualiza conforme va visitando fisicamente lugares
        self.AreasRiesgo = [] # Se actualiza si hay brisa u olor
        self.AreasMortales = [] #Se actualiza si hay un monstruo o agujero
        self.Historial = []
######################################################################
        self.Vivo = True  
        self.OroInventario = False
        self.Presente = True
        self.Movimientos = 0
        self.Escapando = False
        self.Descubrir(self.PosicionActual)

    def Descubrir(self,Posicion):
        X, Y = Posicion
        RiesgosDescubiertos = []
        if self.MapaJuego[Y][X].Brisa == True or self.MapaJuego[Y][X].Olor == True:
            if Y+1 <= 3:
                PosicionDesc = [X, Y+1]
                if PosicionDesc not in self.AreasVisitadas and PosicionDesc not in self.AreasRiesgo:
                    self.AreasRiesgo.append(PosicionDesc)
                    RiesgosDescubiertos.append(PosicionDesc)
            if Y-1 >= 0:
                PosicionDesc = [X, Y-1]
                if PosicionDesc not in self.AreasVisitadas and PosicionDesc not in self.AreasRiesgo:
                    self.AreasRiesgo.append(PosicionDesc)
                    RiesgosDescubiertos.append(PosicionDesc)
            if X+1 <= 3:
                PosicionDesc = [X+1, Y]
                if PosicionDesc not in self.AreasVisitadas and PosicionDesc not in self.AreasRiesgo:
                    self.AreasRiesgo.append(PosicionDesc)
                    RiesgosDescubiertos.append(PosicionDesc)
            if X-1 >= 0:
                PosicionDesc = [X-1, Y]
                if PosicionDesc not in self.AreasVisitadas and PosicionDesc not in self.AreasRiesgo:
                    self.AreasRiesgo.append(PosicionDesc)
                    RiesgosDescubiertos.append(PosicionDesc)

            if len(RiesgosDescubiertos) == 1 and RiesgosDescubiertos not in self.AreasMortales:
                AreaMortal = RiesgosDescubiertos[0]
                if AreaMortal not in self.AreasMortales:
                   self.AreasMortales.append(AreaMortal)
                if AreaMortal in self.AreasRiesgo:
                    self.AreasRiesgo.remove(AreaMortal)

        else:
            if Y+1 <= 3:
                PosicionDesc = [X, Y+1]
                if PosicionDesc not in self.AreasVisitadas  and PosicionDesc not in self.AreasSeguras:
                    self.AreasSeguras.append([X, Y+1])
            if Y-1 >= 0:
                PosicionDesc = [X, Y-1]
                if PosicionDesc not in self.AreasVisitadas and PosicionDesc not in self.AreasSeguras:
                    self.AreasSeguras.append([X, Y-1])
            if X+1 <= 3:
                PosicionDesc = [X+1, Y]
                if PosicionDesc not in self.AreasVisitadas and PosicionDesc not in self.AreasSeguras:
                    self.AreasSeguras.append([X+1, Y])
            if X-1 >= 0:
                PosicionDesc = [X-1, Y]
                if PosicionDesc not in self.AreasVisitadas and PosicionDesc not in self.AreasSeguras:
                    self.AreasSeguras.append([X-1, Y])

    def ElegirCamino(self):
        AreasSegurasNoExploradas = list(filter(lambda x: x not in self.AreasVisitadas, self.AreasSeguras))
        AreasPeligrosasNoExploradas = list(filter(lambda x: x not in self.AreasVisitadas, self.AreasRiesgo))
        X,Y = self.PosicionActual

        if self.Movimientos >= 100:
            print("Ya alcance el limite de movimientos, me voy")
            self.Escapar()
            return
        
        self.DetectarMortales()
        
        if self.MapaJuego[Y][X].Tesoro == True:
            print("Encontre el tesoro, ahora tengo que escapar!")
            self.OroInventario = True
            self.Escapar()
            return
        if AreasSegurasNoExploradas:
            Objetivo = self.MejorDistancia(AreasSegurasNoExploradas)
            self.Trasladar(Objetivo)
        else:
            Objetivo = self.MejorDistancia(AreasPeligrosasNoExploradas)
            self.Trasladar(Objetivo)

    def MejorDistancia(self, PosiblesDestinos):
        if not PosiblesDestinos:
            print("No se como llegar.. mejor me voy") 
            self.Escapar()
        DistanciasGuardadas = []

        for i in range(len(PosiblesDestinos)):  
            Xact, Yact = self.PosicionActual
            Xdest, Ydest = PosiblesDestinos[i]
            Distancia = abs(Xact - Xdest) + abs(Yact - Ydest)
            DistanciasGuardadas.append(Distancia)

        IndiceMin = DistanciasGuardadas.index(min(DistanciasGuardadas))
        Objetivo = PosiblesDestinos[IndiceMin]
        return Objetivo
    
    def Trasladar(self, Destino):
        Xobj, Yobj = Destino


        while self.PosicionActual != Destino and self.Vivo and self.Presente:
            Xact, Yact = self.PosicionActual
            Distancia = abs(Xact - Xobj) + abs(Yact - Yobj)
            self.Movimientos+= 1

            if self.Movimientos >= 100 and not self.Escapando:
                print("Ya pase mucho tiempo aqui, tengo que reconsiderar mi ruta")
                return

            print(f"Estoy en: ({Xact}, {Yact}), Este es mi movimiento numero {self.Movimientos}")
            print(f"Marque el area en la que estoy con estas letras: {self.MapaJuego[Yact][Xact].ImpAtributos()} ")
            print(f"Los ultimos 3 lugares que visite son: {self.Historial}")
            print(f"Areas que ya visite: {self.AreasVisitadas}")
            print(f"Riesgos que conozco: {self.AreasRiesgo}")
            print(f"Areas seguras que conozco: {self.AreasSeguras}")
            print(f"Areas mortales que tengo que evitar: {self.AreasMortales}")            
            print(" ")

            if self.PosicionActual in self.AreasMortales or (self.MapaJuego[Yact][Xact].Wumpus or self.MapaJuego[Yact][Xact].Agujero):
                self.Vivo = False
                print("LA IA HA MUERTO A CAUSA DE UNA MALA DECISION")
                return
    

            if Distancia == 1:
                if Destino in self.AreasMortales:
                    print("No puedo ir ahí, me puedo morir")
                    self.Escapar()
                    return
                
                self.PosicionActual = Destino
                self.Historial.append(self.PosicionActual)
                self.ActualizarHistorial()


                if self.PosicionActual not in self.AreasVisitadas:
                    self.Descubrir(self.PosicionActual)
                    self.AreasVisitadas.append(self.PosicionActual)
                    break 

            else:
                Alrededores = [[Xact, Yact+1],[Xact, Yact-1],[Xact+1, Yact],[Xact-1, Yact]]
                Alrededores = [c for c in Alrededores if 0 <= c[0] <= 3 and 0 <= c[1]<= 3]
                Alrededores = [c for c in Alrededores if c not in self.AreasMortales]

                Coincidente = [c for c in Alrededores if c in self.AreasVisitadas and self.Historial.count(c) < 2]

                if not Coincidente:
                    Coincidente = [c for c in Alrededores if c in self.AreasSeguras and c not in self.AreasVisitadas]
 
                if not Coincidente:
                    Coincidente = [c for c in Alrededores if c in self.AreasRiesgo and c not in self.AreasVisitadas]
 
                if not Coincidente:
                    Coincidente = Alrededores

                ObjetivoNuevo = self.MejorDistancia(Coincidente)

                if not Coincidente:
                    if Destino != [0,0]:
                        print("No hay camino")
                        self.Escapar()
                        return
                    else:
                        print("ERROR GRAVE: NO HAY CAMINO NI SE PUEDE ESCAPAR")
                        self.Presente = False
                        return   
                      
                self.PosicionActual = ObjetivoNuevo
                self.Historial.append(self.PosicionActual)
                self.ActualizarHistorial()

            if self.PosicionActual not in self.AreasVisitadas:
                self.AreasVisitadas.append(self.PosicionActual)
                self.Descubrir(self.PosicionActual)
                if self.PosicionActual in self.AreasRiesgo:
                    self.AreasRiesgo.remove(self.PosicionActual)
                
    def Escapar(self):
        self.Trasladar([0,0])
        self.Presente = False
        self.Escapando = True
        if self.OroInventario and self.Vivo:
            print("La IA escapo con el tesoro adquirido")
            print(f"Movimientos totales: {self.Movimientos}")
        else:  
            print("La IA escapo sin el tesoro")
            print(f"Movimientos totales: {self.Movimientos}")
    
    def ActualizarHistorial(self):
        if len(self.Historial) > 5:
            self.Historial.pop(0)
    
    def DetectarMortales(self):
        Xact, Yact = self.PosicionActual
        Alrededores = [[Xact, Yact+1],[Xact, Yact-1],[Xact+1, Yact],[Xact-1, Yact]]
        Alrededores = [c for c in Alrededores if 0 <= c[0] <= 3 and 0 <= c[1]<= 3]     
        RiesgoTemporal = []

        for i in range(len(Alrededores)):
            if Alrededores[i] in self.AreasRiesgo and Alrededores[i] not in self.AreasVisitadas:
                RiesgoTemporal.append(Alrededores[i])

        if len(RiesgoTemporal) == 1 :
            AreaMortal = RiesgoTemporal[0]
            if AreaMortal not in self.AreasMortales:
                self.AreasMortales.append(AreaMortal)
                print(f"Solo queda una casilla de riesgo cerca.. por lo que asumo que {RiesgoTemporal} me llevara a la muerte")

