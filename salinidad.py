import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
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

def Balance(Co,Cf,Qo,Qf):
    carga=((Qo*Co)+(Qf*Cf))
    caudal=(Qo+Qf)
    concentracion=carga/caudal
    return concentracion,caudal

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
    return caudales,fecha
#Se crea una función que calcule el caudal afluente a cada sección teniendo en cuenta las microcuencas aferentes a la sección y definidas con anterioridad
def caudal_tributario(caudal_tributario,afluentes):
    caudal=[]
    for fila in range(0,caudal_tributario.shape[0]):
        a=np.sum(caudal_tributario[afluentes].iloc[fila]) #Se suman horizontalmente las columnas (una o mas) para hallar el caudal en la sección
        caudal.append(a)
    return caudal

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

def potencial_de_salinidad(salinidades,salinidad_geogenica):
    pot_sal=[]
    for dia in range(0,len(salinidades)):
        n=[]
        for elemento in range(0,len(salinidades[0])):
            a=((salinidades[dia][elemento]-salinidad_geogenica)/salinidad_geogenica)*100
            n.append(a)
        pot_sal.append(n)
    return pot_sal

def convertir_dataframe(vector,fecha,estaciones):
    df=pd.DataFrame(vector)
    if len(vector[0]) != len(estaciones):
        estaciones=estaciones[1:]
    df.columns = estaciones
    df['Fecha']=np.array(fecha)
    df.set_index('Fecha',inplace=True)
    return df

#########################################################################################################################################################
print(datetime.now())
# Se importan los archivos
secciones=r'C:\Users\sergi\Desktop\Archivos_prueba\SECCIONES.xlsx' #Archivo de secciones a entrenar
ruta_HEC_RAS_nivel=r'C:\Users\sergi\Desktop\Archivos_prueba\salida_nivel_rio.xls' #Archivo de niveles (salida HEC-RAS)
ruta_HEC_RAS_caudal=r'C:\Users\sergi\Desktop\Archivos_prueba\salida_caudal.xls' #Archivo de caudal (salida HEC-RAS)
tributarios_HEC_HMS=r'C:\Users\sergi\Desktop\Archivos_prueba\tributarios_rio_ejemplo.xls' #Tributarios de HEC-HMS (salida HEC-HMS)
calidad=r'C:\Users\sergi\Desktop\Archivos_prueba\Calidad_rio.xlsx' #Se llaman el archivo que contiene la conductividad y la temperatura de los afluentes (Gestión y archivos provenientes de dársenas y lago)
Estaciones=[10950, 10500, 10350, 9600, 9300,7050,6750, 6600, 6450, 6300,4350 ,4050, 3750, 2850, 150] #Estaciones dentro del río (Río Chicamocha)
cotas_menores=[2492.4,2489.55,2487.8,2487.8,2487.4,2485.2,2484.8,2485.2,2485.4,2485.2,2484.6,2484,2483.6,2484.31,2482.6] #Cotas menores río Chicamocha
junction=['J804','Q. EL TOTUMO A.D.','J786','J798','RIO CHICAMOCHA ALTO','LAGO SOCHAGOTA','PTAR',
          'Q. HONDA-LAGO SOCHA?','Q. SECA','ITP','Q. EL ORTIGAL','Q. TOIBITA A.D.','Q. CHORROBLANCO','RIO CHICAMOCHA ALTO 4'] #Aferentes rio chicamocha

caudal=ordenar_datos(ruta_HEC_RAS_caudal,Estaciones) #Se llama la función para ordenar caudales
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

#Calculo información de tributarios
caudal_trib=ordenar_tributarios(tributarios_HEC_HMS)[0] #Se ordenan los tributarios
fecha=ordenar_tributarios(tributarios_HEC_HMS)[1]
#Se aplica la funcion caudal_tributario a cada sección, teniendo en cuenta los afluentes respectivos (Ej: lago)
est_10950=[0 for i in range(0,len(caudal_trib))] #La primera sección no recibe afluentes
est_10500=caudal_tributario(caudal_trib,[junction[1]])
est_10350=caudal_tributario(caudal_trib,[junction[2]])
est_9600=caudal_tributario(caudal_trib,[junction[3]])
est_9300=caudal_tributario(caudal_trib,[junction[4]])
est_7050=[0 for i in range(0,len(caudal_trib))] #La primera sección no recibe afluentes
est_6750=caudal_tributario(caudal_trib,[junction[5]])
est_6600=caudal_tributario(caudal_trib,[junction[6]])
est_6450=caudal_tributario(caudal_trib,[junction[7]])
est_6300=caudal_tributario(caudal_trib,[junction[8]])
est_4350=[0 for i in range(0,len(caudal_trib))] #La primera sección no recibe afluentes
est_4050=caudal_tributario(caudal_trib,[junction[9]])
est_3750=caudal_tributario(caudal_trib,[junction[10],junction[11],junction[12]])
est_2850=caudal_tributario(caudal_trib,[junction[13]])
est_150=[0 for i in range(0,len(caudal_trib))] #La última sección no recibe afluentes

#Se concatenan las listas en una sola
tributarios=[est_10950,est_10500,est_10350,est_9600,est_9300,est_7050,est_6750,
             est_6600,est_6450,est_6300,est_4350,est_4050,est_3750,est_2850,est_150]
#Se transpone la lista para que quede una matriz de 365 x 12
tributarios=list(map(list, zip(*tributarios)))

#Se separa la conductividad y la temperatura en dos dataframes
conductividad=pd.read_excel(calidad,header=0,index_col='Fecha',sheet_name='Conductividad')
temperatura=pd.read_excel(calidad,header=0,index_col='Fecha',sheet_name='Temperatura')

salinidad_afl=[]
for estacion in range(0,len(Estaciones)):
    a=list(salinidad(conductividad[Estaciones[estacion]],temperatura[Estaciones[estacion]]))
    salinidad_afl.append(a)
salinidad_afl=list(map(list, zip(*salinidad_afl)))

lago=[99999 for i in range(0,365)] #serie de salinidades del lago
darsena2=[99999 for i in range(0,365)] #serie de salinidades del lago
for i in range(0,len(salinidad_afl)):
    salinidad_afl[i][6]=lago[i] #Lago
    salinidad_afl[i][11] = darsena2[i] #Dársena 2

print(salinidad_afl)



#Calculo para un año (ej:2011)
Caudales=caudal
areas=areas_secciones  #Areas secciones primer dia
velocidades=velocidad #Velocidades secciones primer dia
Afluentes=tributarios #Afluentes a los tramos dia 1
Concentraciones=salinidad_afl #Concentraciones afuentes a los tramos dia 1

conc=[]
for dia in range(0,len(Caudales)):
    Concentracion_inicial = 10
    area = areas[dia][0]
    U = velocidades[dia][0]
    Co = Concentracion_inicial  # Concentracion en la entrada
    d=[]
    a=[]
    for tributario in range(0,len(Estaciones)):
        if tributario==len(Estaciones)-1:
            break
        E=0.5
        X=Estaciones[tributario]-Estaciones[tributario+1]
        #Balance para lanzar el trazador
        dist=Estaciones[0]-Estaciones[tributario+1]
        Cf=Concentraciones[dia][tributario] #primer tributario para inicializar
        Qo=Caudales[dia][tributario] #Caudal de entrada
        Qf=Afluentes[dia][tributario] #primer tributario para inicializar

        #Se calcula la masa para el primer lanzamiento
        Ct=Balance(Co,Cf,Qo,Qf)[0] #Se extrae la concentracion remanente en el tramo
        M=Ct*area/U
        t0=X/U
        c = ((M/areas[dia][tributario])/((4*np.pi*E*t0)**0.5))*np.exp(-(((X-(U*t0))**2)/(4*E*t0)))
        a.append(c)

        #Se iniciliza las nuevas condiciones para el siguiente tramo
        area = areas[dia][tributario]
        U = velocidades[dia][tributario]
        Co=c
        d.append(dist)

    conc.append((a))

pot_sal=potencial_de_salinidad(conc,2.65)
print(convertir_dataframe(nivel,fecha,Estaciones))
print(datetime.now())

# for i in range(0,15):
#     plt.figure(figsize=(15,6))
#     plt.scatter(d,conc[i],color='white',edgecolors='black',s=20)
#     plt.grid(linestyle='--',linewidth ='0.5')
#     plt.xticks(size='medium',color ='k',rotation=45,**{'fontname':'calibri'})
#     plt.yticks(size='medium',color ='k',rotation=0,**{'fontname':'calibri'})
#     plt.xlabel('Distancia (m)',fontsize=12,**{'fontname':'calibri'})
#     plt.ylabel('Concentración (mg/l)',fontsize=12,**{'fontname':'calibri'})
#     plt.show()

