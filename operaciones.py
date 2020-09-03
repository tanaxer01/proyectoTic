#CHECKCHOOSING
#in: oint[], int | out: int[], int[]
def checkChoosing(elegidos, MaxTime):
    elegidos = sorted(elegidos, key= lambda x: x[0]-x[1]) #modificar ?
    div = 0
    
    for i in range(len(elegidos)):
        if(elegidos[i][0] - elegidos[i][1] <= MaxTime):
            elegidos[i][1] = 0
            div += 1
        else:
            elegidos[i][1] += MaxTime
    
    return elegidos[:div],elegidos[div:]

#KEEPGOINT?
#in: int[][], int[], int | out: Bool
def keepGoing(caja, pasanACaja, MaxTime):
    for i in caja:
        if len(i) != 0 and i[0][0] - i[0][1] <= MaxTime:
            return True
    if len(pasanACaja) !=0:
        return True
    return False

#CHOOSENEXT
#in: int[][], int[] | out: Bool[]
def chooseNext(caja, pasanACaja):
    # if len(pasanACaja) != 0:
    #     return([i[0][0] - i[0][1] <= pasanACaja[0][0]-pasanACaja[0][1] if len(i) != 0 else False for i in caja])
    # else:
    #     return([len(i) != 0 for i in caja])

    bools = [False for i in range(len(caja))]
    if len(pasanACaja) != 0:
        for i in range(len(caja)):
            if len(caja[i]) != 0:
                if caja[i][0][0]-caja[i][0][1] <= pasanACaja[0][0]-pasanACaja[0][1]:
                    bools[i] = True
    else:
        for i in range(len(caja)):
            if len(caja[i]) != 0:
                bools[i] = True

    return bools

        
#ADDTOCAJAS
#in: int[][], int , int | out: VOID
def addToCajas(caja, cliente, cajasAbiertas):
    caja = min(caja[:cajasAbiertas], key=lambda x: len(x)) #modificar ?
    caja.append(cliente)
   
#PROCESSCAJAS
#in: int[][], bool[] | out: int[]
def processCajas(caja, bools):
    outOfHere = []
    
    for i in range(len(bools)):
        if bools[i]:
            outOfHere.append(caja[i].pop(0))
            
    return outOfHere

def adjustTimes(Cajas,Pasan, Cliente, MaxTime):
    MaxTime -= Cliente[0]-Cliente[1]

    for i in Pasan:
      if len(i) != 0:
        i[1] += Cliente[0]-Cliente[1]
         
    for i in Cajas:
        if len(i) != 0:
            i[0][1] += Cliente[0]-Cliente[1]

    return Cajas, Pasan, MaxTime


def check(caja, cola):
    cuantos = 0
    for i in caja:
        cuantos += len(i)
    
    cuantos += len(cola)

    return cuantos
