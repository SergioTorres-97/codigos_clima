import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta

tributarios_HEC_HMS=r'C:\Users\sergi\Desktop\tributarios_rio_ejemplo.xls'
#Se crea una función que ordene los tributarios provenientes de HEC-HMS
def ordenar_tributarios(ruta_tributarios_HEC_HMS):
    tributarios=pd.read_excel(ruta_tributarios_HEC_HMS) #Se lee el archivo de HEC-HMS
    fecha=tributarios['Unnamed: 1']  #Se extrae la columna donde se encuentran las fechas
    fecha=fecha[6:]+ timedelta(days=1) #Se le suma un dia a la fecha original, debido al formato con el que sale de HEC-HMS (01/01/1995 24:00 = 02/02/1995)
    caudales=tributarios.drop(['A','Unnamed: 1'],axis=1) #Al dataframe original se le remueven las columnas A y Unnamed
    caudales.columns=caudales.iloc[0]  #Se genera un vector que contenga el nombre de los juntions y se asignan como cabeceras
    caudales=caudales[6:] #se eliminan las filas innecesarias
    caudales['Fecha']=fecha #Se agrega el vector de fechas previamente creado al nuevo dataframe
    caudales.set_index('Fecha',inplace=True)  #Se indexa la fecha
    return caudales
#Se crea una función que calcule el caudal afluente a cada sección teniendo en cuenta las microcuencas aferentes a la sección y definidas con anterioridad
def caudal_tributario(caudal_tributario,afluentes):
    caudal=[]
    for fila in range(0,caudal_tributario.shape[0]):
        a=np.sum(caudal_tributario[afluentes].iloc[fila]) #Se suman horizontalmente las columnas (una o mas) para hallar el caudal en la sección
        caudal.append(a)
    return caudal

junction=['J804','Q. EL TOTUMO A.D.','J786','J798','RIO CHICAMOCHA ALTO','LAGO SOCHAGOTA','PTAR',
          'Q. HONDA-LAGO SOCHA?','Q. SECA','ITP','Q. EL ORTIGAL','Q. TOIBITA A.D.','Q. CHORROBLANCO','RIO CHICAMOCHA ALTO 4'] #Aferentes rio chicamocha
Estaciones=[10950,10500,10350,9600,9300,6750,6600,6450,6300,4050,3750,2850,150] #Ejemplo rio chicamocha
caudal_trib=ordenar_tributarios(tributarios_HEC_HMS) #Se ordenan los tributarios

#Se aplica la funcion caudal_tributario a cada sección, teniendo en cuenta los afluentes respectivos (Ej: lago)
est_10950=[0 for i in range(0,len(caudal_trib))] #La primera sección no recibe afluentes
est_10500=caudal_tributario(caudal_trib,[junction[1]])
est_10350=caudal_tributario(caudal_trib,[junction[2]])
est_9600=caudal_tributario(caudal_trib,[junction[3]])
est_9300=caudal_tributario(caudal_trib,[junction[4]])
est_6750=caudal_tributario(caudal_trib,[junction[5]])
est_6600=caudal_tributario(caudal_trib,[junction[6]])
est_6450=caudal_tributario(caudal_trib,[junction[7]])
est_6300=caudal_tributario(caudal_trib,[junction[8]])
est_4050=caudal_tributario(caudal_trib,[junction[9]])
est_3750=caudal_tributario(caudal_trib,[junction[10],junction[11],junction[12]])
est_2850=caudal_tributario(caudal_trib,[junction[13]])
est_150=[0 for i in range(0,len(caudal_trib))] #La última sección no recibe afluentes

#Se concatenan las listas en una sola
tributarios=[est_10950,est_10500,est_10350,est_9600,est_9300,est_6750,
             est_6600,est_6450,est_6300,est_4050,est_3750,est_2850,est_150]
#Se transpone la lista para que quede una matriz de 365 x 12
tributarios=list(map(list, zip(*tributarios)))

#Como resultado se obtienen los caudales tributarios

# Definición de la expresión para el cálculo de la salinidad en unidades de Kg/m3 a partir de la conductividad a 25ºc
def salinidad(conductividad, temperatura):
    C_KCL = 4.2914  # conductividad de la solución de referencia a 15ºC (S/m) Unesco,1981
    Tc = 15  # Temperatura de la solución standard ºC
    C_KCL25 = (C_KCL * 10000) / (1 + (0.0191 * (
                Tc - 25)))  # se expresa la conductividad de la solución de referencia a 25ºC, empleando una aproximación asumiendo que no existe una temperatura interna de compensación en la celda de medición
    # 10000 para hacer la conversión de S/m a microohms/cm
    a0 = 0.0080
    a1 = -0.1692
    a2 = 25.3851
    a3 = 14.0941
    a4 = -7.0261
    a5 = 2.7081
    b0 = 0.0005
    b1 = -0.0056
    b2 = -0.0066
    b3 = -0.0375
    b4 = 0.0636
    b5 = -0.0144
    # Cálculo de la conductividad a 25ºC
    XT = temperatura - 15
    RT35 = (((1.0031E-9 * XT - 6.9698E-7) * XT + 1.104259E-4) * XT + 2.00564E-2) * XT + 0.6766097

    if (temperatura == 25).any():  # El .any() permite emplear series temporales
        C_25 = conductividad * 1000  # corresponde al factor de conversión de la conductividad expresada en mS/cm o dS/m a microohms/cm
    else:
        C_25 = 1000 * conductividad / (1 + 0.0191 * (
                    temperatura - 25))  # corresponde al factor de conversión de la conductividad expresada en mS/cm o dS/m a microohms/cm
    # Relación de conductividades ajustes por efecto de temperatura y cálculo de
    # la salinidad
    # Para salinidades entre 0 y 40 ups
    Rt = C_25 / C_KCL25
    X = 400 * Rt
    Y = 100 * Rt
    f = XT / (1 + 0.0162 * XT)
    deltaS = (f) * (b0 + b1 * Rt ** (1 / 2) + b2 * Rt + b3 * Rt ** (3 / 2) + b4 * Rt ** 2 + b5 * Rt ** (5 / 2))
    S = a0 + a1 * Rt ** (1 / 2) + a2 * Rt + a3 * Rt ** (3 / 2) + a4 * Rt ** 2 + a5 * Rt ** (5 / 2) + deltaS
    salinidad = S - (a0 / (1 + 1.5 * X + X ** 2)) - b0 * f / (1 + Y ** (1 / 2) + Y ** (3 / 2))

    return salinidad  # Salinidad en kg/m3

#Se llaman el archivo que contiene la conductividad y la temperatura de los afluentes
calidad=r'C:\Users\sergi\Desktop\Calidad_rio.xlsx'
conductividad=pd.read_excel(calidad,header=0,index_col='Fecha',sheet_name='Conductividad')
temperatura=pd.read_excel(calidad,header=0,index_col='Fecha',sheet_name='Temperatura')

print(conductividad.columns)
salinidad_afl=[]
for estacion in range(0,len(Estaciones)):
    a=list(salinidad(conductividad[Estaciones[estacion]],temperatura[Estaciones[estacion]]))
    salinidad_afl.append(a)
salinidad_afl=list(map(list, zip(*salinidad_afl)))
print(len(salinidad_afl))
