from math import *
import numpy as np
import matplotlib.pyplot as plt
#------------------------------------------------CONVERSION--------------------------------------------------

lbf_to_N = 4.4482216
hr_to_s = 3600.
lbm_to_kg = 0.45359237
ft_to_km = 0.3048/1000
ft_to_m = 0.3048
gal_to_L = 3.78541
FL_to_m = ft_to_m*100
rad_to_deg = 180/pi
inch_to_cm=2.54
cm_to_inch=1/2.54
mm_to_m=1./1000.
m_to_mm=1000.
cm_to_m=1/100.
inch_to_m=inch_to_cm*cm_to_m
rad_to_deg=180/pi
deg_to_rad=pi/180

m_to_cm=1/100.

M_tf = 0.935                        #technology factor for supercritical airfoils
FL = 390                            #flight level
h_cr = FL*FL_to_m                   #cruise altitude
R = 287.05
g = 9.80665                         #gravitational acc.
gamma = 1.4
M_cr = 0.79                         #cruise mach number (req)
M_max = 0.82                        #maximum cruise mach number
rho_0 = 1.225                       #sea-level density
T_0 = 288.15                        #sea-level temperature 
s_l = 2000.                         #landing distance
V_land = sqrt(s_l/0.5847)           #landing velocity based on landing distance
cV = 0.024                          #climb gradient requirement from CS25
A = 14.                             #Aspect ratio
c = 17.                             #climb rate as from ref. aircraft
C_f_e = 0.003                       #friction coefficient
V_s = 100.                          #stall speed based on reference aircraft
V_rot = 1.1                         #rotation speed
n_max = 2.5                         #max load factor (CS25)
f = 0.9745                          #fuel fraction during cruise

mft        = 3.2808399        # conversion factor meters to feet
kglbs      = 2.20462262       # conversion factor kilograms to pounds
sqmsqft    = 10.7639104       # conversion factor square meters to square feet
mskts      = 1.94384449       # conversion factor meters per seconds to knots
degrad     = 0.0174532925     # conversion factor degrees to radians
kmnm       = 0.539956803      # conversion factor kilometers to nautical miles
Nlbs       = 0.224808943      # conversion factor newtons to pounds
papsf      = 0.02089          # conversion factor pascal to pound-force per square foot
kgmlbsgall = 0.00834540445    # conversion factor for kilogram per cubic meter to pounds per gallon
papsi      = 0.000145037738   # conversion factor for pascal to pounds-force per square inch


#------------------------------------------------FUNCTIONS-----------------------------------------------------

#---------PARAMETERS----------

def value(symbol):
    file = 'parameters.txt'
    file = np.genfromtxt(file, dtype=str, delimiter=';')
    lst = []
    found = False

    for i in range(len(file)):
        lst.append(file[i].split())

    for i in range(len(lst)):
        if lst[i][0] == symbol:
            found == True
            return eval(lst[i][1])
    if found == False:
        return "parameter has not been found"
    
#------------ISA--------------

lapselst = [-.0065,0,.001,.0028,0,-.0028,-.002,0.]
hlst = [0,11000,20000,32000,47000,51000,71000,84852,100000]
T0lst = [288.15]
p0lst = [101325]
g = 9.80665
R = 287.05

for i in range(1,8):
    T0 = T0lst[i-1] + lapselst[i-1]*(hlst[i]-hlst[i-1])
    T0lst.append(T0)
    
    if lapselst[i-1] != 0:
        p0 = p0lst[i-1] * (T0lst[i]/T0lst[i-1])**(-g/(lapselst[i-1]*R))
    else:
        p0 = p0lst[i-1] * e**(-g/(R*T0lst[i])*(hlst[i]-hlst[i-1]))

    p0lst.append(p0)
    
def ISA(h):
    for i in range(8):
        if hlst[i] <= h <= hlst[i+1]:
            h0 = hlst[i]
            T0 = T0lst[i]
            p0 = p0lst[i]
            a  = lapselst[i]
            
            if a != 0:
                T = T0 + a*(h-h0)
                p = p0 * (T/T0)**(-g/(a*R))
            else:
                T = T0
                p = p0 * e**(-g/(R*T0)*(h - h0))

            rho = p / (R*T)

    return T,p,rho

def ISA_rho(rho):
    T0 = T0lst[i]
    a  = lapselst[i]
    if rho > ISA(11000)[2]:
        h = (rho/1.225**((-g/(a*R)-1)**-1)-1)*T0/a
#--------------speed------------------

def a(h): #speed of sound

    a = sqrt(value("gamma")*value("R")*ISA(h)[0])

    return a

def max_speed(h):

    V = value("M_max")*a(h)

    return V
    
def cruise_speed(h_cr):

    V_cr = value("M_cr")*a(value("h_cr"))

    return V_cr

#---------dynamic pressure------------

def q(V,h): 

    q = 0.5*ISA(h)[2]*V**2

    return q

def cruise_q(h_cr):
    
    q_cr = 0.5*ISA(value("h_cr"))[2]*cruise_speed(value("h_cr"))**2

    return q_cr

#-------------thrust------------------

def cruise_thrust(h,C_D_cr,S):
    
    T_cr = 0.5*ISA(h)[2]*cruise_speed(h)**2*value("C_D_cr")*value("S")

    return T_cr

