from math import *
import matplotlib.pyplot as plt
from parameters import *

#---------------------------------PARAMETERS---------------------------------------

SM = 0.05
C_L_alpha_h =
C_L_alpha_Ah =
downwash = 
l_h = value("l_h")
c_bar =
V_h_over_V = sqrt(0.85) #vraag In 't Veld
c_bar_ac =
C_L_h = -0.8
C_L_Ah = 
C_m_ac = 0.
C_L_Ah =
x_bar_ac = 

x_bar_cg = np.arange(0,1,0.001)
Sh_S_stab = []
Sh_S_cont = []

#---------------------------------STABILITY----------------------------------------
for i in x_bar_ac:
    
    m = (C_L_alpha_h/C_L_alpha_Ah*(1-downwash)*l_h/c_bar*(V_h_over_V)**2)**-1
    q = -(x_bar_ac - SM)/(C_L_alpha_h/C_L_alpha_Ah*(1-downwash)*l_h/c_bar*(V_h_over_V)**2)

    Sh_S_stab.append(m*i + q)

#---------------------------------CONTROLLABILITY--------------------------------------

for i in x_bar_ac:
    n = (C_L_h/C_L_Ah*l_h/c_bar*(V_h_over_V)**2)**-1
    p = (C_m_ac/C_L_Ah-x_bar_ac)/(C_L_h/C_L_Ah*l_h/c_bar*(V_h_over_V)**2)

    Sh_S_cont.append(n*i + p)

plt.plot(x_bar_ac,Sh_S_stab)
plt.plot(x_bar_ac,Sh_S_cont)
plt.xlabel("x_bar_ac")
plt.ylabel("Sh/S")
plt.label
plt.show()
