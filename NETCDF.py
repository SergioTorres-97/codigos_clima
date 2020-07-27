# from netCDF4 import Dataset
# import numpy as np
# import matplotlib.pyplot as plt
#
# # import os
# # import conda
# #
# # conda_file_dir = conda.__file__
# # conda_dir = conda_file_dir.split('lib')[0]
# # proj_lib = os.path.join(os.path.join(conda_dir, 'share'), 'proj')
# # # os.environ["PROJ_LIB"] = proj_lib
# #
# # from mpl_toolkits.basemap import Basemap
#
# my_example_nc_file = r'C:\Users\sergi\OneDrive\Documents\Universidad\Articulo_clasificacion_climatica/precip.mon.mean.nc'
# fh = Dataset(my_example_nc_file, mode='r')
#
#
# lons = fh.variables['lon'][:]
# lats = fh.variables['lat'][:]
# precip = fh.variables['precip'][:]
#
# print(lons,lats)
#
#
# fh.close()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ruta=r'C:\Users\sergi\Desktop\Apertura_CompuertaLagoS.xlsx'
compuertas=pd.read_excel(ruta,header=0,usecols="F:G",index_col='Serie de Tiempo ')
compuertas=compuertas.replace(1,100)
fec1='2018'
fec2='2018'
plt.plot(compuertas.loc[fec1:fec2].index,compuertas.loc[fec1:fec2])
plt.show()