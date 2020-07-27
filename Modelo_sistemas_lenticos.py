import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import matplotlib.dates as mdates


#Definición de la expresión para el cálculo de la salinidad en unidades de Kg/m3 a
#partir de la conductividad a 25ºc
def salinidad(conductividad,temperatura):
    C_KCL=4.2914 #conductividad de la solución de referencia a 15ºC (S/m) Unesco,1981
    Tc=15 #Temperatura de la solución standard ºC
    C_KCL25=(C_KCL*10000)/(1+(0.0191*(Tc-25))) #se expresa la conductividad de la solución de referencia a 25ºC, empleando una aproximación asumiendo que no existe una temperatura interna de compensación en la celda de medición
    # 10000 para hacer la conversión de S/m a microohms/cm
    a0=0.0080
    a1=-0.1692
    a2=25.3851
    a3=14.0941
    a4=-7.0261
    a5=2.7081
    b0=0.0005
    b1=-0.0056
    b2=-0.0066
    b3=-0.0375
    b4=0.0636
    b5=-0.0144
    # Cálculo de la conductividad a 25ºC
    XT=temperatura-15
    RT35=(((1.0031E-9*XT-6.9698E-7)*XT+1.104259E-4)*XT+2.00564E-2)*XT+0.6766097
    
    if (temperatura==25).any(): #El .any() permite emplear series temporales
        C_25=conductividad*1000 # corresponde al factor de conversión de la conductividad expresada en mS/cm o dS/m a microohms/cm
    else:
        C_25=1000*conductividad/(1+0.0191*(temperatura-25)) #corresponde al factor de conversión de la conductividad expresada en mS/cm o dS/m a microohms/cm
    # Relación de conductividades ajustes por efecto de temperatura y cálculo de
    # la salinidad 
    # Para salinidades entre 0 y 40 ups
    Rt=C_25/C_KCL25
    X=400*Rt
    Y=100*Rt
    f=XT/(1+0.0162*XT)
    deltaS=(f)*(b0+b1*Rt**(1/2)+b2*Rt+b3*Rt**(3/2)+b4*Rt**2+b5*Rt**(5/2))
    S=a0+a1*Rt**(1/2)+a2*Rt+a3*Rt**(3/2)+a4*Rt**2+a5*Rt**(5/2)+deltaS
    salinidad=S-(a0/(1+1.5*X+X**2))-b0*f/(1+Y**(1/2)+Y**(3/2))
    
    return salinidad #Salinidad en kg/m3

#Definición de la expresión para el cálculo de la salinidad en unidades de Kg/m3 a
#partir de la conductividad a 25ºc
def salinidad1(conductividad,temperatura):
    C_KCL=4.2914 #conductividad de la solución de referencia a 15ºC (S/m) Unesco,1981
    Tc=15 #Temperatura de la solución standard ºC
    C_KCL25=(C_KCL*10000)/(1+(0.0191*(Tc-25))) #se expresa la conductividad de la solución de referencia a 25ºC, empleando una aproximación asumiendo que no existe una temperatura interna de compensación en la celda de medición
    # 10000 para hacer la conversión de S/m a microohms/cm
    a0=0.0080
    a1=-0.1692
    a2=25.3851
    a3=14.0941
    a4=-7.0261
    a5=2.7081
    b0=0.0005
    b1=-0.0056
    b2=-0.0066
    b3=-0.0375
    b4=0.0636
    b5=-0.0144
    # Cálculo de la conductividad a 25ºC
    XT=temperatura-15
    RT35=(((1.0031E-9*XT-6.9698E-7)*XT+1.104259E-4)*XT+2.00564E-2)*XT+0.6766097
    
    if temperatura==25: #El .any() permite emplear series temporales
        C_25=conductividad*1000 # corresponde al factor de conversión de la conductividad expresada en mS/cm o dS/m a microohms/cm
    else:
        C_25=1000*conductividad/(1+0.0191*(temperatura-25)) #corresponde al factor de conversión de la conductividad expresada en mS/cm o dS/m a microohms/cm
    # Relación de conductividades ajustes por efecto de temperatura y cálculo de
    # la salinidad 
    # Para salinidades entre 0 y 40 ups
    Rt=C_25/C_KCL25
    X=400*Rt
    Y=100*Rt
    f=XT/(1+0.0162*XT)
    deltaS=(f)*(b0+b1*Rt**(1/2)+b2*Rt+b3*Rt**(3/2)+b4*Rt**2+b5*Rt**(5/2))
    S=a0+a1*Rt**(1/2)+a2*Rt+a3*Rt**(3/2)+a4*Rt**2+a5*Rt**(5/2)+deltaS
    salinidad=S-(a0/(1+1.5*X+X**2))-b0*f/(1+Y**(1/2)+Y**(3/2))
    
    return salinidad #Salinidad en kg/m3

def Ab(x,a=1.391e+06,b=4192,c=6.023):

#x= profundidad del agua en el algo con respecto a la cota de fondo en el lago (m)
#Ley de áreas para el Lago (área en m^2) , ajuste mediante función
#logística

#Batimetría año 2015 Fuente: Corpoboyacá, Geospatial (2015)
    if (x<=0).any():
        Ab=0 #(en m^2)
    else:
        Ab=(a*b*2.718281**(c*x))/(a+b*(2.718281**(6.008*x))-1)#(en m^2)
        
    return Ab

def Ab1(x,a=1.391e+06,b=4192,c=6.023):

#x= profundidad del agua en el algo con respecto a la cota de fondo en el lago (m)
#Ley de áreas para el Lago (área en m^2) , ajuste mediante función
#logística

#Batimetría año 2015 Fuente: Corpoboyacá, Geospatial (2015)
    if (x<=0):
        Ab=0 #(en m^2)
    else:
        Ab=(a*b*2.718281**(c*x))/(a+b*(2.718281**(6.008*x))-1)#(en m^2)
        
    return Ab

def Area_dar(x,a=1.391e+06,b=4192,c=6.023):

#x= profundidad del agua en el algo con respecto a la cota de fondo en el lago (m)
#Ley de áreas para el Lago (área en m^2) , ajuste mediante función
#logística

#Batimetría año 2015 Fuente: Corpoboyacá, Geospatial (2015)
    if (x<=0):
        Ab=0 #(en m^2)
    else:
        Ab=(a*x**2)+(b*x)+c#(en m^2)
        
    return Ab

def compuerta(a,b,y2,cc=0.42,c1=0.0979):
    if a==0:
        Qe1=0
    else:
        if y2/a >= 2.451:
            cv=1
        else:
            if a==0:
                cv=0.96
                v1=0
            else:
                cv=0.96 + (c1*a/y2)
    
        v1=cv*((2*9.81*y2)**0.5)/((1+(cc*a/y2))**0.5)
        cd=(cc*cv)/((1+(cc*a/y2))**0.5)
        Qe1=cd*((2*9.81*y2)**0.5)*a*b
    
    return (Qe1)

def Vb(x):

#x= profundidad del agua en el algo con respecto a la cota de fondo en la
#zona más profunda (m)
#Ley de volúmenes para el Lago , ajuste mediante regresión
#polinomial de 4 orden Coefficients (with 95% confidence bounds):
    p1 =   10340  #(8887, 1.18e+04)
    p2 =  -159700 #(-1.777e+05, -1.418e+05)
    p3 =   873900 #(8.017e+05, 9.461e+05)
    p4 =  -499600  #(-6.055e+05, -3.937e+05)
    p5 =   30380  #(-1.602e+04, 7.678e+04)

    if (x<=0).any():
        Vb=0 #(Volumen en m^3)
    else:
        Vb=p1*x**4 + p2*x**3 + p3*x**2 + p4*x + p5 #(Volumen en m^3)
        
    return (Vb)    

def cargas_tranvase(caudales,conductividad,temperatura):
    sal=salinidad(conductividad,temperatura)
    car=[]
    for i in range(0,len(caudales)):
        a=caudales[i]*sal[i]
        car.append(a)
    return car

#Generación de los niveles en función de los caudales afluentes
def Dinamica_lago(No,Cfl,Cfc,prec,evap,dq_ant,aper_com,q_hid,q_trans):
    
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
    y=Cfl-Cfc #Cálcula la diferencia entre la cota inferior del lago y la cota inferior de la compuerta
    No_com=No-y-aper_com[0]*1.12/100 #Cálcula la lámina de agua sobre la compuerta
    Ao=Ab1(No) #Se cálcula el área inicial 
    Nivel_com=[]
    Caudal_prec=[]
    Caudal_evap=[]
    delta_cau=[]
    Alturas=[]
    Areas_mod=[]
    Caudal_salida=[]
    for i in range(0,len(fecha)):
        if i==0:
            Q_p=prec[i]/(86400*1000)*Ao #Se calcula el caudal por precipitación en función del área inicial
            Q_e=evap[i]/(86400*1000)*Ao #Se calcula el caudal por evaporación en función del área inicial
            aper=compuerta(aper_com[i]*0.012,2.3,No_com) #Apertura de compuerta, mediante el régimen establecido
            dq=q_hid[i]+q_trans[i]+Q_p-Q_e-aper+dq_ant[i] #Se realiza el balance de masas
            Alt_m=(dq/Ao*86400)+No #Se calcula la áltura de la lámina de agua en función del caudal
            Are_m=Ab1(Alt_m) #Se calcula la nueva área ocupada posterior al balance
            N_c=Alt_m-y+aper_com[i]*0.012 #Se calcula la lámina de agua sobre la compuerta
        if i>0:
            Q_p=prec[i]/(86400*1000)*Areas_mod[i-1]
            Q_e=evap[i]/(86400*1000)*Areas_mod[i-1]
            aper=compuerta(aper_com[i]*0.012,2.3,Nivel_com[i-1])
            dq=q_hid[i]+q_trans[i]+Q_p-Q_e-aper+dq_ant[i]
            Alt_m=(dq/Areas_mod[i-1]*86400)+Alturas[i-1]
            Are_m=Ab1(Alt_m)
            N_c=Alt_m-y+aper_com[i]*0.012
        Nivel_com.append(N_c) 
        Caudal_prec.append(Q_p) #lista de caudales por precipitación
        Caudal_evap.append(Q_e) #lista de caudales por evaporación
        delta_cau.append(dq) #lista de variación diaria de caudales
        Caudal_salida.append(aper) #Caudal de salida por la compuerta
        Alturas.append(Alt_m) #Niveles del lago
        Areas_mod.append(Are_m) #Area superficial del lago 
    Alturas=np.array(Alturas)  
    Caudal_salida=np.array(Caudal_salida) 
    return Alturas,Caudal_salida

def salinizacion(vol_sis,cargas_transvase,cargas_afluentes, caudales_efl, con_inicial, tem_inicial, con_geo=2.5,
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

        Mooas3=(Ci * vol_sis[i])+(cargas_afluentes[i]+cargas_transvase[i])*86400
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

def Bombeo_darsena_1(hor_bom,potencia=234):
    caudal=hor_bom*potencia/86400
    return caudal 

#Generación de los niveles en función de los caudales afluentes
def Dinamica_darsena_1(No,prec,evap,dq_ant,hor_bom):
    
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
    Ao=Area_dar(No,-747.6,3195.9,320.76) #Se cálcula el área inicial 
    Caudal_prec=[]
    Caudal_evap=[]
    delta_cau=[]
    Alturas=[]
    Areas_mod=[]
    Caudal_salida=[]
    for i in range(0,len(fecha)):
        if i==0:
            Q_p=prec[i]/(86400*1000)*Ao #Se calcula el caudal por precipitación en función del área inicial
            Q_e=evap[i]/(86400*1000)*Ao #Se calcula el caudal por evaporación en función del área inicial
            bomb=Bombeo_darsena_1(hor_bom[i])
            dq=Q_p-Q_e-bomb+dq_ant[i] #Se realiza el balance de masas
            Alt_m=(dq/Ao*86400)+No #Se calcula la áltura de la lámina de agua en función del caudal
            Are_m=Area_dar(Alt_m,-747.6,3195.9,320.76) #Se calcula la nueva área ocupada posterior al balance
        elif i>0:
            Q_p=prec[i]/(86400*1000)*Areas_mod[i-1]
            Q_e=evap[i]/(86400*1000)*Areas_mod[i-1]
            bomb=Bombeo_darsena_1(hor_bom[i])
            dq=Q_p-Q_e-bomb+dq_ant[i] 
            Alt_m=(dq/Areas_mod[i-1]*86400)+Alturas[i-1]
            Are_m=Area_dar(Alt_m,-747.6,3195.9,320.76)
        Caudal_prec.append(Q_p) #lista de caudales por precipitación
        Caudal_evap.append(Q_e) #lista de caudales por evaporación
        delta_cau.append(dq) #lista de variación diaria de caudales
        Caudal_salida.append(bomb) #Caudal de salida por la compuerta
        Alturas.append(Alt_m) #Niveles del lago
        Areas_mod.append(Are_m) #Area superficial del lago 
    Alturas=np.array(Alturas) 
    Caudal_salida=np.array(Caudal_salida)
    Areas_mod=np.array(Areas_mod)
    return Alturas,Caudal_salida,Areas_mod

#Generación de los niveles en función de los caudales afluentes
def Dinamica_Darsena2(No,Cfl,Cfc,prec,evap,dq_ant,cau_dar1,aper_com):
    
    #cambiar 1.12 de la compuerta
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
    y=Cfl-Cfc #Cálcula la diferencia entre la cota inferior del lago y la cota inferior de la compuerta
    No_com=No-y-aper_com[0]*2/100 #Cálcula la lámina de agua sobre la compuerta
    Ao=Area_dar(No,11444,19653,-2692.7) #Se cálcula el área inicial 
    Nivel_com=[]
    Caudal_prec=[]
    Caudal_evap=[]
    delta_cau=[]
    Alturas=[]
    Areas_mod=[]
    Caudal_salida=[]
    for i in range(0,len(fecha)):
        if i==0:
            Q_p=prec[i]/(86400*1000)*Ao #Se calcula el caudal por precipitación en función del área inicial
            Q_e=evap[i]/(86400*1000)*Ao #Se calcula el caudal por evaporación en función del área inicial
            aper=compuerta(aper_com[i]*0.02,1.5,No_com)
            dq=Q_p-Q_e-aper+dq_ant[i]+cau_dar1[i] #Se realiza el balance de masas
            Alt_m=(dq/Ao*86400)+No #Se calcula la áltura de la lámina de agua en función del caudal
            Are_m=Area_dar(Alt_m,11444,19653,-2692.7) #Se calcula la nueva área ocupada posterior al balance
            N_c=Alt_m-y+aper_com[i]*0.02 #Se calcula la lámina de agua sobre la compuerta
        if i>0:
            Q_p=prec[i]/(86400*1000)*Areas_mod[i-1]
            Q_e=evap[i]/(86400*1000)*Areas_mod[i-1]
            aper=compuerta(aper_com[i]*0.02,1.5,Nivel_com[i-1])
            dq=Q_p-Q_e-aper+dq_ant[i]+cau_dar1[i]
            Alt_m=(dq/Areas_mod[i-1]*86400)+Alturas[i-1]
            Are_m=Area_dar(Alt_m,11444,19653,-2692.7)
            N_c=Alt_m-y+aper_com[i]*0.02 
        Nivel_com.append(N_c) 
        Caudal_prec.append(Q_p) #lista de caudales por precipitación
        Caudal_evap.append(Q_e) #lista de caudales por evaporación
        delta_cau.append(dq) #lista de variación diaria de caudales
        Caudal_salida.append(aper) #Caudal de salida por la compuerta
        Alturas.append(Alt_m) #Niveles del lago
        Areas_mod.append(Are_m) #Area superficial del lago 
    Alturas=np.array(Alturas)  
    Caudal_salida=np.array(Caudal_salida) 
    Areas_mod=np.array(Areas_mod)
    return Alturas,Caudal_salida,Areas_mod

def Abrir_excel(ruta_carpeta,nombre_excel,nombre_hoja):
    vars()[str(nombre_hoja)]=pd.read_excel(ruta_carpeta+'\\'+str(nombre_excel)+'.xlsx',header=0,index_col='Fecha',sheet_name=str(nombre_hoja))
    return vars()[str(nombre_hoja)]

#Caudales antrópicos delta
def caudales_antropicos(Afluentes,Efluentes):
    dq_ant=[]
    afl=[]
    efl=[]
    for i in range(0,Afluentes.shape[0]):
        a=np.sum(Afluentes.iloc[i].values)
        b=np.sum(Efluentes.iloc[i].values)
        delt=a-b
        dq_ant.append(delt) #Delta de caudales antrópicos
        afl.append(a) #Caudales afluentes
        efl.append(b) #Caudales efluente
    return dq_ant,afl,efl

def graficar(variable,fecha,ylabel,cota_rebose=0):
    if cota_rebose!=0:
        cota_desborde = [cota_rebose for i in range(0, len(fecha))]
        plt.plot(fecha, cota_desborde, color='black')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.plot(fecha,variable,color='#131C76')
    plt.gcf().autofmt_xdate()
    plt.grid(linestyle='--',linewidth ='0.5')
    plt.xlim(fecha[0],fecha[len(fecha)-1])
    plt.xticks(rotation=45,size='medium')
    plt.ylabel(str(ylabel),fontsize=14,**{'fontname':'Times new roman'})
    plt.xlabel('')
    plt.legend()

def NS(observados,modelados): #índice Nash para calibración
    a=np.sum(np.square(modelados-observados))
    b=np.sum(np.square(observados))-((1/len(observados))*(np.sum(observados)**2))
    return 1-(a/b)

#Se define una funcion para cambiar los formatos de salida a DSS-VUE, en funcion de la fecha y la variable
def cambiar_formato(lista_variable,fechas):
    names = ['INST-VAL', 'M3/S', '', '', 'FLOW', 'LAGO SOCHAGOTA', 'RIO CHICAMOCHA']
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

###### LAGO SOCHAGOTA ######################################################3

#Vector de fechas
fec1="01/01/1999"
fec2="12/31/1999" #Modificar fecha según periodo simulado
fecha=np.array(pd.date_range(fec1,fec2))

#Variables de entrada Lago
ruta_carpeta=r'C:\Users\sergi\Desktop\Archivos_prueba\Escenario_base\1999'
nombre_excel='Variables_de_entrada_Lago'
Afluentes=Abrir_excel(ruta_carpeta,nombre_excel,'Afluentes')
Efluentes=Abrir_excel(ruta_carpeta,nombre_excel,'Efluentes')
Conductividad=Abrir_excel(ruta_carpeta,nombre_excel,'Conductividad')
Temperatura=Abrir_excel(ruta_carpeta,nombre_excel,'Temperatura')
Regimen_compuerta=Abrir_excel(ruta_carpeta,nombre_excel,'Compuerta')
#observados=Abrir_excel(ruta_carpeta,nombre_excel,'Datos observados')

#Caudal hidrológico (Escenario base)
ruta_carpeta=r'C:\Users\sergi\OneDrive\Documents\Universidad\Proyecto_BIO\Proyecto_Boyaca_BIO\Modelos\Bases_de_Datos'
fec1_="01/01/1985"
fec2_="12/31/2018" #Modificar fecha según periodo simulado
vec_fecha=np.array(pd.date_range(fec1_,fec2_))
Quebrada_Honda=pd.read_excel(ruta_carpeta+'\\'+'Informacion_escenario_base.xls',header=1)
Quebrada_Honda=Quebrada_Honda.iloc[:,[50]]
Quebrada_Honda=Quebrada_Honda.iloc[5:Quebrada_Honda.shape[0], :]
Quebrada_Honda['Fecha']=vec_fecha
Quebrada_Honda.set_index('Fecha',inplace=True)
Quebrada_Honda=Quebrada_Honda.rename(columns={'J887':'Quebrada_Honda'})
Quebrada_Honda= Quebrada_Honda.loc[fec1:fec2]

#Varables climáticas
ruta_carpeta=r'C:\Users\sergi\OneDrive\Documents\Universidad\Proyecto_BIO\Proyecto_Boyaca_BIO\Modelos\Modelo_sistemas_lenticos\Lago_Sochagota'
nombre_excel='Evaporacion'
Evaporacion=Abrir_excel(ruta_carpeta,nombre_excel,'Sheet1')
nombre_excel='Precipitacion'
Precipitacion=Abrir_excel(ruta_carpeta,nombre_excel,'Sheet1')
Precipitacion=Precipitacion['TUNGUAVITA - AUT [24035430]'].loc[fec1:fec2]
Evaporacion=Evaporacion['TUNGUAVITA - AUT [24035430]'].loc[fec1:fec2]

#Delta de caudales antrópicos, afluentes, efluentes
dq_ant,afl,efl=caudales_antropicos(Afluentes,Efluentes)

#Caso Lago Sochagota
No=2.55
Cfl=2489.28
Cfc=2489.8
prec=Precipitacion
evap=Evaporacion
dq_ant=dq_ant
aper_com=Regimen_compuerta['Porcentaje de apertura (%)']
q_hid=Quebrada_Honda['Quebrada_Honda']
#Altura y caudales de salida del Lago
Alturas_lago,Caudal_salida_lago=Dinamica_lago(No,Cfl,Cfc,prec,evap,dq_ant,aper_com,q_hid)

#Datos observados
#observados[observados.columns[0]]=2492.06-2489.28-observados[observados.columns[0]] #Para calibración

Alturas_cal=pd.DataFrame(Alturas_lago) #Para calibración
Alturas_cal['Fecha']=fecha
Alturas_cal.set_index('Fecha',inplace=True)
Alturas_cal=Alturas_cal.rename(columns={0: "Modelados"})

# fig = plt.figure()
# x=Alturas_cal.index
# plt.figure(figsize=(15,6))
# plt.subplot(111)

# cota_desborde=[2.78 for i in range(0,len(fecha))]
# plt.plot(Alturas_cal.index,cota_desborde,'black')
# plt.plot(Alturas_cal.index,Alturas_cal,label='Modelados')
# #plt.scatter(x=observados.index,y=observados[observados.columns[0]],s=8,color='red',label='Observados')
# plt.grid(linestyle='--',linewidth ='0.5')
# #plt.xlim('2011-09-01','2011-10-01')
# plt.legend()

print(Alturas_lago)
print(Caudal_salida_lago)
graficar(Alturas_lago,fecha,'Niveles [m]',2.78)
plt.show()

graficar(Caudal_salida_lago,fecha,'Caudal [m3/s)')
plt.show()

#Salinidad lago
salinidad_lago=pd.DataFrame()
for j in range(0,Conductividad.shape[1]):
    b=[]
    for i in range(0,Conductividad.shape[0]):
        a=salinidad1(Conductividad.iloc[i,j],Temperatura.iloc[i,j])
        b.append(a)
    salinidad_lago[Conductividad.columns[j]]=b
salinidad_lago.index=Conductividad.index

#Cargas entrantes al lago, se realizando multiplicando cada caudal por cada concentración. Finalmente se suman todas las cargas
#diariamente
cargas=[]
for i in range(0,Afluentes.shape[0]):
    a=np.sum(salinidad_lago.iloc[i].values*Afluentes.iloc[i].values)
    cargas.append(a)
cargas=np.array(cargas)

vol_sis=Vb(Alturas_lago) #Se calcula el volumen del lago con cada nivel
cargas_afluentes=cargas #Se llaman las cargas de salinidades
caudales_efl=np.array(efl) #Se llaman los caudales efluentes
con_inicial=10.16
tem_inicial=20

#Salinidad de salida del Lago Sochagota en el ciclo de gestión
salinidad_salida_lago=salinizacion(vol_sis, cargas_afluentes, caudales_efl, con_inicial, tem_inicial, con_geo=2.5,tem_geo=21.2)

#Se convierte a DSS
print(cambiar_formato(salinidad_salida_lago,fecha))


