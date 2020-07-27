import numpy as np
import pandas as pd
import openpyxl
import xlrd
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt

def ordenar_datos(ruta_HEC_RAS,Estaciones):
    salida = pd.read_excel(ruta_HEC_RAS, header=2)
    # Se redondea la columna estación para facilitar el filtro
    salida['STATION'] = round(salida['STATION'])
    # Se crea una lista que contenga las estaciones a utilizar
    Estaciones = Estaciones
    # Se extrae el índice de las estaciones con base en el archivo original
    nrows = []
    for i in range(0, len(Estaciones)):
        a = salida.loc[(salida['STATION'] == Estaciones[i])].index[0] + 3
        nrows.append(a)  # Se crea una lista que contenga la fila en la cual se encuentra cada estacion
    # Se utiliza la librería Xlrd para iterar por cada una de las hojas
    datos = xlrd.open_workbook(ruta_HEC_RAS)  # Se abre el archivo nuevamente con la nueva libreria

    # Se itera buscando la información de cada una de las secciones para todos los días
    datos_salida = []
    for dia in range(0, len(datos.sheet_names())):
        c = []  # Lista vacia que se limpia cada vez que se calcule un día
        for i in range(0, len(Estaciones)):
            a = datos.sheet_by_index(dia).cell(nrows[i],2).value  # Con la lista de filas halladas previamente, se busca la celda especificamente
            c.append(a)
        datos_salida.append(c)

    # Se itera buscando la fecha presente en cada hoja
    fecha = []
    for dia in range(0, len(datos.sheet_names())):
        a = datos.sheet_by_index(dia).cell(0, 2).value  # la celda 0,2 es donde se encuentra la fecha en las hojas
        a = a[0:2] + '/' + a[2:5] + '/' + a[5:9]  # Se extrae la cadena de caracteres de la fecha ddmmmyyyy -02apr2010
        datetime_ = str(a)  # Se convierte a cadena
        n = datetime.strptime(datetime_, '%d/%b/%Y')  # Se pasa a un formato fecha que sea aceptado por Python
        fecha.append(n)

    Salidas = pd.DataFrame(datos_salida)  # Se crea un dataframe que contenga los caudales
    Salidas.columns = Estaciones  # Se renombran las columnas con el nombre de las estaciones
    Salidas['Fecha'] = fecha  # Se agrega una nueva columna que contenga las fechas previamente extraidas
    Salidas = Salidas.sort_values(by='Fecha')  # Se ordenan las fechas
    Salidas.set_index('Fecha', inplace=True)  # Se deja como indice el vector de fechas
    Salidas_array=np.array(Salidas) #Se deja en formato de vectores

    return Salidas_array

#Se calcula el área de la sección en función del nivel, se busca obtener una funcion para cada seccion de estudio
def calculo_de_areas(ruta_secciones,Estaciones):
    par1=[]
    par2=[]
    for i in range(0,len(Estaciones)):
        areas = pd.read_excel(ruta_secciones, header=0,sheet_name=str(Estaciones[i]))
        x = np.array(areas[areas.columns[0]])
        y = np.array(areas[areas.columns[1]])
        modelo=np.polyfit(np.log(x),y,1)
        P1=modelo[0]
        P2=modelo[1]
        par1.append(P1) #Parametro a de la forma a*log(x)+b
        par2.append(P2) #Parametro b de la forma a*log(x)+b
    return par1,par2

# funcion anonima para calcular las diferentes areas
areas=lambda par1,par2,nivel:(par1*np.log(nivel) + par2)
# funcion anonima para calcular la velocidad mediante los parametros de caudal y area
velocidad_seccion=lambda caudal,area : (caudal/area)

def trazador(Estaciones,velocidades,Areas,tf=3200,dt=10000,M=10000,E=2.04):
    X=[Estaciones[0]-Estaciones[1],Estaciones[0]-Estaciones[2]]
    U=velocidades
    A=Areas #Vector de n filas x n columnas, donde las filas representan los dias y las columnas las estaciones
    traz=[]
    for estacion in range(0,len(X)):
        a=[]
        for dia in range(0,len(A)):
            vel=U[dia][estacion+1]
            Are = A[dia][estacion + 1]
            t=X[estacion]/vel
            c=((M/Are)/((4*np.pi*E*t)**0.5))*np.exp(-(((X[estacion]-(vel*t))**2)/(4*E*t)))
        # if estacion==len(X):
        #     break
            a.append(c)
        traz.append(a)
    traz=np.array(traz).T
    return traz

def potencial_de_renovacion(concentraciones):
    pr=[]
    for i in range(0,len(concentraciones)):
        a=(concentraciones[i][0]-concentraciones[i][1])/concentraciones[i][0]
        pr.append(a)
    return pr
###########################################################################################
secciones=r'C:\Users\sergi\Desktop\SECCIONES.xlsx' #Archivo de secciones a entrenar
ruta_HEC_RAS_nivel=r'C:\Users\sergi\Desktop\salida_nivel_rio.xls' #Archivo de niveles (salida HEC-RAS)
ruta_HEC_RAS_caudal=r'C:\Users\sergi\Desktop\salida_caudal.xls' #Archivo de caudal (salida HEC-RAS)
tributarios_HEC_HMS=r'C:\Users\sergi\Desktop\tributarios_rio_ejemplo.xls' #Tributarios de HEC-HMS (salida HEC-HMS)
calidad=r'C:\Users\sergi\Desktop\Calidad_rio.xlsx' #Se llaman el archivo que contiene la conductividad y la temperatura de los afluentes (Gestión y archivos provenientes de dársenas y lago)
Estaciones=[10950, 10500, 6750] #Estaciones dentro del río (Río Chicamocha)

caudal=caudales=ordenar_datos(ruta_HEC_RAS_caudal,Estaciones) #Se llama la función para ordenar caudales
nivel=ordenar_datos(ruta_HEC_RAS_nivel,Estaciones) #Se llama la función para ordenar niveles
par1,par2=calculo_de_areas(secciones,Estaciones) #Se calculan los parametros de las ecuaciones para el calculo de las áreas

#Se calculan las areas en funcion de los niveles, teniendo en cuenta las relaciones existentes entre ellos para cada seccion
areas_secciones=[]
b=[]
for dia in range(0,len(nivel)):
    b=[]
    for i in range(0,len(Estaciones)):
        a=round(areas(par1[i], par2[i], nivel[dia][i]),2) #Se calculan las area por estacion en los diferentes dias
        b.append(a)
    areas_secciones.append(b)
areas_secciones=np.array(areas_secciones) #Vector de estaciones que contiene las áreas

velocidad=velocidad_seccion(caudal,areas_secciones) #Se calcula la velocidad por sección y por día teniendo en cuenta el caudal y el área
concentracion=trazador(Estaciones,velocidad,areas_secciones)
pot_rev=potencial_de_renovacion(concentracion)
plt.plot(pot_rev)
plt.show()
print(concentracion)
