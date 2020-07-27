import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import xlrd
from datetime import datetime
from scipy.optimize import curve_fit

def transformar(informacion):
    datos=pd.DataFrame(informacion)
    columnas=['ID','Measured','Predicted']
    datos.columns=columnas
    datos.set_index(columnas[0],inplace=True)
    return datos
def ordenar_datos(ruta):
    wb = xlrd.open_workbook(ruta)
    print(datetime.now())
    informacion = []
    for hoja in range(0, len(wb.sheet_names())):
        sheet = wb.sheet_by_index(hoja)
        sheet.cell_value(0, 0)
        for fila in range(1, sheet.nrows):
            filas = []
            for columna in range(1, sheet.ncols):
                filas.append(round(sheet.cell_value(fila, columna), 3))
            informacion.append(filas)

    validacion = transformar(informacion)
    validacion[validacion.columns[0]] = eliminacion(np.array(validacion[validacion.columns[0]]))
    validacion[validacion.columns[1]] = eliminacion(np.array(validacion[validacion.columns[1]]))
    return validacion
def eliminacion(vector):
    for elementos in range(0,len(vector)):
        if vector[elementos]<0:
            vector[elementos]=0
    return vector
def graficar(medidos,simulados):
    plt.figure(figsize=(10,6))
    plt.scatter(medidos,simulados,s=8,color='black')
    plt.xlim(0,160)
    plt.ylim(0,160)
    plt.minorticks_on()
    plt.grid(which='major', linestyle='-', linewidth='0.5')
    plt.grid(which='minor', linestyle=':', linewidth='0.5')
    plt.xlabel('Observed data [mm]',fontsize=14,fontweight='bold',**{'fontname':'calibri'})
    plt.ylabel('Simulated data [mm]',fontsize=14,fontweight='bold',**{'fontname':'calibri'})
    plt.xticks(size='large', color='k', rotation=45, **{'fontname': 'calibri'})
    plt.yticks(size='large', color='k', rotation=0, **{'fontname': 'calibri'})
    plt.legend()
    # ruta_guardar=r'C:\Users\sergi\OneDrive\Documents\Universidad\Informe_joven_investigador\Informe_final\graficos\Validacion_llenado'
    # plt.savefig(ruta_guardar+'\\'+str(fec1[4:])+'.png')
def CE(obs,est):
    n=len(obs)
    ave=sum(obs)/n
    c=[]
    d=[]
    for i in range(0,n):
        a=(obs[i]-est[i])**2
        b=(obs[i]-ave)**2
        c.append(a)
        d.append(b)
    CE=1-(sum(c)/sum(d))
    return CE
def R2(observados,modelados):
    def func(x,observados,modelados):
        return (observados*x)+modelados
    z = np.polyfit(observados,modelados, 1)
    p = np.poly1d(z)
    popt, pcov = curve_fit(func, observados,modelados)
    residuals = modelados- func(observados, *popt)
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((modelados-np.mean(modelados))**2)
    r2 = round(1 - (ss_res / ss_tot),3)
    return r2
def d(observados,modelados):
    a=np.sum(np.square(modelados-observados))
    b=np.sum(np.square(abs(modelados-np.mean(modelados))+abs(observados-np.mean(observados))))
    return 1-(a/b)

print(datetime.now())
ruta=r'C:\Users\sergi\OneDrive\Documents\Universidad\Proyecto_BIO\Nuevas_estaciones\Validacion_interpolacion\Validacion_cruzada.xlsx'
validacion=ordenar_datos(ruta)
# validacion.to_excel(r'C:\Users\sergi\OneDrive\Documents\Universidad\Proyecto_BIO\Nuevas_estaciones\Validacion_interpolacion\ordenados.xlsx')

medidos=np.array(validacion['Measured'])
simulados=np.array(validacion['Predicted'])

graficar(medidos,simulados)
plt.show()

print(CE(medidos,simulados))
print(d(medidos,simulados))
print(R2(medidos,simulados))
print(datetime.now())

####Prueba agrupando datos
prueba=validacion.reset_index()
fec1='1/1/1985'
fec2='1/1/2019'
fecha=pd.date_range(fec1,fec2)

#vars()['Est' + str(i)]
for i in range(1,19):
    vars()['Est' + str(i)]=pd.DataFrame()
    vars()['Est'+str(i)]=prueba.loc[prueba['ID']==i]
    vars()['Est' + str(i)]['Fecha']=fecha
    vars()['Est' + str(i)].drop('ID', axis=1, inplace=True)

Estaciones=pd.DataFrame()
Estaciones['Fecha']=fecha
for i in range(1,19):
    Estaciones=pd.merge(Estaciones,vars()['Est' + str(i)],how='left',on='Fecha')
Estaciones.set_index('Fecha',inplace=True)


# agrupados=Estaciones.groupby(lambda m:m.month).sum()
agrupados=Estaciones
columnas=['Est'+str(i) for i in range(0,agrupados.shape[1])]
agrupados.columns=columnas
for i in range(0,agrupados.shape[1]-1):
    # plt.scatter(agrupados[agrupados.columns[i]],agrupados[agrupados.columns[i+1]])
    # plt.show()
    medidos=np.array(agrupados[agrupados.columns[i]])
    simulados=np.array(agrupados[agrupados.columns[i+1]])
    print('EST'+str(i)+',','CE,',CE(medidos, simulados))
    print('EST'+str(i)+',','d ,',d(medidos, simulados))
    print('EST'+str(i)+',','R2,',R2(medidos, simulados))




