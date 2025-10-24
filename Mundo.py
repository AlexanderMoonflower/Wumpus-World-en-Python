import numpy as np
from random import randint
from ClaseCasilla import Casilla

class mundo:
    def __init__(self):
        self.mapa = []
        self.wumpus = []
        self.agujeros = []
        self.tesoro= []

    def generar_mundo(self):
        AgujerosCont = 0
        TesoroCont = 0
        WumpusExiste = False

        Mundo = [[Casilla(),Casilla(),Casilla(),Casilla()],
                [Casilla(),Casilla(),Casilla(),Casilla()],
                [Casilla(),Casilla(),Casilla(),Casilla()],
                [Casilla(),Casilla(),Casilla(),Casilla()]]
        
        for i in range (16):
            if WumpusExiste == False:
                X = randint(0,3)
                Y = randint(0,3) 
                if not (X == 0 and Y == 0):
                    self.wumpus = [X,Y]
                    Mundo[Y][X].Wumpus = True
                    Mundo[Y][X].Vacio = False
                    WumpusExiste = True
                    Mundo = self.GenerarBrisaYOlor(X, Y, Mundo)

            elif AgujerosCont < 3 : 
                X = randint(0,3)
                Y = randint(0,3) 
                if not (X == 0 and Y == 0) and Mundo[Y][X].Wumpus == False:
                    self.agujeros.append([X,Y])
                    Mundo[Y][X].Agujero = True
                    Mundo[Y][X].Vacio = False
                    AgujerosCont+=1
                    Mundo = self.GenerarBrisaYOlor(X, Y, Mundo)

            elif TesoroCont == 0:
                    X = randint(0,3)
                    Y = randint(0,3) 
                    if not (X == 0 and Y == 0) and Mundo[Y][X].Agujero == False and Mundo[Y][X].Wumpus == False:
                        self.tesoro = [X,Y]
                        Mundo[Y][X].Tesoro = True
                        Mundo[Y][X].Vacio = False
                        TesoroCont+=1
        self.mapa = Mundo
        return Mundo

    def GenerarBrisaYOlor(self, X, Y, Mundo):
        # Recordatorio: X y Y en las matrices estan volteadas entonces las coordenadas siempre seran Y,X y no X,Y
        # Arriba
        if Y+1 <= 3:
            Mundo[Y+1][X].Vacio = False
            if Mundo[Y][X].Agujero:
                Mundo[Y+1][X].Brisa = True
            else: 
                Mundo[Y+1][X].Olor = True
        # Abajo
        if Y-1 >= 0:
            Mundo[Y-1][X].Vacio = False
            if Mundo[Y][X].Agujero:
                Mundo[Y-1][X].Brisa = True
            else: 
                Mundo[Y-1][X].Olor = True
        # Derecha
        if X+1 <= 3:
            Mundo[Y][X+1].Vacio = False
            if Mundo[Y][X].Agujero:
                Mundo[Y][X+1].Brisa = True
            else: 
                Mundo[Y][X+1].Olor = True
        # Izquierda
        if X-1 >= 0:
            Mundo[Y][X-1].Vacio = False
            if Mundo[Y][X].Agujero:
                Mundo[Y][X-1].Brisa = True
            else: 
                Mundo[Y][X-1].Olor = True
        return Mundo
    


