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
    Salidas_array=np.array(Salidas).T #Se deja en formato de vectores donde cada vector es un estacion con n dias

    return Salidas_array

#Función para extraer el calado de cada sección, en función de su cota menor
def calado(niveles,cota_menor):
    a=niveles-cota_menor
    return a
#Función para calcular potencial de déficit hídrico de cada sección
def deficit_hidrico(niveles,nivel_critico):
    a=((niveles-nivel_critico)/nivel_critico)*100
    return a


###Ejemplo río Chicamocha
ruta_HEC_RAS_nivel=r'C:\Users\sergi\Desktop\salida_nivel_quebrada.xls' #Archivo de niveles (salida HEC-RAS)
Estaciones=[10950,3450,150] #Secciones transversales
cotas_menores=[2492.4,2484,2482.60] #Cotas menores extraidas de HEC_RAS
nivel_critico=0.5 #Nivel crítico definido

Niveles=ordenar_datos(ruta_HEC_RAS_nivel,Estaciones) #Se extraen los niveles y se ordenan

#Se crea un ciclo para que extraiga el calado de cada estación simultaneamente
calado_est=[]
for i in range(0,len(cotas_menores)):
    a=calado(Niveles[i],cotas_menores[i])
    calado_est.append(a)
#Se crea un ciclo para que calcule el potencial en cada estación simultaneamente
pdh=[]
for i in range(0,len(Estaciones)):
    a=deficit_hidrico(calado_est[i],nivel_critico)
    pdh.append(a)

# plt.plot(pdh[1])
# plt.show()

