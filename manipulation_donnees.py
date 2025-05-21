import uproot
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

file = uproot.open("Ak10Jet_82.root")
events=file['eventtree'].arrays(library='pd')

achanger=['ak10_true_E','ak10_true_mass','ak10_true_pt']
for i in achanger:
    events[i]=events[i]/1000

events['rE']=events['ak10_E']/events['ak10_true_E']
events['rm']=events['ak10_mass']/events['ak10_true_mass']

events['rE_cal']=events['ak10_cal_E']/events['ak10_true_E']
events['rm_cal']=events['ak10_cal_mass']/events['ak10_true_mass']

def histogrammes_E(df):
    energy_ranges = [(0, 200), (200, 400), (400, 600), (600, 800), (800,1000), (1000, float('inf'))]

    plt.figure()
    df['rE'].hist(bins=1000, alpha=0.5,label='Brut',range=(0,4))
    df['rE_cal'].hist(bins=1000, alpha=0.5,label='Calibré',range=(0,4))
    plt.legend()
    plt.show()

    for e_min, e_max in energy_ranges:
        if e_max == float('inf'):
            filtered_df = df[df['ak10_true_E'] >= e_min]
            title = f"Énergie >= {e_min}"
        else:
            filtered_df = df[(df['ak10_true_E'] >= e_min) & (df['ak10_true_E'] <= e_max)]
            title = f"Énergie entre {e_min} et {e_max}"
        
        plt.figure()
        filtered_df['rE'].hist(bins=1000, alpha=0.5,label='Brut',range=(0,4))
        filtered_df['rE_cal'].hist(bins=1000, alpha=0.5,label='Calibré',range=(0,4))
        plt.title(title)
        plt.legend()
        plt.show()
        
def histogrammes_m(df):
    energy_ranges = [(0, 200), (200, 400), (400, 600), (600, 800), (800,1000), (1000, float('inf'))]

    plt.figure()
    df['rm'].hist(bins=1000, alpha=0.5,label='Brut',range=(0,4))
    df['rm_cal'].hist(bins=1000, alpha=0.5,label='Calibré',range=(0,4))
    plt.legend()
    plt.show()

    for e_min, e_max in energy_ranges:
        if e_max == float('inf'):
            filtered_df = df[df['ak10_true_E'] >= e_min]
            title = f"Énergie >= {e_min}"
        else:
            filtered_df = df[(df['ak10_true_E'] >= e_min) & (df['ak10_true_E'] <= e_max)]
            title = f"Énergie entre {e_min} et {e_max}"
        
        plt.figure()
        filtered_df['rm'].hist(bins=1000, alpha=0.5,label='Brut',range=(0,4))
        filtered_df['rm_cal'].hist(bins=1000, alpha=0.5,label='Calibré',range=(0,4))
        plt.title(title)
        plt.legend()
        plt.show()

histogrammes_E(events)
histogrammes_m(events)

def recherche_max_hist_E(df):
    energy_ranges = [(0, 200), (200, 400), (400, 600), (600, 800), (800, 1000), (1000, float('inf'))]
    RE={i:0 for i in energy_ranges}
    RE_cal={i:0 for i in energy_ranges}
    for e_min, e_max in energy_ranges:
        if e_max == float('inf'):
            filtered_df = df[df['ak10_true_E'] >= e_min]
        else:
            filtered_df = df[(df['ak10_true_E'] >= e_min) & (df['ak10_true_E'] <= e_max)]
        h1=np.histogram(filtered_df['rE'],bins=1000,range=(0,4))
        i1=np.argmax(h1[0])
        m1=h1[1][i1]
        RE[(e_min,e_max)]=m1
        
        h2=np.histogram(filtered_df['rE_cal'],bins=1000,range=(0,4))
        i2=np.argmax(h2[0])
        m2=h2[1][i2]
        RE_cal[(e_min,e_max)]=m2
    return RE,RE_cal

def recherche_max_hist_m(df):
    energy_ranges = [(0, 200), (200, 400), (400, 600), (600, 800), (800, 1000), (1000, float('inf'))]
    Rm={i:0 for i in energy_ranges}
    Rm_cal={i:0 for i in energy_ranges}
    for e_min, e_max in energy_ranges:
        if e_max == float('inf'):
            filtered_df = df[df['ak10_true_E'] >= e_min]
        else:
            filtered_df = df[(df['ak10_true_E'] >= e_min) & (df['ak10_true_E'] <= e_max)]
        h1=np.histogram(filtered_df['rm'],bins=1000,range=(0,4))
        i1=np.argmax(h1[0])
        m1=h1[1][i1]
        Rm[(e_min,e_max)]=m1
        
        h2=np.histogram(filtered_df['rm_cal'],bins=1000,range=(0,4))
        i2=np.argmax(h2[0])
        m2=h2[1][i2]
        Rm_cal[(e_min,e_max)]=m2
    return Rm,Rm_cal
    
RE,RE_cal=recherche_max_hist_E(events)
Rm,Rm_cal=recherche_max_hist_m(events)

e=[]
for i in RE.keys():
    if float('inf') in i: e.append(i[0])
    else: e.append((i[0]+i[1])/2)
    
E=np.array(e)
re=[]
for i in RE.items():
    re.append(i[1])
Re=np.array(re)

plt.figure()
plt.plot(E,Re)
plt.show()

