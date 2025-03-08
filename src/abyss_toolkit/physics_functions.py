import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import numba
from pytreegrav import Potential
from yt.units import pc, Msun, g,cm, km, s

msun_g  = float((1*Msun).in_cgs().d)
pc_cm   = float((1*pc).in_cgs().d)
kms_cms = float((1*km/s).in_cgs().d)
g_msun  = 1/float((1*Msun).in_cgs().d)
cm_pc   = 1/float((1*pc).in_cgs().d)
cms_kms = 1/float((1*km/s).in_cgs().d)
G       = 6.67430e-8 # cgs


def get_kinetic_energy(ptcl):
    v_com = np.mean(ptcl[:,3:6],axis=0)
    v2 = np.sum((ptcl[:,3:6]-v_com)**2, axis=1)
    return np.sum(ptcl[:,6]*v2)/2 #,ptcl[:,6]*v2/2

def get_potential_energy(ptcl):
    # Create a Potential object
    potentials = Potential(ptcl[:,:3], ptcl[:,6], [0]*ptcl.shape[0])

    # Calculate the total potential energy
    return 0.5 * G * np.sum(ptcl[:,6] * potentials)