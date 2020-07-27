import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import re

ruta=r'C:\Users\sergi\OneDrive\Documents\Proyecto_ubate\PRECIPITACIÓN'

filenames=glob.glob(ruta+'\*.csv')

datos=[]
for file in filenames:
    df=pd.read_csv(file,header=0,sep=',')
    datos.append(pd.read_csv(file))

datos=pd.concat(datos)
datos=datos[['CodigoEstacion','NombreEstacion','Fecha','Valor']]

Estaciones=np.unique(np.array(datos['NombreEstacion']))

nom_est=[]
for i in range(0,len(Estaciones)):
    a=str(Estaciones[i])
    a=a.replace(' ','')
    a=a.replace('-','')
    v = re.sub(r'\[.*?\]', '', a)
    v=v.lower()
    nom_est.append(v)
print(nom_est)
#['agropecuariagja', 'laboyeraaut', 'novilleros', 'puntadevega', 'ubate', 'ubategranja']
for i in range(0,len(Estaciones)):
    vars()[str(nom_est[i])]=datos.loc[datos['NombreEstacion']==Estaciones[i]]
print(ubategranja)