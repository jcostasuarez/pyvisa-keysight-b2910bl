# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 17:52:13 2023

@author: juancosta
"""

import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def exp_response(t, tau, A):
    return A*(1-np.exp(-t/tau))

sns.set_theme(style="whitegrid", palette="pastel")

data = pd.read_csv('20231023-143831_IV.txt',skiprows=1)

print(data)

plt.figure()
current_plot = sns.lineplot(data,x="Tiempo [S]",y="Corriente [A]")
current_plot.set_title("Corriente vs Tiempo")

plt.figure()
resistance_plot = sns.lineplot(data,x="Tiempo [S]",y="Resistencia [$\Omega$]")
resistance_plot.set_title("Resistencia vs Tiempo")

#################
#FITTING

Resistencia = data["Resistencia [$\Omega$]"].to_numpy()
Tiempo = data["Tiempo [S]"].to_numpy()

Resistencia -= Resistencia[0]
Resistencia /= Resistencia.max()

popt, pcov = curve_fit(exp_response, Tiempo, Resistencia)

Tau = popt[0]
desvio_Tau = np.sqrt(pcov[0,0])
A = popt[1]

Fit_Label = "Tau = "+f'{Tau:.3f}'+" segundos" + "\n Desvio de Tau = "+f'{desvio_Tau:.3f}' +" segundos"

data["Fit"] = (exp_response(Tiempo,Tau,A))
data["Resistencia Normalizada"] = Resistencia.tolist()

fig = plt.figure()

fit = sns.lineplot(data,x="Tiempo [S]",y="Resistencia Normalizada",label="Resistencia Normalizada")
fit = sns.lineplot(data,x="Tiempo [S]",y="Fit",label=Fit_Label,ax=fit)
fit.set_title("Ajuste temporal de la función exponencial")


plt.show()
 
