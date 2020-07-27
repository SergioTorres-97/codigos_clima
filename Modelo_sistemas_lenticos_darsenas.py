import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import matplotlib.dates as mdates

# Definición de la expresión para el cálculo de la salinidad en unidades de Kg/m3 a
# partir de la conductividad a 25ºc
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

# Definición de la expresión para el cálculo de la salinidad en unidades de Kg/m3 a
# partir de la conductividad a 25ºc
def salinidad1(conductividad, temperatura):
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

    if temperatura == 25:  # El .any() permite emplear series temporales
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

def Ab1(x, a=1.391e+06, b=4192, c=6.023):
    # x= profundidad del agua en el algo con respecto a la cota de fondo en el lago (m)
    # Ley de áreas para el Lago (área en m^2) , ajuste mediante función
    # logística

    # Batimetría año 2015 Fuente: Corpoboyacá, Geospatial (2015)
    if (x <= 0):
        Ab = 0  # (en m^2)
    else:
        Ab = (a * b * 2.718281 ** (c * x)) / (a + b * (2.718281 ** (6.008 * x)) - 1)  # (en m^2)

    return Ab

def Area_dar1(x, a=271.88902077, b=-1925.40179148, c=5346.75787005,d=-7508.69710111,e=6639.38465588,f=-93.74337132):
    # x= profundidad del agua en el algo con respecto a la cota de fondo en el lago (m)
    # Ley de áreas para el Lago (área en m^2) , ajuste mediante función
    # logística

    # Batimetría año 2015 Fuente: Corpoboyacá, Geospatial (2015)
    if (x <= 0.0144):
        Ab = 0  # (en m^2)
    else:
        Ab = (a*(x**5))+(b*(x**4))+(c*(x**3))+(d*(x**2))+(e*(x))+f # (en m^2)
    return Ab

def Area_dar2(x, a=-1482.24872765, b=18167.68264678, c=-64707.50734129,d=97886.66908086,e=-19430.68615198 ,f=464.18587539):
    # x= profundidad del agua en el algo con respecto a la cota de fondo en el lago (m)
    # Ley de áreas para el Lago (área en m^2) , ajuste mediante función
    # logística

    # Batimetría año 2015 Fuente: Corpoboyacá, Geospatial (2015)
    if x<=0 and x<0.2:
        Ab = 0  # (en m^2)
    else:
        Ab = (a*(x**5))+(b*(x**4))+(c*(x**3))+(d*(x**2))+(e*(x))+f # (en m^2)
    return Ab

def compuerta(a, b, y2, cc=0.42, c1=0.0979):
    if a == 0:
        Qe1 = 0
    else:
        if y2 / a >= 2.451:
            cv = 1
        else:
            if a == 0:
                cv = 0.96
                v1 = 0
            else:
                cv = 0.96 + (c1 * a / y2)

        v1 = cv * ((2 * 9.81 * y2) ** 0.5) / ((1 + (cc * a / y2)) ** 0.5)
        cd = (cc * cv) / ((1 + (cc * a / y2)) ** 0.5)
        Qe1 = cd * ((2 * 9.81 * y2) ** 0.5) * a * b

    return (Qe1)

def Bombeo_darsena_1(hor_bom, potencia=234):
    caudal = hor_bom * potencia / 86400
    return caudal

# Generación de los niveles en función de los caudales afluentes
def Dinamica_darsena_1(No, prec, evap, dq_ant, hor_bom):
    """
    Parámetros
    ----------------------------------------------------------------------------------------------------------------------
    No=Nivel inicial del lago
    Cfl=Cota de fondo lago
    Cfc=Cota de fondo compuerta
    aper_com=régimen de apertura de compuerta
    prec=serie temporal de precipitacion [mm]
    evap=serie temporal de evaporacion [mm]
    dq=delta de caudales antrópicos [m3/s]
    q_hid=Serie de caudal hidrológico [m3/s]
    """
    Ao = Area_dar1(No, -747.6, 3195.9, 320.76)  # Se cálcula el área inicial
    Caudal_prec = []
    Caudal_evap = []
    delta_cau = []
    Alturas = []
    Areas_mod = []
    Caudal_salida = []
    for i in range(0, len(fecha)):
        if i == 0:
            Q_p = prec[i] / (86400 * 1000) * Ao  # Se calcula el caudal por precipitación en función del área inicial
            Q_e = evap[i] / (86400 * 1000) * Ao  # Se calcula el caudal por evaporación en función del área inicial
            bomb = Bombeo_darsena_1(hor_bom[i])
            dq = Q_p - Q_e - bomb + dq_ant[i]  # Se realiza el balance de masas
            Alt_m = (dq / Ao * 86400) + No  # Se calcula la áltura de la lámina de agua en función del caudal
            Are_m = Area_dar1(Alt_m, a=-747.6, b=3195.9, c=320.76)  # Se calcula la nueva área ocupada posterior al balance
        if i > 0:
            Q_p = prec[i] / (86400 * 1000) * Areas_mod[i - 1]
            Q_e = evap[i] / (86400 * 1000) * Areas_mod[i - 1]
            bomb = Bombeo_darsena_1(hor_bom[i])
            dq = Q_p - Q_e - bomb + dq_ant[i]
            Alt_m = (dq / Areas_mod[i - 1] * 86400) + Alturas[i - 1]
            Are_m = Area_dar1(Alt_m, a=-747.6, b=3195.9, c=320.76)
        print(Are_m,Alt_m)
        Caudal_prec.append(Q_p)  # lista de caudales por precipitación
        Caudal_evap.append(Q_e)  # lista de caudales por evaporación
        delta_cau.append(dq)  # lista de variación diaria de caudales
        Caudal_salida.append(bomb)  # Caudal de salida por la compuerta
        Alturas.append(Alt_m)  # Niveles del lago
        Areas_mod.append(Are_m)  # Area superficial del lago
    Alturas = np.array(Alturas)
    Caudal_salida = np.array(Caudal_salida)
    Areas_mod = np.array(Areas_mod)
    return Alturas, Caudal_salida, Areas_mod

# Generación de los niveles en función de los caudales afluentes
def Dinamica_Darsena2(No, Cfl, Cfc, prec, evap, dq_ant, cau_dar1, aper_com):
    # cambiar 1.12 de la compuerta
    """
    Parámetros
    ----------------------------------------------------------------------------------------------------------------------
    No=Nivel inicial del lago
    Cfl=Cota de fondo lago
    Cfc=Cota de fondo compuerta
    aper_com=régimen de apertura de compuerta
    prec=serie temporal de precipitacion [mm]
    evap=serie temporal de evaporacion [mm]
    dq=delta de caudales antrópicos [m3/s]
    q_hid=Serie de caudal hidrológico [m3/s]
    """
    y = Cfl - Cfc  # Cálcula la diferencia entre la cota inferior del lago y la cota inferior de la compuerta
    No_com = No - y - aper_com[0] * 2 / 100  # Cálcula la lámina de agua sobre la compuerta
    Ao = Area_dar2(No, 11444, 19653, -2692.7)  # Se cálcula el área inicial
    Nivel_com = []
    Caudal_prec = []
    Caudal_evap = []
    delta_cau = []
    Alturas = []
    Areas_mod = []
    Caudal_salida = []
    for i in range(0, len(fecha)):
        if i == 0:
            Q_p = prec[i] / (86400 * 1000) * Ao  # Se calcula el caudal por precipitación en función del área inicial
            Q_e = evap[i] / (86400 * 1000) * Ao  # Se calcula el caudal por evaporación en función del área inicial
            aper = compuerta(aper_com[i] * 0.02, 1.5, No_com)
            dq = Q_p - Q_e - aper + dq_ant[i] + cau_dar1[i]  # Se realiza el balance de masas
            Alt_m = (dq / Ao * 86400) + No  # Se calcula la áltura de la lámina de agua en función del caudal
            Are_m = Area_dar2(Alt_m, 11444, 19653, -2692.7)  # Se calcula la nueva área ocupada posterior al balance
            N_c = Alt_m - y + aper_com[i] * 0.02  # Se calcula la lámina de agua sobre la compuerta
        if i > 0:
            Q_p = prec[i] / (86400 * 1000) * Areas_mod[i - 1]
            Q_e = evap[i] / (86400 * 1000) * Areas_mod[i - 1]
            aper = compuerta(aper_com[i] * 0.02, 1.5, Nivel_com[i - 1])
            dq = Q_p - Q_e - aper + dq_ant[i] + cau_dar1[i]
            Alt_m = (dq / Areas_mod[i - 1] * 86400) + Alturas[i - 1]
            Are_m = Area_dar2(Alt_m, 11444, 19653, -2692.7)
            N_c = Alt_m - y + aper_com[i] * 0.02
        Nivel_com.append(N_c)
        Caudal_prec.append(Q_p)  # lista de caudales por precipitación
        Caudal_evap.append(Q_e)  # lista de caudales por evaporación
        delta_cau.append(dq)  # lista de variación diaria de caudales
        Caudal_salida.append(aper)  # Caudal de salida por la compuerta
        Alturas.append(Alt_m)  # Niveles del lago
        Areas_mod.append(Are_m)  # Area superficial del lago
    Alturas = np.array(Alturas)
    Caudal_salida = np.array(Caudal_salida)
    Areas_mod = np.array(Areas_mod)
    return Alturas, Caudal_salida, Areas_mod

def salinizacion(vol_sis, cargas_afluentes, caudales_efl, con_inicial, tem_inicial, con_geo=2.5,
                              tem_geo=21.2):
    """
    Parámetros
    ----------------------------------------------------------------------------------------------------------------------
    vol_sis=Serie temporal de volumen del sistema
    carga_salinidad=Serie temporal de carga total de salinidad aportante al sistema
    con_inicial=Conductividad inicial del sistema al t=0
    tem_inicial=Temperatura inicial del sistema al t=0
    """
    Sal=[]
    ps=[]
    Ci=salinidad1(con_inicial, tem_inicial)
    Co=Ci
    for i in range(0, 365):

        Mooas3=(Ci * vol_sis[i])+(cargas_afluentes[i])*86400
        Msaas=(caudales_efl[i]*Co)*86400
        Mtaas=Mooas3-Msaas

        if i>0:
            Co=Sal[i-1]
        if i<364:
            a=Mtaas/vol_sis[i+1]
        Sal.append(a)
    sg=salinidad1(con_geo,tem_geo)

    for i in range(0,len(Sal)):
        a=Sal[i]/sg*100
        ps.append(a)
    return Sal  # Serie temporal de potencial de salinidad

def Abrir_excel(ruta_carpeta, nombre_excel, nombre_hoja):
    vars()[str(nombre_hoja)] = pd.read_excel(ruta_carpeta + '\\' + str(nombre_excel) + '.xlsx', header=0,
                                             index_col='Fecha', sheet_name=str(nombre_hoja))
    return vars()[str(nombre_hoja)]

# Caudales antrópicos delta
def caudales_antropicos(Afluentes, Efluentes):
    dq_ant = []
    afl = []
    efl = []
    for i in range(0, Afluentes.shape[0]):
        a = np.sum(Afluentes.iloc[i].values)
        b = np.sum(Efluentes.iloc[i].values)
        delt = a - b
        dq_ant.append(delt)  # Delta de caudales antrópicos
        afl.append(a)  # Caudales afluentes
        efl.append(b)  # Caudales efluente
    return dq_ant, afl, efl

def graficar(variable, fecha, ylabel, cota_rebose=0):
    if cota_rebose != 0:
        cota_desborde = [cota_rebose for i in range(0, len(fecha))]
        plt.plot(fecha, cota_desborde, color='black')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.plot(fecha, variable, color='#131C76')
    plt.gcf().autofmt_xdate()
    plt.grid(linestyle='--', linewidth='0.5')
    plt.xlim(fecha[0], fecha[len(fecha) - 1])
    plt.xticks(rotation=45, size='medium')
    plt.ylabel(str(ylabel), fontsize=14, **{'fontname': 'Times new roman'})
    plt.xlabel('')
    plt.legend()

def NS(observados, modelados):  # índice Nash para calibración
    a = np.sum(np.square(modelados - observados))
    b = np.sum(np.square(observados)) - ((1 / len(observados)) * (np.sum(observados) ** 2))
    return 1 - (a / b)

def cambiar_formato(lista_variable,fechas):
    names = ['INST-VAL', 'M3/S', '', '', 'FLOW', 'ITP', 'RIO CHICAMOCHA']
    blanks = ['' for i in range(0, 7)]
    for i in range(0,len(blanks)):
        if i==0:
            a=np.insert(fechas,0,blanks[i])
        else:
            a=np.insert(a,0,blanks[i])
        fecha=a
    for name in range(0,len(names)):
        b=lista_variable[:]
        b.insert(0, names[name])
        lista_variable=b
    dss=pd.DataFrame()
    dss[0]=fecha
    dss[1]=lista_variable
    dss=dss.fillna('')
    return dss

################## Dársena 1 ############################################################

fec1="01/01/2017"
fec2="12/31/2017" #Modificar fecha según periodo simulado
fecha=np.array(pd.date_range(fec1,fec2))

#Variables de entrada D1
ruta_carpeta=r'C:\Users\sergi\OneDrive\Documents\Universidad\Proyecto_BIO\Proyecto_Boyaca_BIO\Modelos\Modelo_sistemas_lenticos\Darsena_1'
nombre_excel='Variables_de_entrada_Darsena_1'
Afluentes=Abrir_excel(ruta_carpeta,nombre_excel,'Afluentes')
Efluentes=Abrir_excel(ruta_carpeta,nombre_excel,'Efluentes')
Conductividad=Abrir_excel(ruta_carpeta,nombre_excel,'Conductividad')
Temperatura=Abrir_excel(ruta_carpeta,nombre_excel,'Temperatura')
#observados=Abrir_excel(ruta_carpeta,nombre_excel,'Datos_observados')
Horas_bombeo=Abrir_excel(ruta_carpeta,nombre_excel,'Horas_bombeo')

#Variables climáticas
nombre_excel='Evaporacion'
Evaporacion=Abrir_excel(ruta_carpeta,nombre_excel,'Sheet1')
nombre_excel='Precipitacion'
Precipitacion=Abrir_excel(ruta_carpeta,nombre_excel,'Sheet1')
Precipitacion=Precipitacion['Q. Seca'].loc[fec1:fec2]
Evaporacion=Evaporacion['Q. Seca'].loc[fec1:fec2]


#Calculo de alturas y caudal de salida de dársena 1
No=1.5
prec=Precipitacion
evap=Evaporacion
dq_ant,afl,efl=caudales_antropicos(Afluentes,Efluentes)
hor_bom=Horas_bombeo['Horas de bombeo']

Alturas_D1,Caudal_salida_D1,Areas_mod_D1=Dinamica_darsena_1(No,prec,evap,dq_ant,hor_bom)

# Alturas_cal=pd.DataFrame(Alturas_D1) #Para calibración
# Alturas_cal['Fecha']=fecha
# Alturas_cal.set_index('Fecha',inplace=True)
# Alturas_cal=Alturas_cal.rename(columns={0: "Modelados"})
#
# Alturas_cal.plot(figsize=(15,6),color='black',label='Modelados') #Para calibración
# #plt.scatter(x=observados.index,y=observados[observados.columns[0]],s=8,color='red',label='Observados')
# plt.grid(linestyle='--',linewidth ='0.5')
# plt.legend()

# print('El índice de NASH es: ', round(NS(observados[observados.columns[0]],Alturas_cal['Modelados']),3))
graficar(Alturas_D1,fecha,'Niveles [m]')
plt.show()

graficar(Caudal_salida_D1,fecha,'Caudal [m3/s)')
plt.show()

#Potencial de salinidad

#Salinidad dársena 1
salinidad_D1=pd.DataFrame()
for j in range(0,Conductividad.shape[1]):
    b=[]
    for i in range(0,Conductividad.shape[0]):
        a=salinidad1(Conductividad.iloc[i,j],Temperatura.iloc[i,j])
        b.append(a)
    salinidad_D1[Conductividad.columns[j]]=b
salinidad_D1.index=Conductividad.index

#Cargas entrantes a la dársena 1, se realizando multiplicando cada caudal por cada concentración. Finalmente se suman todas las cargas
#diariamente
cargas=[]
for i in range(0,Afluentes.shape[0]):
    a=np.sum(salinidad_D1.iloc[i].values*Afluentes.iloc[i].values)
    cargas.append(a)
cargas_D1=np.array(cargas)

#Potencial de salinización de la dársena 1
vol_sis=Alturas_D1*Areas_mod_D1 #Se calcula el volumen de dársena 1 con cada nivel
cargas_afluentes=cargas_D1 #Se llaman las cargas de salinidades
caudales_efl=np.array(efl) #Se llaman los caudales efluentes
con_inicial=10.16
tem_inicial=20

#serie temporal de salinidad
Salinidad_efl_D1=salinizacion(vol_sis,cargas_afluentes,caudales_efl,con_inicial,tem_inicial)
cargas_salida_D1=Salinidad_efl_D1*Caudal_salida_D1
#################################### Dársena 2 ################################################

fec1="01/01/2017"
fec2="12/31/2017" #Modificar fecha según periodo simulado
fecha=np.array(pd.date_range(fec1,fec2))

#Variables de entrada D2
ruta_carpeta=r'C:\Users\sergi\OneDrive\Documents\Universidad\Proyecto_BIO\Proyecto_Boyaca_BIO\Modelos\Modelo_sistemas_lenticos\Darsena_2'
nombre_excel='Variables_de_entrada_Darsena_2'
Afluentes=Abrir_excel(ruta_carpeta,nombre_excel,'Afluentes')
Efluentes=Abrir_excel(ruta_carpeta,nombre_excel,'Efluentes')
Conductividad=Abrir_excel(ruta_carpeta,nombre_excel,'Conductividad')
Temperatura=Abrir_excel(ruta_carpeta,nombre_excel,'Temperatura')
#observados=Abrir_excel(ruta_carpeta,nombre_excel,'Datos_observados')
Compuerta=Abrir_excel(ruta_carpeta,nombre_excel,'Compuerta')

#Variables climáticas
nombre_excel='Evaporacion'
Evaporacion=Abrir_excel(ruta_carpeta,nombre_excel,'Sheet1')
nombre_excel='Precipitacion'
Precipitacion=Abrir_excel(ruta_carpeta,nombre_excel,'Sheet1')
Precipitacion=Precipitacion['Q. Seca'].loc[fec1:fec2]
Evaporacion=Evaporacion['Q. Seca'].loc[fec1:fec2]

#Calculo de altura y caudal de dársena 2
No=1.4
Cfl=2497.16
Cfc=2497.86
prec=Precipitacion
evap=Evaporacion
dq_ant,afl,efl=caudales_antropicos(Afluentes,Efluentes)
aper_com=Compuerta['Porcentaje de apertura (%)']
cau_dar1=Caudal_salida_D1

Alturas_D2,Caudal_salida_D2,Areas_mod_D2=Dinamica_Darsena2(No,Cfl,Cfc,prec,evap,dq_ant,cau_dar1,aper_com)

# Alturas_cal=pd.DataFrame(Alturas_D2) #Para calibración
# Alturas_cal['Fecha']=fecha
# Alturas_cal.set_index('Fecha',inplace=True)
# Alturas_cal=Alturas_cal.rename(columns={0: "Modelados"})
#
# Alturas_cal.plot(figsize=(15,6),color='black',label='Modelados') #Para calibración
# #plt.scatter(x=observados.index,y=observados[observados.columns[0]],s=8,color='red',label='Observados')
# #observados[observados.columns[0]].plot()
# plt.grid(linestyle='--',linewidth ='0.5')
# plt.legend()

graficar(Alturas_D2,fecha,'Niveles [m]')
plt.show()

graficar(Caudal_salida_D2,fecha,'Caudal [m3/s)')
plt.show()

#Potencial de salinidad
#Salinidad dársena 2
salinidad_D2=pd.DataFrame()
for j in range(0,Conductividad.shape[1]):
    b=[]
    for i in range(0,Conductividad.shape[0]):
        a=salinidad1(Conductividad.iloc[i,j],Temperatura.iloc[i,j])
        b.append(a)
    salinidad_D2[Conductividad.columns[j]]=b
salinidad_D2.index=Conductividad.index

plt.show()

#Cargas entrantes a la dársena 2, se realizando multiplicando cada caudal por cada concentración. Finalmente se suman todas las cargas
#diariamente
cargas=[]
for i in range(0,Afluentes.shape[0]):
    a=np.sum(salinidad_D2.iloc[i].values*Afluentes.iloc[i].values)
    cargas.append(a)
cargas=np.array(cargas+cargas_salida_D1)  #Se suma adicionalmente la carga proveniente de Darsena 1

#Potencial de salinización de la dársena 2
vol_sis=Alturas_D2*Areas_mod_D2 #Se calcula el volumen de dársena 2 con cada nivel
cargas_afluentes=cargas #Se llaman las cargas de salinidades
caudales_efl=np.array(efl) #Se llaman los caudales efluentes
con_inicial=10.16
tem_inicial=20

#serie temporal de salinidad
Salinidad_efl_D2=salinizacion(vol_sis,cargas_afluentes,caudales_efl,con_inicial,tem_inicial)
#Salidas Caudal_salida_D2, salinidad_D2
print(cambiar_formato(Salinidad_efl_D2,fecha))