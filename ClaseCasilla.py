class Casilla:

    def __init__(self):
        self.Wumpus = False
        self.Olor = False
        self.Brisa = False
        self.Tesoro = False
        self.Vacio = True
        self.Agujero = False

    def ImpAtributos(self):
        Atributos = '-- '
        if self.Wumpus: 
            Atributos += 'W'
        if self.Olor:
            Atributos += 'O'
        if self.Brisa:
            Atributos += 'B'
        if self.Tesoro:
            Atributos += 'T'
        if self.Vacio: 
            Atributos += 'V'
        if self.Agujero:
            Atributos += 'A'
        Atributos += ' --'
        return Atributos

                
