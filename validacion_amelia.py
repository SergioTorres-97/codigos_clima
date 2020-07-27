import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from scipy.optimize import curve_fit

ruta=r'C:\Users\sergi\OneDrive\Documents\Universidad\Proyecto_BIO\Nuevas_estaciones\Precipitacion\Validacion_metodologia'


def completar_datos(ruta_archivos_R,nombre_archivo,m=5):
    for i in range(1,m+1):
        vars()['imp'+str(i)]=pd.read_csv(ruta_archivos_R+'\\'+nombre_archivo+'-imp'+str(i)+'.csv',header=0,
                                         index_col='Fecha',parse_dates=True)
    for i in range(1,m+1):
        if i ==1:
            a=vars()['imp'+str(i)]
        else:
            a=a+vars()['imp'+str(i)]
        impf=a/m
        impf=impf.fillna(impf.mean().mean())
    return impf
def renombrar_col(datos):
    columnas=[]
    for i in range(0,datos.shape[1]):
        a=str(datos.columns[i])
        a=a.replace('_NaN','')
        v = re.sub(r'\[.*?\]', '', a)
        columnas.append(v)
    datos.columns = columnas
    return datos
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
def matriz(est,obs,fec1,fec2):
    fecha=pd.date_range(fec1,fec2)
    datos=pd.DataFrame()
    datos['Fecha']=fecha
    datos.set_index('Fecha',inplace=True)
    datos=pd.merge(datos,obs,how='left',on="Fecha")
    datos = pd.merge(datos, est, how='left', on="Fecha")
    datos=datos.dropna()
    columnas=['Observados','Estimados']
    datos.columns=columnas
    return datos
def agrupar(variable):
    variable=variable.groupby(lambda m:m.month).sum()
    return variable

#Se completa la serie de prueba
fec1='1/1/2017'
fec2='12/31/2017'
estimados=completar_datos(ruta,'Año_2017')
estimados=renombrar_col(estimados)
estimados=estimados['TUNGUAVITA...AUT..24035430.'].loc[fec1:fec2]
for i in range(0,len(estimados)):
    if estimados[i]<1:
        estimados[i]=0
estimados=np.array(agrupar(estimados))

observados=pd.read_csv(ruta+'\\'+'Precipitacion.csv',sep=',',index_col='Fecha',parse_dates=True)
observados=observados['TUNGUAVITA - AUT [24035430]_NaN'].loc[fec1:fec2]
observados=np.array(agrupar(observados))


# datos=matriz(estimados,observados,fec1,fec2)
# estimados=np.array(datos[datos.columns[1]])
# observados=np.array(datos[datos.columns[0]])

# print([round(estimados[i],2) for i in range(0,len(estimados))])
# print(observados)

meses=['Jan','Feb','Mar','Apr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dec']
plt.figure(figsize=(10,6))
plt.plot(meses,list(observados),'--o',color='black',label='Observed data')
plt.plot(meses,list(estimados),'^',color='black',label='Estimated data',markersize=12)
# plt.scatter(list(observados),list(estimados))
plt.minorticks_on()
plt.grid(which='major', linestyle='-', linewidth='0.5')
plt.grid(which='minor', linestyle=':', linewidth='0.5')
plt.ylabel('Monthly Total Precipitation [mm]',fontsize=14,fontweight='bold',**{'fontname':'calibri'})
plt.xticks(size='large', color='k', rotation=45, **{'fontname': 'calibri'})
plt.yticks(size='large', color='k', rotation=0, **{'fontname': 'calibri'})
plt.legend()
ruta_guardar=r'C:\Users\sergi\OneDrive\Documents\Universidad\Informe_joven_investigador\Informe_final\graficos\Validacion_llenado'
plt.savefig(ruta_guardar+'\\'+str(fec1[4:])+'.png')
plt.show()


print(CE(estimados,observados))
print(R2(estimados,observados))
print(d(estimados,observados))

