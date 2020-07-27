#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from sklearn.cluster import KMeans
import seaborn as sbn
from sklearn import decomposition
import mglearn
from sklearn.preprocessing import MinMaxScaler
from scipy.spatial.distance import cdist
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.cluster import hierarchy
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import StandardScaler

path=r'C:\Users\sergi\Downloads\CN_Area_Total_Final.xlsx'
datos=pd.read_excel(path,header=0,index_col='Subbasin')

datos

correlacion=datos.corr(method='spearman')
plt.figure(figsize=(15,6))
sbn.heatmap(correlacion, linewidths=.5,cmap="Greens")
plt.savefig(r'C:\Users\sergi\OneDrive\Documents\Universidad\Proyecto_BIO\Nuevas_estaciones\Clustering\Graficas\Correlación.png')

correlacion

plt.figure(figsize=(15,6))
z=hierarchy.linkage(datos, 'ward')
hierarchy.dendrogram(z, leaf_font_size=8, labels=datos.index,orientation="right")
plt.xticks(size='medium',color ='k',rotation = 0,**{'fontname':'calibri'})
plt.yticks(size='medium',color ='k',rotation = 0,**{'fontname':'calibri'})
plt.grid(linestyle=':', linewidth='0.5')

#Se reduce el número de dimensiones de la información general
PCA=decomposition.PCA(n_components=2)
PCA.fit(datos)
PCA.explained_variance_ratio_

transformada=PCA.transform(datos)

plt.figure(figsize=(15,6))
mglearn.discrete_scatter(transformada[:,0],transformada[:,1])
plt.savefig(r'C:\Users\sergi\OneDrive\Documents\Universidad\Proyecto_BIO\Nuevas_estaciones\Clustering\Graficas\Datos_sin_escalar.png')

escala=MinMaxScaler()
escala.fit(datos)
escalada=escala.transform(datos)
PCA.fit(escalada)
transformada=PCA.transform(escalada)
plt.figure(figsize=(15,6))
mglearn.discrete_scatter(transformada[:,0],transformada[:,1])
plt.gca()
plt.xticks(size='medium',color ='k',rotation = 0,**{'fontname':'calibri'})
plt.yticks(size='medium',color ='k',rotation = 0,**{'fontname':'calibri'})
plt.xlabel('PCA 1',**{'fontname':'calibri'})
plt.ylabel('PCA 2',**{'fontname':'calibri'})
plt.grid(linestyle=':', linewidth='0.5')
plt.savefig(r'C:\Users\sergi\OneDrive\Documents\Universidad\Proyecto_BIO\Nuevas_estaciones\Clustering\Graficas\Datos_escalados.png')

loadings = PCA.components_.T * np.sqrt(PCA.explained_variance_)
loading_matrix = pd.DataFrame(loadings, columns=['PC1', 'PC2'],index=datos.columns)
loading_matrix

def loading_plot(coeff, labels):
    n = coeff.shape[0]
    for i in range(n):
        plt.arrow(0, 0, coeff[i,0], coeff[i,1], head_width = 0.05, head_length = 0.05, color = 'gray',alpha = 0.5)
        plt.text(coeff[i,0]* 1.15, coeff[i,1] * 1.3, labels[i], color = 'black', ha = 'center', va = 'center',**{'fontname':'Times new roman'})
    plt.xlim(-1,1.5)
    plt.ylim(-1,1.5)
    plt.xticks(size='medium',color ='k',rotation = 45,**{'fontname':'Times new roman'})
    plt.yticks(size='medium',color ='k',rotation = 0,**{'fontname':'Times new roman'})
    plt.ylabel('PC2',fontsize=11,**{'fontname':'Times new roman'})
    plt.xlabel('PC1',fontsize=11, **{'fontname':'Times new roman'})    
    plt.grid(linestyle=':', linewidth='0.5')

fig, ax = plt.subplots(figsize = (15,6))
loading_plot(PCA.components_.T, datos.columns)
plt.savefig(r'C:\Users\sergi\OneDrive\Documents\Universidad\Proyecto_BIO\Nuevas_estaciones\Clustering\Graficas\Diagrama_de_flechas.png')

PCA.fit(transformada)
variance = PCA.explained_variance_ratio_ #calculate variance ratios
var=np.cumsum(np.round(PCA.explained_variance_ratio_, decimals=3)*100)
var #cumulative sum of variance explained with [n] features

PCA.components_.T

X=transformada

plt.figure(figsize=(15,6))
z=hierarchy.linkage(X, 'ward')
hierarchy.dendrogram(z, leaf_font_size=8, labels=datos.index,orientation="right")
plt.xticks(size='medium',color ='k',rotation = 0,**{'fontname':'calibri'})
plt.yticks(size='medium',color ='k',rotation = 0,**{'fontname':'calibri'})
plt.xlabel('Euclidian distance',**{'fontname':'calibri'})
plt.grid(linestyle=':', linewidth='0.5')
plt.savefig(r'C:\Users\sergi\OneDrive\Documents\Universidad\Proyecto_BIO\Nuevas_estaciones\Clustering\Graficas\Dendograma.png')

plt.figure(figsize=(15,6))
plt.ylabel('% Porcentaje de varianza explicada (%)',**{'fontname':'calibri'})
plt.xlabel('Número de atributos',**{'fontname':'calibri'})
plt.xticks(size='medium',color ='k',rotation = 0,**{'fontname':'calibri'})
plt.yticks(size='medium',color ='k',rotation = 0,**{'fontname':'calibri'})
plt.grid(linestyle=':', linewidth='0.5')
#plt.style.context('seaborn-whitegrid')
plt.plot(var,color='black') #Con 2 dimensiones es posible explicar el 86.1% de la varianza
#plt.savefig(r'C:\Users\sergi\OneDrive\Documents\Universidad\Proyecto_BIO\Nuevas_estaciones\Clustering\Graficas\Varianza_acumulada.png')

distortions = []
K = range(1,10)
for k in K:
    kmeanModel = KMeans(n_clusters=k).fit(X)
    kmeanModel.fit(X)
    distortions.append(sum(np.min(cdist(X, kmeanModel.cluster_centers_, 'euclidean'), axis=1)) / X.shape[0])

plt.figure(figsize=(15,6))
plt.plot(K, distortions, 'ko-')

Circle = plt.Rectangle((2.9,0.28),0.2,0.023, fc='white',ec="red")
plt.gca().add_patch(Circle)

plt.xlabel('k',**{'fontname':'calibri'})
plt.ylabel('Distortion',**{'fontname':'calibri'})
plt.xticks(size='medium',color ='k',rotation = 0,**{'fontname':'calibri'})
plt.yticks(size='medium',color ='k',rotation = 0,**{'fontname':'calibri'})
plt.grid(linestyle=':', linewidth='0.5')
plt.savefig(r'C:\Users\sergi\OneDrive\Documents\Universidad\Proyecto_BIO\Nuevas_estaciones\Clustering\Graficas\Elbow_method.png')

n_clusters=3
kmeans = KMeans(n_clusters=n_clusters, init ='k-means++', max_iter=300, n_init=10,random_state=0 )
y_kmeans = kmeans.fit_predict(X)

plt.figure(figsize=(15,6))
plt.scatter(X[y_kmeans==0, 0], X[y_kmeans==0, 1], s = 120, c = 'blue', label = 'Cluster 1',edgecolors='black',marker='*')
plt.scatter(X[y_kmeans==1, 0], X[y_kmeans==1, 1],s = 100, c = 'green', label = 'Cluster 2',edgecolors='black',marker='o')
plt.scatter(X[y_kmeans==2, 0], X[y_kmeans==2, 1],s = 150, c = 'red', label = 'Cluster 3',edgecolors='black',marker='+')
plt.grid(linestyle=':', linewidth='0.5')
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=150, c='black', label = 'Centroids',marker='X')
plt.xticks(size='medium',color ='k',rotation = 0,**{'fontname':'calibri'})
plt.yticks(size='medium',color ='k',rotation = 0,**{'fontname':'calibri'})
plt.xlabel('PC1',**{'fontname':'calibri'})
plt.ylabel('PC2',**{'fontname':'calibri'})
plt.legend()
plt.savefig(r'C:\Users\sergi\OneDrive\Documents\Universidad\Proyecto_BIO\Nuevas_estaciones\Clustering\Graficas\Clustering.png')

f=pd.DataFrame(X,columns=['PC1','PC2'],index=datos.index)

f['cluster']=y_kmeans

for i in range(0,n_clusters+1):
    vars()['Clusters_n_'+str(i)]=f.loc[f['cluster']==i]

f.to_excel(r'C:\Users\sergi\OneDrive\Documents\Universidad\Proyecto_BIO\Nuevas_estaciones\Clustering\Graficas\Clustering.xlsx')

Clusters_n_0

Clusters_n_1

Clusters_n_2





