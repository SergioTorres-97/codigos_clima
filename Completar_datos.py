import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob

'''
Código que permite organizar y completar la información proveniente de los datos extraidos del DHIME

Created on thu Jun 30 05:3:40 2020
@author: Ing. Sergio Torres

'''

def intervalo_fecha(fecha_inicial,fecha_final):
    return np.array(pd.date_range(fecha_inicial,fecha_final))

def organizar_datos(ruta_archivos_dhime,fecha_inicial,fecha_final):
    filenames=glob.glob(ruta_archivos_dhime+'\*.xls')
    Estaciones=[]
    for file in filenames:
        df=pd.read_excel(file,header=0)
        Estaciones.append(pd.read_excel(file))
    variable=pd.concat(Estaciones,sort=False)
    variable=variable.loc[:,["NombreEstacion","Valor","Fecha"]]
    variable['Fecha'] = pd.to_datetime(df.Fecha)
    variable.set_index("Fecha",inplace=True)
    nombres_est = np.unique(variable['NombreEstacion'])

    # Se define un ciclo para extraer todas las estaciones
    for i in range(0, len(nombres_est)):
        vars()[str(nombres_est[i])] = variable.loc[variable['NombreEstacion'] == nombres_est[i]]

    fecha = intervalo_fecha(fecha_inicial,fecha_final)
    Matriz_datos = pd.DataFrame(fecha)
    Matriz_datos.rename(columns={0: "Fecha"}, inplace=True)

    for i in range(0, len(nombres_est)):
        Matriz_datos = pd.merge(Matriz_datos, vars()[nombres_est[i]].iloc[:, 1], how='left', on="Fecha")
    Matriz_datos.set_index('Fecha', inplace=True)
    Matriz_datos.columns = nombres_est

    return Matriz_datos

def outliers(matriz_variable,lim_min,lim_max):
    matriz_variable[matriz_variable>=lim_max]=np.NaN
    matriz_variable[matriz_variable<lim_min]=np.NaN
    return matriz_variable

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

#Se definen los parámetros de entrada para la organización de los datos provenientes del DHIME
ruta=r"C:\Users\sergi\OneDrive\Documents\Universidad\Proyecto_BIO\Nuevas_estaciones\Evaporacion"
fecha_inicial='1/1/1985'
fecha_final='1/1/2019'

Evaporacion=organizar_datos(ruta,fecha_inicial,fecha_final)
print(Evaporacion)
#Se establecen los parámetros necesarios para excluir los outliers de las series temporales. (El criterio de máximo y
#mínimo depende del operario y puede variar por estación
lim_min=0
lim_max=Evaporacion.max().max()+(3*(Evaporacion.std().max()))
Evaporacion=outliers(Evaporacion,lim_min,lim_max)
#Se graba el dataframe en un csv que se empleará en la herramienta Amelia de R
# Evaporacion.to_excel(r'C:\Users\sergi\Desktop\Evaporacion.xlsx')

#Se llaman los archivos provenientes de las múltiples imputaciones realizadas en R
ruta_archivos_R=ruta
nombre_archivo='Evaporacion'

Precipitacion=completar_datos(ruta_archivos_R,nombre_archivo)
print('Número de datos faltantes: ',pd.isnull(Precipitacion).sum().max())
