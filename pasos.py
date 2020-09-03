from numpy.random import randint
from math import ceil
from operaciones import checkChoosing, keepGoing, chooseNext, processCajas, addToCajas

class Pasos:
    def __init__(self, Cajas, Eligiendo, cajasAbiertas, minP, maxP, maxClientes,TiempoPaso, TiemposPromedio, ultimo):
        # INPUT
        self.cajas = Cajas
        self.eligiendo = Eligiendo
        self.minP = minP
        self.maxP = maxP
        self.maxClientes = maxClientes
        self.tPaso = TiempoPaso
        self.Telegir, self.Tprocess , self.Tpagar = TiemposPromedio
        self.cajasAbiertas = cajasAbiertas
        self.ultimo = ultimo
    
    #           OUTPUT
        self.clientesDespachados = 0
        self.productosDespachados = 0
        self.clientesEnEspera = 0
        self.maxCola = 0



    def sim(self):
        #paso 1: generar Clientes
        self.entran = 0
        if self.maxClientes > 0:
            if self.ultimo:
                self.entran = self.maxClientes
            else:
                self.entran = randint(0, self.maxClientes)

            rands = [[i*self.Telegir,0] for i in randint(self.minP, self.maxP + 1, size = self.entran)] #randint => [1,2,3,...] ====> [[1*Telegir,0],[2*Telegir,0],[3*Telegir,0] ]
            self.eligiendo += rands 
        
        #paso 2: dividir Clientes
        self.pasan, self.eligiendo = checkChoosing(self.eligiendo, self.tPaso)

        #paso 3: ver si podemos agregar clientes a las colas o hacer que clientes paguen
        while(keepGoing(self.cajas, self.pasan, self.tPaso)):
            bools = chooseNext(self.cajas, self.pasan)

            if True in bools:
                #procesamos las cajas
                antes = sum([len(i) for i in self.cajas])
                salen = processCajas(self.cajas, bools)
                despues = sum([len(i) for i in self.cajas])

                #sumas Clientes despachados
                self.clientesDespachados += len(salen)

                for i in salen:
                    self.productosDespachados += (i[0]-self.Tpagar)/self.Tprocess

                

                self.ajustarTiempos(max(salen, key = lambda x: x[0]-x[1]))
                
            else:
                #agregamos a cajas
                entra = self.pasan.pop(0)

                self.ajustarTiempos(entra)

                entra[0] = int(entra[0]/self.Telegir)*self.Tprocess + self.Tpagar
                entra[1] = 0

                addToCajas(self.cajas, entra, self.cajasAbiertas)
                #check MaxCola
                self.maxCola = max(self.maxCola, len(max(self.cajas, key=lambda x: len(x))))

        for i in self.cajas:
            if len(i) != 0:
                self.clientesEnEspera += len(i)

        return (self.cajas,
                self.eligiendo,
                self.entran, 
                self.clientesDespachados, 
                self.productosDespachados,
                self.clientesEnEspera,
                self.maxCola)

    def ajustarTiempos(self, cliente):
        self.tPaso -= max(0,(cliente[0] - cliente[1]))

        for i in self.cajas:
            if len(i) != 0:
                i[0][1] += (cliente[0] - cliente[1])

        if len(self.pasan) != 0:
            for i in self.pasan:
                i[1] += (cliente[0] - cliente[1])

if __name__ == '__main__':
    Paso = Pasos([[[300,0],[100,0]],[[40,0]],[],[],[]], [[2000,0],[300,0]], 5, 2, 10, 70, 1200, (30,10,45), False)
    Paso.sim()