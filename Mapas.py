import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re

path=r'C:\Users\sergi\OneDrive\Documents\Universidad\Proyecto_BIO\Nuevas_estaciones\Precipitacion\Precipitacion.csv'
datos=pd.read_csv(path,header=0,index_col='Fecha')

#datos=datos.groupby(lambda y:y.year).mean()
columnas=[]
for i in range(0,datos.shape[1]):
    a=str(datos.columns[i])
    a=a.replace('_NaN','')
    v = re.sub(r'\[.*?\]', '', a)
    columnas.append(v)

datos.columns=columnas
plt.figure(figsize=(15,6))
ax=datos.count().sort_values(ascending=False).plot(kind='barh',color='#52C9DB')
plt.grid(linestyle='--',linewidth ='0.5')
plt.xticks(size='large',color ='k',rotation = 45,**{'fontname':'calibri'})
plt.yticks(size='large',color ='k',rotation = 0,**{'fontname':'calibri'})
plt.xlabel('Número de datos')
for tick in ax.get_xticklabels():
    tick.set_fontsize(10)
for tick in ax.get_yticklabels():
    tick.set_fontsize(10)

plt.xlim(0,12420)
# plt.show()
# datos=datos.loc[datos['SUB']==6]
#
# SED_OUT=datos[['SUB', 'YEAR', 'MON','SED_OUTtons']]
# SED_OUT.set_index('SUB',inplace=True)
#
# fecha=[]
#
# for i in range(0,SED_OUT.shape[0]):
#     a=(str(list(SED_OUT['YEAR'])[i])+'/'+str(list(SED_OUT['MON'])[i])+'/01')
#     a=datetime.strptime(a, '%Y/%m/%d')
#     fecha.append(a)
#
# SED_OUT=SED_OUT.drop(['YEAR','MON'],axis=1)
# SED_OUT['Fecha']=fecha
# SED_OUT.set_index('Fecha',inplace=True)
# print(SED_OUT.describe())
#
# SED_OUT.plot(legend=False,color='#EA470B')
# plt.grid(linestyle='--',linewidth ='0.5')
# plt.xticks(size='large',color ='k',rotation = 45,**{'fontname':'calibri'})
# plt.yticks(size='large',color ='k',rotation = 0,**{'fontname':'calibri'})
# plt.ylabel('Sediments [TON]',fontsize=12,**{'fontname':'calibri'})
# plt.xlabel('')
# plt.savefig(r'C:\Users\sergi\Desktop\Sedimentos.png')
# plt.show()
#
# plt.hist(SED_OUT[SED_OUT.columns[0]],bins=10,color='#0608A1')
# plt.grid(linestyle='--',linewidth ='0.5')
# plt.ylabel('Sediments [TON]',fontsize=12,**{'fontname':'calibri'})
# plt.xlabel('Frequency')
# plt.savefig(r'C:\Users\sergi\Desktop\Histogramas.png')

# plt.show()
