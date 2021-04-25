#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 15:12:19 2021

@author: Varvara Semenova
"""

import astropy.io.fits as fits
from astropy.table import Table, hstack, vstack
import pandas as pd

df = pd.read_csv('all_objects.csv')

df = df[(df['FLUX_G'] > 0) & (df['FLUX_R'] > 0) & (df['FLUX_Z'] > 0) & (df['FLUX_W1'] > 0) & (df['FLUX_W2'] > 0)] 

def shift(gflux, rflux, zflux):
    gshift = gflux * 10**(-0.4*0.004) * (gflux/rflux)**(-0.059)
    rshift = rflux * 10**(0.4*0.003) * (rflux/zflux)**(-0.024)
    zshift = zflux * 10**(0.4*0.013) * (rflux/zflux)**(+0.015)
    return gshift, rshift, zshift

north = df[df['HEMISPHERE'] == 'N']
g, r, z = shift(north['FLUX_G'], north['FLUX_R'], north['FLUX_Z'])


north['FLUX_G'] = g
north['FLUX_R'] = r
north['FLUX_Z'] = z
south = df[df['HEMISPHERE'] == 'S']
df = pd.concat([south, north], ignore_index=True)

df.to_csv('all_objects.csv', index = False)
