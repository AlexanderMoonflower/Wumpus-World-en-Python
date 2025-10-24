from Mundo import mundo 
from Agente import Agente

M1 = mundo()
MapaJuego = M1.generar_mundo()

print("Mapa de juego, Generado aleatoriamente: ")
for i in range(4): 
    for j in range(4):
        print(f"{M1.mapa[i][j].ImpAtributos()}X{j}Y{i}" , end = '') 
    print()
A1 = Agente(MapaJuego) 

## Iniciar Juego
A1.Descubrir(A1.PosicionInicial)
while A1.Vivo and A1.Presente:
    A1.ElegirCamino()