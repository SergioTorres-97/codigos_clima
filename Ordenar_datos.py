import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def muskingum_method(Upstream,initial_outflow_value,k,x,dt=1):
    O_0=initial_outflow_value

    C0=((-k*x)+0.5*dt)/((k*(1-x))+0.5*dt)
    C1=((k*x)+0.5*dt)/((k*(1-x))+0.5*dt)
    C2=((k*(1-x))-0.5*dt)/((k*(1-x))+0.5*dt)
    O=O_0
    Qd=[]
    for i in range(0,len(Upstream)):
        if i==len(Upstream)-1:
            break
        Oi=C0*Upstream[i+1]+C1*Upstream[i]+C2*O
        O=Oi
        Qd.append(Oi)

    Qd.insert(0,O_0)
    time=[i for i in range(0,len(Upstream))]

    plt.figure(figsize=(8,6))
    plt.plot(time,Qd,'.-', color='red')
    plt.plot(time,Upstream,'.-',color='blue')
    plt.xlim(0,len(Upstream)+5)
    plt.xticks(rotation=45, size='medium')
    plt.ylabel('Discharge [M3/S]', fontsize=14, **{'fontname': 'Times new roman'})
    plt.xlabel('Time [h]', fontsize=14, **{'fontname': 'Times new roman'})
    plt.title('Muskingum Routing', fontsize=14, **{'fontname': 'Times new roman'})
    plt.grid(linestyle='--',linewidth ='0.5')

    plt.show()

Qups=[50,100,200,325,450,600,700,780,790,775,750,680,590,500,420,350,300,250,225,200]
muskingum_method(Qups,50,2.3,0.15)
