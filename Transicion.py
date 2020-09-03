from pasos import Pasos
from operaciones import keepGoing, chooseNext, processCajas, addToCajas
import time

class Simulacion:
    def __init__(self, horasAtencion, cPasos, cEsperados, distClient, cajasAbiertas, minProd, maxProd, Telegir, Tprocess, Tpagar):
        self.tiempoXint = (horasAtencion//10)*3600
        self.cliXint = [ round(i*cEsperados /100) for i in distClient]

        self.cantPasos = cPasos
        self.cajasAbiertas = cajasAbiertas
        self.minProd = minProd
        self.maxProd = maxProd
        self.TiemposPromedio = (Telegir,Tprocess,Tpagar)

        self.currInt = 0
        self.cajas = []
        self.eligiendo = []
        self.last = True

        # cliIngresados, cliDespachados, prodsDespachados, cliEnEspera, maxCaja
        self.out = [[0 for j in range(5)] for i in range (10)]

    def checkCajas(self):
        if self.currInt == 0:
            self.cajas = [[] for i in range(self.cajasAbiertas[self.currInt])]
        else:
            temp = list(filter(lambda x: len(x) != 0, self.cajas))

            if len(temp) < self.cajasAbiertas[self.currInt]:
                self.cajas = [[] for i in range(self.cajasAbiertas[self.currInt] - len(temp))] + temp

            else:
                self.cajas = temp

    def inicio(self):
        clientesFaltantes = self.cliXint[self.currInt]

        self.checkCajas()
        for i in range(self.cantPasos):
            simPaso = Pasos(self.cajas, self.eligiendo, self.cajasAbiertas[self.currInt], self.minProd, self.maxProd, clientesFaltantes,self.tiempoXint/self.cantPasos,self.TiemposPromedio,i == self.cantPasos-1)
            resultados = simPaso.sim()

            self.cajas = resultados[0]
            self.eligiendo = resultados[1]
            clientesFaltantes = max(0,clientesFaltantes - resultados[2])

            for i in range(4):
                self.out[self.currInt][i] += resultados[i+2]

            self.out[self.currInt][4] = max(resultados[-1], self.out[self.currInt][4])


        if self.currInt != 9:
            self.currInt += 1

            self.inicio()
        else:

            while keepGoing(self.cajas, self.eligiendo, 10e6):
                bools = chooseNext(self.cajas, self.eligiendo)

                if True in bools:
                    salen = processCajas(self.cajas, bools)

                    self.out[9][1] += len(salen)
                else:
                    entra = self.eligiendo.pop(0)
    
                    entra[0] = entra[0]*self.TiemposPromedio[1] + self.TiemposPromedio[2]
                    entra[1] = 0

                    addToCajas(self.cajas, entra, len(self.cajas))

        if self.last:
            self.last = False
            for i in range(10):
                if self.out[i][1] != 0:
                    self.out[i][2] = self.out[i][2]//self.out[i][1]
                
                self.out[i][3] =  self.out[i][3]/self.cajasAbiertas[i]

        return self.out
        
def start():
    A = Simulacion(10,10,10,[10,10,10,10,10,10,10,10,10,10],[5,5,5,10,10,10,15,15,10,10],2,60,30,5,45)

    inC = outC = 0

    for i in A.inicio():
        print(i)
        inC += i[0]
        outC += i[1]

    print(inC," ",outC)

if __name__ == '__main__':
    start = time.time()
    A = Simulacion(10,200,20000,[10,10,10,10,10,10,10,10,10,10],[5,5,5,10,10,10,15,15,10,10],2,60,30,5,45)
    inC = outC = 0

    for i in A.inicio():
        print(i)
        inC += i[0]
        outC += i[1]

    print(inC," ",outC)
    end = time.time()
    print(end - start )