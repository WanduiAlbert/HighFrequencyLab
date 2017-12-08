#! /usr/bin/env python3

import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

#calculate the antenna gain
d = 2.6 * 2.54e-2 #diameter of can
nu = 5.9e9 #GHz
p11 = 1.8412
c = 3e8

lambda_g = ((nu/c)**2 - (p11/(np.pi*d))**2)**(-0.5) #wavelength in waveguide

lambda_f = (c/nu) #wavelength in free space

G_m = 20*np.log10(np.pi*d/lambda_f)

nu_cutoff = c*(p11/np.pi/d)

print ("The wavelength in the waveguide is {0:1.3f} mm".format(lambda_g*1e3))
print ("The wavelength in free space is {0:1.3f} mm".format(lambda_f*1e3))

print ("The maximum gain of the cantenna is {0:2.1f} dBi".format(G_m)) 

print ("The cutoff frequency of the antenna is {0:2.1f} GHz".format(nu_cutoff/1e9))


# p_factor = 10 * np.log10(lambda_f**2/((4*np.pi)**3 * R**4))

new_d = c*(p11/np.pi/3e9) * 1e3 # diameter in mm of can for a 3 GHz cutoff frequency
new_G = 20 * np.log10(np.pi*d/lambda_g)

print ("For a 3 GHz cutoff my can needs to be {0:2.1f} inches".format(new_d/25.4))
print ("with a gain of {0:2.2f} dBi".format(new_G))

Prx = -81 #dBm
R = 20 #m
sigma  =10 # scattering cross-section 3-10m^2 for cars, 1m^2 for person

f = 10 * np.log10((4*np.pi)**3 * R**4/sigma/ lambda_f**2)
print ("The propagation factor is {0:2.2f} dB".format(f))

print ("P_tx times G^2 = {0:2.2f} dB".format(f + Prx))


d = np.r_[2:10:100j]
cutoff = c * (p11/np.pi/(d*2.54e-2)) 
lambda_g  = ((nu/c)**2 - (p11/(np.pi*(d*2.54e-2)))**2)**(-0.5)
gain = 20 * np.log10(np.pi*(d*2.54e-2)/lambda_f)

fig, ax = plt.subplots(figsize=(10,10))
ax.plot(d, cutoff/1e9)
ax2 = ax.twinx()
ax2.plot(d, gain, 'r')
ax.set_xlabel('Cantenna Diameter [inches]')
ax.set_ylabel('Cutoff Frequency [GHz]')
ax2.set_ylabel(r'Gain [dBi]')
ax.grid(which='both')

plt.savefig('cantenna.png')
# ax.hlines()

# # fig2, ax2 = plt.subplots(figsize=(10,10))
# # ax2.plot(d, gain)
# # ax2.set_xlabel('Diameter')
# # ax2.set_ylabel('Gain')



Ptx = 25.5 #dBm
G = 4.5
f = Ptx + 2*G - Prx

R = (10**(f/10) * lambda_f**2 * sigma/(4*np.pi)**3)**0.25

print ("The range of my radar is now {0:2.2f} m ".format(R))