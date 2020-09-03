from flask import Flask, render_template, redirect, url_for, request,flash
import timeit
import json
import ast
import time
from Transicion import *
app = Flask(__name__, template_folder="Templates")

#Renderiza la planilla index
@app.route("/")
def Index():
    return render_template('index.html')

#Renderiza la planilla input
@app.route("/input")
def input():
    return render_template('input.html')

#Renderiza la planilla output
@app.route("/output")
def output():
    return render_template('output.html')

#Recibe los datos ingresados en "input.html" y genera una simulcion:
#Si el nombre existe en el cache, renderiza "edit.html" con los datos ingresados en resultados[] y un mensaje de alerta.
#Si el nombre nno exite en el cache, renderiza "output.html" con los datos ingresados en resultados[] y los datos de la simulacion en simulacion[].
@app.route("/simular", methods = ['POST'])
def simular():
    if request.method == 'POST':
        
        nombre = str(request.form['nombre'])

        horasDiarias = int(request.form['horasDiarias'])

        nPasos= int(request.form['nPasos'])

        nClient = int(request.form['nClient'])

        distribucion1 = int(request.form['distribucion1'])
        distribucion2 = int(request.form['distribucion2'])
        distribucion3 = int(request.form['distribucion3'])
        distribucion4 = int (request.form['distribucion4'])
        distribucion5 = int (request.form['distribucion5'])
        distribucion6 = int (request.form['distribucion6'])
        distribucion7 = int (request.form['distribucion7'])
        distribucion8 = int (request.form['distribucion8'])
        distribucion9 =int (request.form['distribucion9'])
        distribucion10 = int (request.form['distribucion10'])
        
        distribuciones=[distribucion1, distribucion2, distribucion3, distribucion4, distribucion5, distribucion6, distribucion7, distribucion8, distribucion9, distribucion10]

        caja1 = int (request.form['caja1'])
        caja2 = int (request.form['caja2'])
        caja3 = int (request.form['caja3'])
        caja4 = int (request.form['caja4'])
        caja5 = int (request.form['caja5'])
        caja6 = int (request.form['caja6'])
        caja7 = int(request.form['caja7'])
        caja8 = int(request.form['caja8'])
        caja9 = int(request.form['caja9'])
        caja10 = int(request.form['caja10'])
        
        cajas = [caja1, caja2, caja3, caja4, caja5, caja6, caja7, caja8, caja9, caja10 ]

        cantMin = int (request.form['cantMin'])
        
        cantMax = int (request.form['cantMax'])
        
        tSelect = int(request.form['tSelect'])
        
        tDesp = int(request.form['tDesp'])
        
        tPago = int(request.form['tPago'])
        
        resultados = [nombre, horasDiarias, nPasos, nClient, distribuciones, cajas, cantMin, cantMax, tSelect, tDesp, tPago]
        

        ############################
        #AQUI SE HACE LA SIMULACION#
        ############################

        simulacion = Simulacion(horasDiarias, nPasos, nClient, distribuciones, cajas, cantMin, cantMax, tSelect, tDesp, tPago)

        start = time.time()
        resultsA = simulacion.inicio()
        end= time.time()

        minutosSim = (end - start)/60

        resultsSim = [minutosSim, resultsA[0], resultsA[1], resultsA[2], resultsA[3], resultsA[4], resultsA[5], resultsA[6], resultsA[7], resultsA[8], resultsA[9]]

        ############################
        ####FINAL DE SIMULACION#####
        ############################


        with open ('data.json') as file: 
            data = json.load(file)
            for client in data['cache']:
                if str(nombre) == client['nombre']:
                    alerta = "[ERROR] Nombre de la simulacion ya existente, intente otro"
                    return render_template('edit.html', alerta = alerta, resultados = resultados)
         
        return render_template('output.html', resultados = resultados, resultsSim = resultsSim)

#Renderiza "edit.html" con los datos de un "j.son" segun un "nombre", si los datos son correctos se simulan los datos con "simular()"
@app.route("/reInput", methods=['POST'])
def reInput():

    if request.method == 'POST':
        
        nombre = request.form['nombre']

        with open('data.json') as file:
            data = json.load(file)
            for client in data['cache']:
                if client['nombre'] == nombre:

                    nom = client['nombre'] 
                    n_clientes= int(client['numero de clientes'])
                    h_diarias = int(client['horas diarias'])
                    n_pasos = int(client['numero de pasos'])
                    distri = client['distribucion por intervalos']
                    cajas = client['cajas por intervalo']
                    cant_min_prod =  int(client['cantidad minima de productos'])
                    cant_max_prod = int(client['cantidad maxima de productos'])
                    t_selec = int(client['tiempo de seleccion'])
                    t_despacho = int(client['tiempo de despacho'])
                    t_pago = int(client['tiempo de pago'])
                    resultados = [nom,h_diarias,n_pasos,n_clientes,distri,cajas,cant_min_prod, cant_max_prod, t_selec, t_despacho,t_pago]
                    
                    return render_template('edit.html', resultados = resultados)

#Guarda los resultados en  "edit.json" y redirecciona a "index.html"
@app.route("/guardar", methods = ['POST'])
def guardar():
    if  request.method == 'POST':

        nombre = str(request.form['nombre'])
        horasDiarias = int(request.form['horasDiarias'])
        nPasos= int(request.form['nPasos'])
        nClient = int(request.form['nClient'])
        distribuciones = ast.literal_eval(request.form['distribuciones'])
        cajas = ast.literal_eval(request.form['cajas'])
        cantMin = int(request.form['cantMin'])
        cantMax = int(request.form['cantMax'])
        tSelect = int(request.form['tSelect'])
        tDesp = int(request.form['tDesp'])
        tPago = int(request.form['tPago'])

        with open ('data.json') as f:
            var = json.load(f)
            var['cache'].append({
                'nombre':nombre,
                'horas diarias':horasDiarias,
                'numero de pasos':nPasos,
                'numero de clientes':nClient,
                'distribucion por intervalos':distribuciones,
                'cajas por intervalo':cajas,
                'cantidad minima de productos':cantMin,
                'cantidad maxima de productos':cantMax,
                'tiempo de seleccion': tSelect,
                'tiempo de despacho': tDesp,
                'tiempo de pago': tPago
        })

        with open ('data.json', 'w') as fi: 
            json.dump(var, fi,indent=11)

        #datos[POST]
        segundosSim = int(request.form['minutosSim'])
        minutosSim = segundosSim
        sim1  = ast.literal_eval(request.form['sim1'])
        sim2  = ast.literal_eval(request.form['sim2'])
        sim3  = ast.literal_eval(request.form['sim3'])
        sim4  = ast.literal_eval(request.form['sim4'])
        sim5  = ast.literal_eval(request.form['sim5'])
        sim6  = ast.literal_eval(request.form['sim6'])
        sim7  = ast.literal_eval(request.form['sim7'])
        sim8  = ast.literal_eval(request.form['sim8'])
        sim9  = ast.literal_eval(request.form['sim9'])
        sim10 = ast.literal_eval(request.form['sim10'])

        with open ('data_sim.json') as f:
            var = json.load(f)
            var['cache_sim'].append({
                'nombre':nombre,
                'horas diarias':minutosSim,
                'sim1':sim1, 
                'sim2':sim2,
                'sim3':sim3,
                'sim4':sim4,
                'sim5':sim5,
                'sim6':sim6,
                'sim7':sim7,
                'sim8':sim8,
                'sim9':sim9,
                'sim10':sim10
        })

        with open ('data_sim.json', 'w') as fi: 
            json.dump(var, fi,indent=12)

    return redirect(url_for('Index'))

#Reanderiza "memoria.html" con todos los datos de "data.json" en el arreglo "data[]""
@app.route("/memoria")
def memoria():
    with open('data.json') as file:
        #aca los carga a una variable 'data'
        data = json.load(file)
    return render_template('memoria.html', data = data)

@app.route("/memoriasim/<string:nombre>")
def memoriasim(nombre):

    totalDatos = []

    with open ('data_sim.json') as file: 
        data_sim = json.load(file)
        for client in data_sim['cache_sim']:
            if nombre == client['nombre']:
                minutosSim = client['horas diarias']
                sim1 = client['sim1']
                sim2 = client['sim2']
                sim3 = client['sim3']
                sim4 = client['sim4']
                sim5 = client['sim5']
                sim6 = client['sim6']
                sim7 = client['sim7']
                sim8 = client['sim8']
                sim9 = client['sim9']
                sim10 = client['sim10']

                dato = [minutosSim, sim1, sim2, sim3, sim4, sim5, sim6, sim7, sim8, sim9, sim10]
                totalDatos.append(dato)

    return render_template('memoriasim.html', totalDatos = totalDatos)





if __name__ == "__main__":
    app.run(port=3000, debug = True) 
