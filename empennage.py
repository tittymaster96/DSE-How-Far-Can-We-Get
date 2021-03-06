# -*- coding: utf-8 -*-
"""
Created on Thu May 31 16:47:29 2018

@author: mrvan
"""

__author__ = 'Menno vd Toorn'
from scipy.integrate import quad
from scipy import optimize as opt
import numpy as np
import matplotlib.pyplot as plt
from math import *
from parameters import *

S = value("S")            #wing surface area
b = value("b")             #wing span
MAC =  value("MAC")        #mean aerodynamic chord

L_fus = value("l_fus")        #fuselage length

Vh =  1         #horizontal tail volume
Vv = 0.100      #vertical tail volume


lh = 20.96 #value("l_h") #rough estimate        #horizontal tail arm [m]
lv = 18.     #rough estimate
Sh = Vh*S*MAC/(lh)   #horizontal tail surface area
Sv = Vv*S*b/(lv)     #vertical tail surface area


sweep_h = 33  #degrees  
sweep_v = 40
Ah = 4.4    #aspect ratio
Av = 1.8
lambda_h = 0.5  #taper
lambda_v = 0.5

b_h = np.sqrt(Ah*Sh)  #horizontal tail span
b_v = np.sqrt(Av*Sv) #actual b_v = b_v/2

cr_h = 2*Sh/(b_h*(1+lambda_h))
ct_h = cr_h*lambda_h
cr_v = 2*Sv/(b_v*(1+lambda_v))
ct_v = cr_v*lambda_v

MAC_h = (2/3.)*(cr_h)*((1+lambda_h+lambda_h*lambda_h)/(1+lambda_h))
MAC_v = (2/3.)*(cr_v)*((1+lambda_v+lambda_v*lambda_v)/(1+lambda_v))

YMAC_h = (b_h/6.)*(1+2*lambda_h)/(1+lambda_h) 
YMAC_v = (b_v/6.)*(1+2*lambda_v)/(1+lambda_v)


string_empennage = ['Sh','Sv','lv','sweep_h','sweep_v','Ah','Av','lambda_h','lambda_v','b_h','b_v','cr_h',
                    'ct_h','cr_v','ct_v','MAC_h','MAC_v','YMAC_h','YMAC_v']
