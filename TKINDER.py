# import tkinter
#
# ventana=tkinter.Tk()
# ventana.geometry('1000x1000')
# ventana.title("POTENCIALES")
# ventana.configure(background='#18238E')
#
# #ventana.configure(background="#2B4C6E") #Color de fondo
#
# L1=tkinter.Label(ventana,text='Ruta_HEC-RAS: ',bg='white',fg='black')
# L1.place(relx=0.01, rely=0.1, relwidth=0.1, relheight=0.025)
#
# E1=tkinter.Entry(ventana)
# E1.place(relx=0.12, rely=0.1, relwidth=0.85, relheight=0.025)
#
#
# # titulo=tkinter.Label(ventana, text="POTENCIAL DE DÉFICIT HÍDRICO",height=2,font=("Times", 20, "italic"))
# # titulo.pack(anchor='center')
#
# # step = tkinter.LabelFrame(ventana, text="POTENCIAL DE DÉFICIT HÍDRICO", font="Arial 20 bold italic")
# # step.grid(row=0, columnspan=7, padx=100, pady=5, ipadx=225, ipady=25)
#
# # def texto_caja():
# #     text=texto.get()
# #     print(text)
# #
# # # def saludo(nombre):
# # #     print('Hola',nombre)
# # texto=tkinter.Entry(ventana,font='calibri')
# # texto.pack()
# # boton1=tkinter.Button(ventana,text='click',command=texto_caja)
# # boton1.pack()
# ventana.mainloop()


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def Abrir_excel(ruta_carpeta,nombre_excel,nombre_hoja):
    vars()[str(nombre_hoja)]=pd.read_excel(ruta_carpeta+'\\'+str(nombre_excel)+'.xlsx',header=0,index_col='Fecha',sheet_name=str(nombre_hoja))
    return vars()[str(nombre_hoja)]

#Varables climáticas
ruta_carpeta=r'C:\Users\sergi\OneDrive\Documents\Universidad\Proyecto_BIO\Proyecto_Boyaca_BIO\Modelos\Modelo_sistemas_lenticos\Lago_Sochagota'
nombre_excel='Precipitacion'
Precipitacion=Abrir_excel(ruta_carpeta,nombre_excel,'Sheet1')

Año1,Año2,Año3=1990,2002,2014
serie1=Precipitacion['TUNGUAVITA - AUT [24035430]'].loc[str(Año1):str(Año1)]
serie2=Precipitacion['TUNGUAVITA - AUT [24035430]'].loc[str(Año2):str(Año2)]
serie3=Precipitacion['TUNGUAVITA - AUT [24035430]'].loc[str(Año3):str(Año3)]

serie1=list(serie1.groupby(lambda m:m.month).sum())
serie2=list(serie2.groupby(lambda m:m.month).sum())
serie3=list(serie3.groupby(lambda m:m.month).sum())

def grafica_mensual(serie1,serie2,serie3,Año1,Año2,Año3):
    meses=['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dec']
    fig, ax = plt.subplots(figsize=(15,6))
    index = np.arange(1,len(serie1)+1)
    bar_width=0.25
    plt.minorticks_on()
    plt.grid(which='major', linestyle='-', linewidth='0.5',zorder=0)
    plt.grid(which='minor', linestyle=':', linewidth='0.5',zorder=0)
    serie1_graph=plt.bar(index, serie1, bar_width
                  ,color='#F3800C',label='serie 1: '+str(Año1),zorder=3)
    serie2_graph=plt.bar(index + bar_width,
                     serie2, bar_width,color='olivedrab',label='serie 2: '+str(Año2),zorder=3)
    serie3_graph=plt.bar(index + 2*bar_width,
                     serie3, bar_width,color='#0B3012',label='serie 3: '+str(Año3),zorder=3)
    plt.xlabel('Ciclo de gestión',fontsize=14,fontweight='bold',**{'fontname':'calibri'})
    plt.ylabel('Precipitación total mensual [MM]',fontsize=14,fontweight='bold',**{'fontname':'calibri'})
    plt.xticks(index + bar_width, meses,
               size='large',color ='k',rotation = 45,**{'fontname':'calibri'})
    plt.yticks(size='large',color ='k',rotation = 0,**{'fontname':'calibri'})
    plt.legend()

grafica_mensual(serie1,serie2,serie3,Año1,Año2,Año3)
plt.show()










