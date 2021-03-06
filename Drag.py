#from scipy.integrate import quad
#from scipy import optimize as opt
#import numpy as np
#import matplotlib.pyplot as plt
import math
from parameters import *

#method 1
S_ref = value("S")
S_w_fuselage = value("c_r") * 4
S_ht_exp = 22.
S_vt_exp = value("Sv")
L_1 = value("ratio_nosecone") * 4
L_3 = value("ratio_tailcone") * 4
L_2 = value("l_fus") - L_1 - L_3
C_fe = value("C_f_e")


S_wing_wet = 1.07 * 2 *( S_ref - S_w_fuselage)
S_ht_wet = 1.05 * 2 * S_ht_exp
S_vt_wet = 1.05 * 2 * S_vt_exp
S_f_wet = (pi*4 / 4) * ((1/(3*L_1**2))*((4*L_1**2 + 4**2 / 4) - 4**3 / 8)- 4 + 4*L_2 + 2*sqrt(L_3**2 + 4**2 /4))

S_wet = S_wing_wet + S_ht_wet + S_vt_wet + S_f_wet

CD0 = S_wet/ S_ref * C_fe
#method 2

#fuselage
mu = 14.21*10**(-6)
k_fus = 0.052*10**-5
rho_cr = 0.3164
Re_cr_1 = rho_cr * value("V_cr") * value("l_fus") /mu
Re_cr_2 = 44.62*(value("l_fus")/k_fus)**1.053 * value("M_cr")**1.16
Re_cr_fus = min(Re_cr_1, Re_cr_2)

C_f_fus_lam = 1.328 / sqrt(Re_cr_fus)
C_f_fus_tur = 0.455 / ((log10(Re_cr_fus))**2.58 * (1+0.144*value("M_cr")**2)**0.65)
C_f_fus = 0.15 * C_f_fus_lam + 0.85 * C_f_fus_tur


#wing
k_wing = 0.052*10**-5
Re_cr_wing = min(rho_cr*value("V_cr")*value("MAC")/mu , 44.62*(value("MAC")/k_fus)**1.053 * value("M_cr")**1.16)

C_f_wing_lam = 1.328 / sqrt(Re_cr_wing)
C_f_wing_tur = 0.455 / ((log10(Re_cr_wing))**2.58 * (1+0.144*value("M_cr")**2)**0.65)
C_f_wing = 0.65 * C_f_wing_lam + 0.35 * C_f_wing_tur        #using HLFC

#vertical tail
k_vt = 0.052*10**-5
Re_cr_vt = min(rho_cr * value("V_cr")*value("MAC_v")/mu , 44.62*(value("MAC_v")/k_fus)**1.053 * value("M_cr")**1.16)

C_f_vt_lam = 1.328 / sqrt(Re_cr_vt)
C_f_vt_tur = 0.455 / ((log10(Re_cr_vt))**2.58 * (1+0.144*value("M_cr")**2)**0.65)
C_f_vt = 0.65 * C_f_vt_lam + 0.35 * C_f_vt_tur

#horizontal tail
k_ht = 0.052*10**-5
Re_cr_ht = min(rho_cr * value("V_cr")*value("MAC_h")/mu , 44.62*(value("MAC_h")/k_fus)**1.053 * value("M_cr")**1.16)

C_f_ht_lam = 1.328 / sqrt(Re_cr_ht)
C_f_ht_tur = 0.455 / ((log10(Re_cr_ht))**2.58 * (1+0.144*value("M_cr")**2)**0.65)
C_f_ht = 0.65 * C_f_ht_lam + 0.35 * C_f_ht_tur

#form factor

#fuselage
f = value("F")
FF_fus = (1+ 60/f**3 + f/400)

#wing
lambdac_m_wing = atan(tan(value("lambdac_LE")) - (4/value("A"))*(0.38*(1-value("taper"))/(1+value("taper"))))
xc_wing = 0.38
tc_wing = 0.12

FF_wing = (1+ 0.6/ xc_wing * tc_wing + 100 * tc_wing**4) * (1.34 * value("M_cr")**0.18 * lambdac_m_wing**0.28)

#horizontal tail
lambdac_m_ht = atan(tan(value("sweep_h")*pi/180) - (4/value("Ah"))*(0.3*(1-value("lambda_h"))/(1+value("lambda_h"))))
xc_ht = 0.3
tc_ht = 0.12

FF_ht = (1+ 0.6/ xc_ht * tc_ht + 100 * tc_ht**4) * (1.34 * value("M_cr")**0.18 * lambdac_m_ht**0.28)

#vertical tail
lambdac_m_vt = atan(tan(value("sweep_v")*pi/180) - (4/value("Av"))*(0.3*(1-value("lambda_v"))/(1+value("lambda_v"))))
xc_vt = 0.3
tc_vt = 0.12

FF_vt = (1+ 0.6/ xc_vt * tc_vt + 100 * tc_vt**4) * (1.34 * value("M_cr")**0.18 * lambdac_m_vt**0.28)

#strut
xc_strut = 0.50
tc_strut = 0.21
MAC_strut = 0.45
b_strut = 7.2

FF_strut = (1+ 0.6/ xc_strut * tc_strut + 100 * tc_strut**4) * (1.34 * value("M_cr")**0.18)

k_strut = 0.634*10**-5
Re_cr_strut = min(rho_cr * value("V_cr")* MAC_strut / mu , 44.62* (MAC_strut / k_strut)**1.053 * value("M_cr") **1.16)


C_f_strut_lam = 1.328 / sqrt(Re_cr_strut)
C_f_strut_tur = 0.455 / ((log10(Re_cr_strut))**2.58 * (1+0.144*value("M_cr")**2)**0.65)
C_f_strut = 0.15 * C_f_strut_lam + 0.85 * C_f_strut_tur

dC_D_strut = C_f_strut * FF_strut * 1.1 * b_strut * MAC_strut *2
print(2* dC_D_strut /S_ref)

#pylon
xc_p = 0.5
tc_p = 0.1

FF_p = (1+ 0.6/ xc_p * tc_p + 100 * tc_p**4) * (1.34 * value("M_cr")**0.18 )

#nacelle
f_nac = value("ln")/ value("Dn")
FF_nac = 1 + 0.35/f_nac

IF_fuselage = 1.
IF_wing = 1.
IF_tail = 1.04
IF_strut = 1.1
IF_nacelle = 1.3

#base CD0

CD0_base = 1./S_ref *( (C_f_fus*FF_fus*IF_fuselage*S_f_wet) + (C_f_wing*FF_wing*IF_wing*S_wing_wet)+ (C_f_ht*FF_ht*IF_tail*S_ht_wet)+ (C_f_vt*FF_vt*S_vt_wet) + dC_D_strut *2)
print((C_f_fus*FF_fus*IF_fuselage*S_f_wet)/S_ref)
#Miscellaneous drag

#fuselage base drag
u = atan((4/2) / L_3)
C_D_fus1 = ((0.139 + 0.419*(value("M_cr")-0.161)**2)* 0.2 * 0.2) /S_ref
C_D_fus2 = (3.83 * u**2.5 * pi * (4/2)**2) /S_ref

# # #landing gear

dCD_landinggear = 0.48342 / S_ref

# Flaps higher than 10 degrees take-off
F_flap = 0.0074
c_fc = 0.35  #flap chord length      #wing chord
S_flap = 69.6     #flap surface area
delta_flap_land =  40.      #should be in degrees
dCD_flap_land = F_flap *(c_fc) * (S_flap / S_ref) * (delta_flap_land -10 )
delta_flap_TO =  15.      #should be in degrees
dCD_flap_TO = F_flap *(c_fc) * (S_flap / S_ref) * (delta_flap_TO -10 )

# #slats
F_slat = 0.0074
c_fc_slat = 0.15  #flap chord length      #wing chord
S_slat = 83.8     #flap surface area
delta_slat_land =  25.      #should be in degrees
dCD_slat_land = F_slat *(c_fc_slat) * (S_slat / S_ref) * (delta_slat_land -10 )
delta_slat_TO = 14.     #should be in degrees
dCD_slat_TO = F_slat *(c_fc_slat) * (S_slat / S_ref) * (delta_slat_TO -10 )

#Excresence drag
dCD_excresence = 0.03

#total CD0
CD0_tot = (CD0_base + C_D_fus1 +C_D_fus2 ) * (1+dCD_excresence)
print(CD0_tot)

#drag due to lift
A_eff = value("A") + 0.75
e = 1 / (1.05 + 0.007* pi * A_eff)              # Obert method
#e = e + 0.0046 * delta_f #for flap deflection
CL = 0.55
CD = CD0_tot + CL**2 / (pi * A_eff * e)

string_drag = ['A_eff', 'e', 'CD0_tot', 'dCD_excresence', 'S_wet']


CD0_TO = CD0_tot + dCD_flap_TO + dCD_slat_TO + dCD_landinggear
CD_0_TO_nogear = CD0_tot + dCD_flap_TO + dCD_slat_TO
CD_0_land = CD0_tot + dCD_flap_land + dCD_landinggear + dCD_slat_land



string_drag = ['A_eff', 'e', 'CD0_tot', 'dCD_excresence', 'S_wet', 'dCD_flap_TO', 'dCD_flap_land']