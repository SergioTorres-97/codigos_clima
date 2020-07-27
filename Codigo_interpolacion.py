# import arcpy
# from arcpy import env
# from arcpy.sa import *
from datetime import datetime
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import openpyxl

#Se establece un espacio de trabajo
arcpy.env.overwriteOutput = True
env.workspace = r"E:\Documents\Interpolacion\Kriging_Precipitacion\Default.gdb"

def dividir_archivo(Archivo_original,ruta_salida,nombre_archivo_salida='Datos_variable_',a=3,b=245):
    Columnas_iniciales=[0,1,2] #Columnas a repetir en cada iteración (se debe tener transpuesto el archivo original con
    #columnas de longitud y latitud
    columnas=Archivo_original.iloc[:,Columnas_iniciales] #Columnas a repetir en cada iteración
    Numero_datos=Archivo_original.iloc[0,:].count() #Datos del registro
    i=0
    lim_datos=b
    estado=False
    while i<Numero_datos:
        g=Archivo_original.iloc[:,a:b]
        f=pd.merge(columnas,g, how='left', on='Fecha')
        f.to_excel(ruta_salida+'\\'+nombre_archivo_salida+str(i)+'.xlsx')
        a=b
        b=a+(lim_datos-3)
        i=i+1
        if estado:
            break
        elif b>=Numero_datos:
            b=Numero_datos
            estado=True

def crear_shapes(ruta_archivos,ruta_geodatabase,nombre_variable='Precipitacion',nombre_archivo_salida='Datos_variable_'):
    iteraciones = 0
    coordinate_system="GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],VERTCS['WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PARAMETER['Vertical_Shift',0.0],PARAMETER['Direction',1.0],UNIT['Meter',1.0]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision"
    while iteraciones < i:
        Hoja1___2_ = ruta_archivos + '\\' + nombre_archivo_salida + str(iteraciones) + '.xlsx' + '\\' + 'Sheet1$'  # Variable a interpolar
        salida = ruta_geodatabase+'\\'+nombre_variable+ str(iteraciones)  # Estaciones a crear dependiendo de la variable
        arcpy.XYTableToPoint_management(in_table=Hoja1___2_, out_feature_class=salida, x_field="Longitud",
                                        y_field="Latitud", z_field="Altitud",
                                        coordinate_system=coordinate_system)
        iteraciones = iteraciones + 1

def revisar_licencias():
    # Check out the ArcGIS Spatial Analyst extension license
    arcpy.CheckOutExtension("Spatial")
    # Check out the ArcGIS Geostatistical Analyst extension license
    arcpy.CheckOutExtension("GeoStats")

def interpolacion(ruta_geodatabase,ruta_archivos_xlsx,ruta_archivos_respaldo,
                  nombre_variable='Precipitacion',nombre_raster='DEM',nombre_centroides='Centroides',nombre_estaciones='Estaciones')
    arcpy.env.overwriteOutput = True
    env.workspace = ruta_geodatabase
    # Se definen variables locales:
    #Se establece el rango de fechas
    Prec=pd.DataFrame()
    est=pd.DataFrame()
    Input_explanatory_variable_rasters = nombre_raster #Se llama el modelo de elevación digital
    Centroides = nombre_centroides #Se llaman los centroides de las microcuencas
    Estaciones=nombre_estaciones #Se llaman las estaciones en formato shape
    Output_prediction_raster = ""
    Output_diagnostic_feature_class = ""
    inPointFeatures = Centroides
    inPointFeatures2= Estaciones
    iteraciones=0
    i=3
    while iteraciones<i:
        
        

        shapes = ruta_geodatabase+'\\'+nombre_variable+ str(iteraciones) #Estaciones a crear dependiendo de la variable
        zFields = arcpy.ListFields(shapes,field_type="Double")
        a=zFields[3].name
        b=zFields[len(zFields)-1].name
        a=a.replace('F','')
        b=b.replace('F','')
        x=a.split('_')
        y=b.split('_')
        fecha_inicial=x[1]+'/'+x[2]+'/'+x[0] #Inicio de la simulación %m%d%a
        fecha_final=y[1]+'/'+y[2]+'/'+y[0] #Fin de la simulación
        fecha=np.array(pd.date_range(fecha_inicial,fecha_final),dtype='datetime64[D]') #Se crea un vector de fechas
        contador=0 #Se inicializa el contador
        for zField in zFields[3:]: #Se inicializa el ciclo desde la tercera columna
            Dependent_variable_field = zField.name
            outLayer = str(zField.name)
            arcpy.EBKRegressionPrediction_ga(in_features=shapes, dependent_field=Dependent_variable_field, in_explanatory_rasters=Input_explanatory_variable_rasters, out_ga_layer=outLayer, out_raster=Output_prediction_raster, out_diagnostic_feature_class=Output_diagnostic_feature_class, measurement_error_field="", min_cumulative_variance="95", in_subset_features="", transformation_type="NONE", semivariogram_model_type="K_BESSEL", max_local_points="100", overlap_factor="1", number_simulations="100", search_neighborhood="NBRTYPE=StandardCircular RADIUS=0.201366773089453 ANGLE=0 NBR_MAX=15 NBR_MIN=10 SECTOR_TYPE=ONE_SECTOR")
            # Process: GA Layer To Rasters
            Kriging0__2_ = outLayer
            Additional_rasters = ""
            arcpy.GALayerToRasters_ga(in_geostat_layer=outLayer, out_raster=Kriging0__2_, output_type="PREDICTION", quantile_probability_value="", cell_size="1.46933333199991E-03", points_per_block_horz="1", points_per_block_vert="1", additional_rasters="", out_elevation="")
            inRaster = ruta_geodatabase+str('\\'+Kriging0__2_)
            Precip_centroides = str(zField.name)+'_tb'
            estaciones_centroides = str(zField.name)+'_est'
            ExtractValuesToPoints(inPointFeatures, inRaster, Precip_centroides,"INTERPOLATE", "VALUE_ONLY")
            ExtractValuesToPoints(inPointFeatures2, inRaster, estaciones_centroides,"INTERPOLATE", "VALUE_ONLY")
            #arcpy.AlterField_management(r'C:\Users\sergi\OneDrive\Documents\Universidad\Proyecto_BIO\Nuevas_estaciones\Ejemplo_Kriging\Kriging\Default.gdb'+str('\\'+Precip_centroides), 'RASTERVALU', 'Precipitacion')
            in_table = Precip_centroides
            in_table_est = estaciones_centroides
            out_xlsx = ruta_archivos_xlsx+'\\'+'prec_'+str(outLayer)+".xls"
            out_est_xlsx = ruta_archivos_xlsx+'\\'+'est_'+str(outLayer)+".xls"
            arcpy.TableToExcel_conversion(in_table, out_xlsx)
            arcpy.TableToExcel_conversion(in_table_est, out_est_xlsx)
            Preci=pd.read_excel(ruta_archivos_xlsx+'\\'+'prec_'+str(outLayer)+'.xls')
            esta=pd.read_excel(ruta_archivos_xlsx+'\\'+'est_'+str(outLayer)+".xls")
            del esta['OBJECTID']
            esta['Centroide']=esta['Fecha']
            del esta['Fecha']
            del esta['Latitud']
            del esta['Longitud']
            del esta['Altitud']
            esta[fecha[contador]]=esta['RASTERVALU']
            del esta['RASTERVALU']
            if iteraciones==0 and contador ==0:
                Prec['ID']=Preci['OBJECTID']
                Prec['Centroide']=Preci['nom_microc']
                Prec[fecha[contador]]=Preci['RASTERVALU']
                est['Centroide']=esta['Centroide']
                est[fecha[contador]]=esta[fecha[contador]]
                Prec=Prec.append(est,ignore_index=True)
            else:
                Prec[fecha[contador]]=Preci['RASTERVALU'].append(esta[fecha[contador]],ignore_index=True)
            arcpy.Delete_management(in_table) #Se eliminan los shapes creados
            arcpy.Delete_management(in_table_est)
            arcpy.Delete_management(inRaster) #Se eliminan los raster creados
            os.remove(ruta_archivos_xlsx+'\\'+'prec_'+str(outLayer)+'.xls')
            os.remove(ruta_archivos_xlsx+'\\'+'est_'+str(outLayer)+'.xls')
            print('iteracion: '+ str(iteraciones) + ' contador: ' + str(contador)+' Fecha: '+str(fecha[contador]))
            #if contador==3:
                #break
            contador=contador+1
        #if iteraciones==2:
            #break
        a=Prec.transpose()
        a_new=a.rename(index={'Centroide':'Fecha'})
        new_header=a_new.iloc[0]
        a_new= a_new[1:]
        a_new.columns=new_header
        a_new.to_excel(ruta_archivos_respaldo+'\\Precipitacion_'+str(iteraciones)+'.xlsx')
        iteraciones=iteraciones+1
    del Prec['ID']
    a=Prec.transpose()
    a_new=a.rename(index={'Centroide':'Fecha'})
    new_header=a_new.iloc[0]
    a_new= a_new[1:]
    a_new.columns=new_header
    a_new.to_excel(ruta_archivos_xlsx+'\\'+'salida.xlsx')





