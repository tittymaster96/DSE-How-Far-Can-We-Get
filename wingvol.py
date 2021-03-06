from math import *
import numpy as np
import matplotlib.pyplot as plt
#import sympy
from scipy.integrate import quad
from parameters import *

#------------------------------------------------upper coordinates-----------------------------------------------------------

uppercoord = 'uppersurface.txt'

uppercoord = np.genfromtxt(uppercoord, dtype='string', delimiter=';')

uppercoordin = []

for i in range(len(uppercoord)):
    uppercoordin.append(uppercoord[i].split())

xcoordupper = []
ycoordupper = []

for i in range(len(uppercoordin)):
    xcoordupper.append(eval(uppercoordin[i][0]))
    ycoordupper.append(eval(uppercoordin[i][1]))

uppoly = np.polyfit(xcoordupper,ycoordupper,5)

x = np.arange(0,1,0.001)
yupper = []

def fupper(x):

    return uppoly[0]*x**(len(uppoly)-1) + uppoly[1]*x**(len(uppoly)-2) + uppoly[2]*x**(len(uppoly)-3) + uppoly[3]*x**(len(uppoly)-4) + uppoly[4]*x**(len(uppoly)-5) + uppoly[5]*x**(len(uppoly)-6)

for i in range(len(x)):
    yupper.append(fupper(x[i]))

#-----------------------------------------------lower coordinates------------------------------------------------------------

lowercoord = 'lowersurface.txt'

lowercoord = np.genfromtxt(lowercoord, dtype='string', delimiter=';')

lowercoordin = []

for i in range(len(lowercoord)):
    lowercoordin.append(lowercoord[i].split())

xcoordlower = []
ycoordlower = []

for i in range(len(lowercoordin)):
    xcoordlower.append(eval(lowercoordin[i][0]))
    ycoordlower.append(eval(lowercoordin[i][1]))

lowpoly = np.polyfit(xcoordlower,ycoordlower,4)

ylower = []

def flower(x):

    return lowpoly[0]*x**(len(lowpoly)-1) + lowpoly[1]*x**(len(lowpoly)-2) + lowpoly[2]*x**(len(lowpoly)-3) + lowpoly[3]*x**(len(lowpoly)-4) + lowpoly[4]*x**(len(lowpoly)-5)

for i in range(len(x)):
    ylower.append(flower(x[i]))
    
#--------------------------------------------difference coordinate--------------------------------------------------------------

def fdiff(x):

    diff = fupper(x)-flower(x)

    return diff

xr = np.arange(0,1,0.01)
imp = []
for i in range(len(xr)):
    imp.append(fdiff(xr[i]))
#--------------------------------------------------integrate--------------------------------------------------------------------

xstart = value("x_spar1")#"0.25"#raw_input("location of spar 1: ")
xend = value("x_spar2")#"0.55"#raw_input("location of spar 2: ")
print value('x_spar1')
def fint(xstart,xend):

    return quad(fdiff,xstart,xend,args=())[0]

#input 
b = value("b")#span(S,A)                       #span
taper = value("taper")#0.4 #IMPORT FROM WINGPLANFORM
c_r = value("c_r")#2*b/(A*(1+taper))             #root chord
c_t = value("c_t")#c_r*taper                     #tip chord
b_frac = 0.95                          #wing span used for fuel (from the inside)
d_ext_fus = value("d_ext_fus")#2.                          #IMPORT FROM PATRIK
b_eff = (b) - 2
cfac = 0.9                          #correction factor for loss of space in fuel tank

A_cross_section = fint(xstart,xend)
b_cur = np.arange(0.1,(b)/2+0.001,0.1)
vol = []
ilst = []

for i in range(len(b_cur)):
    # if b_cur[i] <= d_ext_fus/2:
    #     vol.append(0)
    if b_cur[i] >= b_eff/2:
        vol.append(max(vol))
    else:
        c_r_f = c_r
        c_t_f = c_r - b_cur[i] / (b / 2) * (c_r - c_t)
        c_avg = sqrt((c_r_f**3 - c_t_f**3)/(3*(c_r_f - c_t_f)))
        volume = cfac*2*b_cur[i]*A_cross_section*c_avg**2
        vol.append(volume)
        if volume >= value("fuelvolume_needed"):
            ilst.append(i)


fuel_in_wings = round(vol[len(vol)-1],4)
empty_tip = round((1-b_frac)*((b-d_ext_fus)/2),2)

#print c_r_f
#print c_t_f

##if len(ilst) > 0:
##    print volneeded,"m^3 of fuel can be fit within", round(b_cur[ilst[0]]/(b/2)*100,2), "% of the half span. The fuel tank is positioned in between", xstart, "and", xend, "x/c."
##    print "The last",round((b-d_fus)/2-b_cur[ilst[0]],2),"m span does not have to be used to place fuel (on both sides)."
##else:
##    print "You can fit",round(vol[len(vol)-1],4),"m^3 of fuel in the wings. Hence", volneeded - round(vol[len(vol)-1],4), "m^3 needs to be fit in the fuselage."
##    print "The last",round((1-b_frac)*((b-d_fus)/2),2),"m span has not been used to place fuel (on both sides)."
##
##font = {'family' : 'normal',
##        'weight' : 'normal',
##        'size'   : 14}
# plt.axhline(value('fuelvolume_needed'), linestyle="dashed", color="Red",label="17 m^3")
# plt.plot(b_cur[0:ilst[0]+1],vol)
# #plt.scatter(xcoordupper,ycoordupper)
# #plt.scatter(xcoordlower,ycoordlower,label="airfoil coordinates")
# #plt.plot(x,yupper,color="red",label="4th order polynomial")
# #plt.plot(x,ylower,color="red")
# #plt.axis((0,1,-0.5,0.5))
# #plt.rc('font', **font)
# plt.xlabel("x [m]")
# plt.ylabel("fuel volume [m^3]")
# ax = plt.subplot(111)
# box = ax.get_position()
# ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
# ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
# #plt.plot(xcoordlower,ycoordlower)
# plt.grid()
# plt.show()

string_wingvol = ["c_r_f","c_t_f","c_avg","fuel_in_wings","empty_tip","A_cross_section"]
print(fuel_in_wings)
