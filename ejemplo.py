import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis
import seaborn as sns
import re

#Establecer pruebas de normalidad
#Precipitacion
path=r'C:\Users\sergi\OneDrive\Documents\Universidad\Proyecto_BIO\Nuevas_estaciones\Precipitacion\Precipitacion.csv'

datos=pd.read_csv(path,sep=',',header=0,index_col='Fecha')

rainy_days=[] #Dias de lluvia
for i in range(0,datos.shape[1]):
    a=list(datos[datos.columns[i]])
    count = sum(map(lambda x:x >= 1, a))
    b=round(count/datos[datos.columns[i]].count()*100,2)
    rainy_days.append(b)

max=[]
for i in range(0,datos.shape[1]):
    a = round(datos[datos.columns[i]].max(),2)
    max.append(a)

min=[]
for i in range(0,datos.shape[1]):
    a = round(datos[datos.columns[i]].min(),2)
    min.append(a)

std=[]
for i in range(0,datos.shape[1]):
    a = round(datos[datos.columns[i]].std(),2)
    std.append(a)

median=[]
for i in range(0,datos.shape[1]):
    a = round(datos[datos.columns[i]].median(),2)
    median.append(a)

mean=[]
for i in range(0,datos.shape[1]):
    a = round(datos[datos.columns[i]].mean(),2)
    mean.append(a)

kurt=[]
for i in range(0,datos.shape[1]):
    a = round(kurtosis(list(datos[datos.columns[i]].dropna()),fisher=True),2)
    kurt.append(a)

columnas=[]
for i in range(0,datos.shape[1]):
    a=str(datos.columns[i])
    a=a.replace('_NaN','')
    v = re.sub(r'\[.*?\]', '', a)
    columnas.append(v)

resultados=pd.DataFrame()
resultados['Station name']=columnas
resultados['Rainy Days (%)']=rainy_days
resultados['Average (mm)']=mean
resultados['Median (mm)']=median
resultados['Standard deviation (mm)']=std
resultados['Maximum value (mm)']=max
resultados['Kurtosis']=kurt


#resultados.to_excel(r'C:\Users\sergi\OneDrive\Documents\Universidad\Informe_joven_investigador\Informe_final\resultados_excel\Mapas.xlsx',
#                    index=False)

datos.columns=columnas
plt.figure(figsize=(15,10))
sns.set(font_scale=0.7)
heatmap=sns.heatmap(datos.corr(method='spearman'),annot=True, vmin=0, vmax=1, center= 0.5,
            cmap= 'coolwarm')
heatmap.set_xticklabels(heatmap.get_yticklabels(), rotation=90)
# plt.savefig(r'C:\Users\sergi\OneDrive\Documents\Universidad\Informe_joven_investigador\Informe_final\graficos\correlacion.png')

plt.show()